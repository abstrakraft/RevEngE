import store

class ProcState(object):
	pass

class SH7058_State(ProcState):
	def __init__(self):
		self.GPR = store.RegFile(reset=True, function_init=True)
		self.Mem = store.MemFile()

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
