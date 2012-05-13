import store
import arg

class Proc(object):
	pass

class SH7058(Proc):
	def __init__(self, function_reset=False):
		self.GPR = store.RegFile(function_reset=function_reset)
		self.Mem = store.MemFile(function_reset=function_reset)

		self.pre_delay_asm = None

	def reset(self):
		self.GPR.reset()
		self.Mem.reset()

		self.pre_delay_asm = None

	def function_reset(self):
		self.GPR.function_reset()
		self.Mem.function_reset()

		self.pre_delay_asm = None

	def __getitem__(self, key):
		if isinstance(key, basestring):
			if key[0].lower() == 'r':
				return self.GPR[int(key[1:])]
			else:
				raise KeyError('unrecognized key %s' % key)
		else:
			raise KeyError('unrecognized key %s' % str(key))

	def __setitem__(self, key, value):
		if isinstance(key, basestring):
			if key[0].lower() == 'r':
				self.GPR[int(key[1:])] = value
			else:
				raise KeyError('unrecognized key %s' % key)
		else:
			raise KeyError('unrecognized key %s' % str(key))

	def __str__(self):
		return '<GPR = %s, Mem = %s>' % (self.GPR, self.Mem)

	delay_slot_instructions = ['bsr']

	def execute(self, asm, pre_delay=False):
		if not pre_delay and asm.instruction in self.delay_slot_instructions:
			self.pre_delay_asm = asm
			return None

		output = []

		map(lambda a:a.pre_effect(self), asm.args)

		if asm.instruction == 'nop':
			pass
		elif asm.instruction == 'bsr':
			output.append('r0 = (%s)();' % str(asm.args[0].get_address(self)))
		elif asm.instruction == 'jsr':
			output.append('r0 = (%s)();' % str(asm.args[0].get_address(self)))
		elif asm.instruction == 'add':
			v1 = asm.args[0].get_value(self)
			v2 = asm.args[1].get_value(self)
			asm.args[1].store_value(self, v1+v2)
		elif asm.instruction == 'and':
			v1 = asm.args[0].get_value(self)
			v2 = asm.args[1].get_value(self)
			asm.args[1].store_value(self, v1&v2)
		elif asm.instruction == 'or':
			v1 = asm.args[0].get_value(self)
			v2 = asm.args[1].get_value(self)
			asm.args[1].store_value(self, v1|v2)
		elif asm.instruction == 'mov':
			if asm.spec:
				v1 = asm.args[0].get_value(self)
				asm.args[1].store_value(self, v1)
			else:
				v1 = asm.args[0].get_value(self)
				asm.args[1].store_value(self, v1)
		else:
			raise NotImplementedError('instruction %s not implemented for execution' % asm.instruction)

		map(lambda a:a.post_effect(self), asm.args)

		if not pre_delay and self.pre_delay_asm:
			r = self.execute(self.pre_delay_asm, pre_delay=True)
			if r:
				output.extend(r)
			self.pre_delay_asm = None

		return output
