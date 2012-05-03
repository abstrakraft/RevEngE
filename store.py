import collections
import expr

class Store(object):
	def __init__(self):
		super(Store, self).__init__()

class RegFile(Store):
	def __init__(self, reset=False, function_init=False):
		super(RegFile, self).__init__()
		self.reg = [expr.UndefinedValue() for r in xrange(16)]

		if reset:
			self.reset_init()
		if function_init:
			self.function_init()

	def reset_init(self):
		for idx in xrange(16):
			self[idx] = expr.UndefinedValue()

	def function_init(self):
		self[4] = expr.SymbolicValue('Arg1')
		self[5] = expr.SymbolicValue('Arg2')
		self[6] = expr.SymbolicValue('Arg3')
		self[7] = expr.SymbolicValue('Arg4')

	def __getitem__(self, key):
		return self.reg[key]

	def __setitem__(self, key, value):
		self.reg[key] = value

	def __str__(self):
		return '[' + ', '.join(map(str, self.reg)) + ']'

class MemFile(Store):
	init_sp = 0xffffbfa0

	def __init__(self):
		self.definite_mem = {}
		self.symbolic_mem = {}

	def __getitem__(self, address):
		if address.can_eval():
			addr_val = address.eval()
			if addr_val in self.definite_mem:
				val = self.definite_mem[addr_val]
			else:
				val = expr.DereferenceOp(addr_val)
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

	def initialize_mem(self):
		pass

	def __str__(self):
		return '<definite_mem = %s, symbolic_mem = %s>' % (self.definite_mem, self.symbolic_mem)
