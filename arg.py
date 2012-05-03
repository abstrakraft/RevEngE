import expr

class ArgVal(object):
	def __init__(self):
		pass

	def pre_effect(self, proc_state):
		raise Exception('abstract function')

	def post_effect(self, proc_state):
		raise Exception('abstract function')

	def store_value(self, proc_state, value):
		raise Exception('abstract function')

	def get_value(self, proc_state):
		raise Exception('abstract function')

class ArgInt(object):
	def __init__(self, value):
		if isinstance(value, basestring):
			if value[0] == '#':
				value = value[1:]
			self.value = int(value, 0)
		else:
			self.value = value

	def pre_effect(self, proc_state):
		pass

	def post_effect(self, proc_state):
		pass

	def store_value(self, proc_state, value):
		raise TypeError('invalid store to an int')

	def get_value(self, proc_state):
		return expr.NumericValue(self.value)

	def __str__(self):
		return str(self.value)

class ArgReg(object):
	def __init__(self, val):
		self.val = val.lower()
		self.mod = False
		self.indirect = False

	def set_pre_decrement(self):
		self.mod = '-'

	def set_post_increment(self):
		self.mod = '+'

	def set_indirect(self):
		self.indirect = True

	def pre_effect(self, proc_state):
		if self.mod == '-':
			proc_state[self.val] -= expr.NumericValue(1)

	def post_effect(self, proc_state):
		if self.mod == '+':
			proc_state[self.val] += expr.NumericValue(1)

	def store_value(self, proc_state, value):
		if self.indirect:
			proc_state.Mem[proc_state[self.val]] = value
		else:
			proc_state[self.val] = value

	def get_value(self, proc_state):
		tmp = proc_state[self.val]
		if self.indirect:
			return proc_state.Mem[tmp]
		else:
			return tmp

	def __str__(self):
		ret = ''
		if self.indirect:
			ret += '@'
		if self.mod == '-':
			ret += '-'
		ret += self.val
		if self.mod == '+':
			ret += '+'

		return ret

class ArgSum(object):
	def __init__(self, arg1, arg2):
		self.args = [arg1, arg2]

	def pre_effect(self, proc_state):
		map(lambda a: a.pre_effect(proc_state), self.args)

	def post_effect(self, proc_state):
		map(lambda a: a.post_effect(proc_state), self.args)

	def get_address(self, proc_state):
		return sum(map(lambda a: a.get_value(proc_state), self.args))

	def store_value(self, proc_state, value):
		proc_state.Mem[self.get_address(proc_state)] = value

	def get_value(self, proc_state):
		return proc_state.Mem[self.get_address(proc_state)]

	def __str__(self):
		return '(%s,%s)' % self.args
