import collections
import functools

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

class MemFile(Store):
	init_sp = 0xffffbfa0

	def __init__(self):
		self.mem = collections.defaultdict(functools.partial(expr.UndefinedValue()))

	def __getitem__(self, key):
		return self.mem[key]

	def __setitem__(self, key, value):
		self.mem[key] = value
