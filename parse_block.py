import ply.yacc

branch_points = ['BF', 'BF.S', 'BT', 'BT.S', 'BRA', 'BRAF', 'JMP']
tokens = branch_points + ['OTHER']

class InstTok(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value

class InstLexer(object):

	def __init__(self):
		pass

	def input(self, asm_list):
		self.asm_list = asm_list
		self.cursor = 0

	def token(self):
		if self.cursor == len(self.asm_list):
			return None
		else:
			line = self.asm_list[self.cursor]
			self.cursor += 1
			instruction = line.instruction.upper()
			if instruction in branch_points:
				type = instruction
			else:
				type = 'OTHER'

			return InstTok(type, line)

start = 'sequence'

def p_sequence(p):
	'''sequence : empty
	            | sequence pattern'''
	p[0] = p[1]
	if len(p) > 2 and p[2] is not None:
		p[0].extend(p[2])

def p_empty(p):
	'''empty : '''
	p[0] = []

def p_pattern(p):
	'''pattern : other_pattern
	           | single_branch_pattern'''
	p[0] = p[1]

def p_other_pattern(p):
	'''other_pattern : OTHER'''
	p[0] = None

#def p_single_branch_pattern(p):
#	'''single_branch_pattern : branch_cluster'''
#	pass

#def p_delay_branch(p):
#	'''delay_branch : 

parser = ply.yacc.yacc(outputdir='parse_block')
