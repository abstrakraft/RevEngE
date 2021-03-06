import sys
import parse_inst
import expr

class AsmLine(object):
	def __init__(self, address, val, instruction, spec, args, attr):
		self.address = address
		self.val = val
		self.instruction = instruction
		self.spec = spec
		self.args = args
		self.attr = attr

	@classmethod
	def import_listing(cls, asm_listing):
		fields = asm_listing.split('\t')
		if len(fields) < 4:
			fields.append('{}')
		elif fields[3] == "":
			fields[3] = '{}'

		(inst, spec, args) = parse_inst.parser.parse(fields[2])
		return cls(int(fields[0][:-1], 16), int(fields[1], 16), inst, spec, args, eval(fields[3]))

	def __str__(self):
		return self.export_listing()

	def export_listing(self):
		asm_string = self.export_string()
		if self.attr == {}:
			return '%8x:\t%.4x\t%s' % (self.address, self.val, asm_string)
		else:
			return '%8x:\t%.4x\t%s\t%s' % (self.address, self.val, asm_string, self.attr)

	def export_string(self):
		return self.instruction + (self.spec and ('.' + self.spec) or '') + (self.args and (' ' + ','.join(map(str, self.args))) or '')

class AsmListing(object):
	def __init__(self, code):
		self.code = code
		self.map = {}
		for c in self.code:
			self.map[c.address] = c

	def __getitem__(self, key):
		if isinstance(key, slice):
			return type(self)(self.code.__getitem__(key))
		else:
			return self.code[key]

	@classmethod
	def import_file(cls, file):
		return cls.import_string(open(file).read())

	@classmethod
	def import_string(cls, s):
		lines = s.split('\n')
		if lines[-1] == '':
			del lines[-1]
		return cls(map(AsmLine.import_listing, lines))

	def export_file(self, file):
		f = open(file, 'w')
		f.write(self.export_string() + '\n')

	def export_string(self):
		return '\n'.join(map(lambda c: c.export_listing(), self.code))

	def export_c_file(self, file):
		f = open(file, 'w')
		f.write(self.export_c_string() + '\n')

	def export_c_string(self):
		in_func = False
		in_data = False
		delay_print = False
		output = []
		for c in self.code:
			if delay_print:
				delay_print = False
				s = '\t\t%s' % c.export_string()
				if 'comment' in c.attr:
					s += '\t\\\\ %s' %c.attr['comment']
				output.append(s)
				output.extend(delay_print_suffix)
			elif in_func:
				s = '\t\t%s' % c.export_string()
				if 'comment' in c.attr:
					s += '\t%s' %c.attr['comment']
				output.append(s)
				inst = c.instruction
				if inst == 'rts' or ((inst == 'bra') and (c.address == int(str(c.args[0]), 16))):
					in_func = False
					delay_print = True
					delay_print_suffix = ['\t}','}','']
			elif in_data:
				if 'data' in c.attr:
					output.append('\t%4x }' % c.val)
					in_data = False
				else:
					output.append('\t0x%4x, \\' % c.val)
			elif 'entry' in c.attr:
				in_func = True
				output.append('%s()' % c.attr['entry'])
				output.append('{')
				output.append('\tasm {')
				output.append('\t\t%s' % c.export_string())
			elif 'data' in c.attr:
				in_data = True
				output.append('%s = { %4x, \\' % (c.attr['data'], c.val))
		return '\n'.join(output)

	def mark_all_entry_points(self):
		main = (code[0][1] << 16) | code[1][1]
		code[main/2][3]['entry'] = 'main'

	def mark_entry_points(self, start):
		pass

class AsmPattern(object):
	def __init__(self, pattern):
		self.pattern = map(lambda p: p.split(';'), pattern.split('|'))

	def match(self, code, start=0, end=-1):
		if end == -1:
			end = len(code)
		pattern_cursor = [0]*len(self.pattern)
		for idx in xrange(start, end):
			for p_idx in xrange(len(self.pattern)):
				if code[idx].instruction == self.pattern[p_idx][pattern_cursor[p_idx]]:
					pattern_cursor[p_idx] += 1
					if pattern_cursor[p_idx] == len(self.pattern[p_idx]):
						yield (p_idx, idx - pattern_cursor[p_idx] + 1)
						pattern_cursor = [0]*len(self.pattern)
						break
				else:
					pattern_cursor[p_idx] = 0


if __name__ == '__main__':
	code = AsmListing.import_file('asm/test.asm')
	#code.export_file('alex_export.asm')
