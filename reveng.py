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
	proc_state = proc.SH7058(function_reset=True)
	test = asm.AsmListing.import_file('asm/test.asm')

	for c in test.code:
		proc_state.execute(c)

	print '\n'.join(['r%d=%s;' % (idx, str(proc_state.GPR[idx])) for idx in range(16) if proc_state.GPR.marked[idx]])

	return proc_state

if __name__ == '__main__':
	main()
