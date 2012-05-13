import collections
import expr

class Store(object):
	def __init__(self):
		pass

class RegFile(Store):
	def __init__(self, no_reset=False, function_reset=False, reg=None, marked=None):
		super(RegFile, self).__init__()
		if reg is None:
			self.reg = [None]*16
		else:
			self.reg = reg
		if marked is None:
			self.marked = [False]*16
		else:
			self.marked = marked

		if not no_reset:
			if function_reset:
				self.function_reset()
			else:
				self.reset()

	def reset(self):
		for idx in xrange(16):
			self[idx] = expr.UndefinedValue()
		self.reset_marked()

	def function_reset(self):
		self.reset()
		self[4] = expr.SymbolicValue('Arg1')
		self[5] = expr.SymbolicValue('Arg2')
		self[6] = expr.SymbolicValue('Arg3')
		self[7] = expr.SymbolicValue('Arg4')
		self.reset_marked()

	def reset_marked(self):
		for idx in xrange(16):
			self.marked[idx] = False

	def __getitem__(self, key):
		return self.reg[key]

	def __setitem__(self, key, value):
		self.reg[key] = value
		self.marked[key] = True

	def __str__(self):
		return '[' + ', '.join(map(str, self.reg)) + ']'

	def __copy__(self):
		return type(self)(no_reset=True, reg=self.reg, marked=self.marked)

class MemFile(Store):
	init_sp = 0xffffbfa0

	def __init__(self, no_reset=False, function_reset=False):
		super(MemFile, self).__init__()
		self.definite_mem = {}
		self.symbolic_mem = {}

	def reset(self):
		self.definite_mem = {}
		self.symbolic_mem = {}

	def function_reset(self):
		self.reset()

	def initialize_mem(self):
		pass

	def __getitem__(self, address):
		if address.can_eval():
			addr_val = address.eval()
			if addr_val in self.definite_mem:
				val = self.definite_mem[addr_val]
			else:
				val = expr.DereferenceOp(address)
		else:
			if address in self.symbolic_mem:
				val = self.symbolc_mem[address]
			else:
				val = expr.DereferenceOp(address)

		return val

	def __setitem__(self, address, val):
		if address.can_eval():
			self.definite_mem[address.eval()] = val
		else:
			self.symbolic_mem[address] = val

	def __str__(self):
		return '<definite_mem = %s, symbolic_mem = %s>' % (self.definite_mem, self.symbolic_mem)
