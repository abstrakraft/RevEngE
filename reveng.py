import asm
import proc

class Function(object):
	def __init__(self, code):
		self.code = code

class Block(object):
	def __init__(self, code, entries):
		self.code = code
		self.entries = entries

def main():
	#Alex = asm.AsmListing.import_file('alex_disassembly.asm')
	#main_entry = (Alex[0].value << 16) | Alex[1].value
	proc_state = proc.SH7058_State()
	test = asm.AsmListing.import_file('test.asm')

	for c in test.code:
		c.execute(proc_state)

	return proc_state
