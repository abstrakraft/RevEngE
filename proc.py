import store

class ProcState(object):
	pass

class SH7058_State(ProcState):
	def __init__(self):
		self.GPR = store.RegFile(reset=True, function_init=True)
