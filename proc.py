import store
import arg

class Proc(object):
	pass

class SH7058(Proc):
	def __init__(self, function_reset=False):
		self.GPR = store.RegFile(function_reset=function_reset)
		self.Mem = store.MemFile(function_reset=function_reset)

	def reset(self):
		self.GPR.reset()
		self.Mem.reset()

	def function_reset(self):
		self.GPR.function_reset()
		self.Mem.function_reset()

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

	def execute(self, asm):
		map(lambda a:a.pre_effect(self), asm.args)

		if asm.instruction == 'nop':
			pass
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
