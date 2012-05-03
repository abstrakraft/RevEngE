import operator
import functools

binary_ops = (
	('AddOp', '+', operator.add,  '__add__'),
	('AndOp', '&', operator.and_, '__and__'),
	('MulOp', '*', operator.mul,  '__mul__'),
	('OrOp',  '|', operator.or_,   '__or__'),
	('SubOp', '-', operator.sub,  '__sub__'),
)

class Expr(object):
	def __init__(self):
		self.ref = False

	def mark(self):
		self.marked = True

	def __str__(self):
		raise Exception('Expr.__str__ is an abstract function')

	for (name, symbol, func, method) in binary_ops:
		def f(x, y, name=name):
			return globals()[name](x,y)
		vars()[method] = f
		#doesn't work as partial objects aren't recognized as functions, and aren't turned into bound methods
		#vars()[value_method] = functools.partial(lambda n,x,y: globals()[n](x,y), name)

class Value(Expr):
	def __init__(self, val):
		super(Value, self).__init__()
		self.val = val

	def __str__(self):
		return str(self.val)

class SymbolicValue(Value):
	def __str__(self):
		return self.val

	def eval(self):
		raise Exception('Can\'t eval symbolic')

	def can_eval(self):
		return False

class UndefinedValue(SymbolicValue):
	def __init__(self):
		super(UndefinedValue, self).__init__('Undefined')

class NumericValue(Value):
	def __str__(self):
		if isinstance(self.val, int):
			return '0x%x' % self.val
		elif isinstance(self.val, float):
			return '%g' %self.val

	def eval(self):
		return self.val

	def can_eval(self):
		return True

class UnaryOp(Expr):
	def __init__(self, op1):
		super(UnaryOp, self).__init__()
		self.op1 = op1

	def __str__(self):
		return self.format % self.op1

	def eval(self):
		return self.func(self.op1)

	def can_eval(self):
		return self.func and self.op1.can_eval()

class BinaryOp(Expr):
	def __init__(self, op1, op2):
		super(BinaryOp, self).__init__()
		self.op1 = op1
		self.op2 = op2

	def __str__(self):
		return self.format % (self.op1, self.op2)

	def eval(self):
		return self.func(self.op1, self.op2)

	def can_eval(self):
		return self.func and self.op1.can_eval() and self.op2.can_eval()

for (name, symbol, func, method) in binary_ops:
	vars()[name] = type(name, (BinaryOp,), {'format': '(%s ' + symbol + ' %s)', 'func': func})

class SignExtendByteOp(UnaryOp):
	format = "exts.b(%s)"
	func = functools.partial(operator.and_, 0xff)

class SignExtendWordOp(UnaryOp):
	format = "exts.w(%s)"
	func = functools.partial(operator.and_, 0xffff)

class DereferenceOp(UnaryOp):
	format = "*(%s)"
	func = None
