import ply.lex
import ply.yacc

import arg

tokens = ('UN_OP', 'BIN_OP', 'TYPE_SPEC', 'INTEGER', 'GENREG', 'PC', 'GBR')
literals = '().,@+-'
t_ignore = ' \t'

t_UN_OP = r'(movt)|(cmp/(pl)|(pz))|(dt)|(tas.b)|(rotr|(cl)|(cr))|(shal|r)|(shll|r(2|8|(16))?)'
t_BIN_OP = r'(mova?)|(swap)|(xtrct)|(add(c|v)?)|(cmp/(eq)|(hs)|(ge)|(hi)|(gt)|(str))|(div1|(0s)|s|u)|(exts|u)|(mac)|(mul(s|u)?)|(negc?)|(sub(c|v)?)|' + \
	       r'(and)|(not)|(or)|(tst)|(xor)|(ldc|s)|(stc|s)'
t_TYPE_SPEC = r'b|w|l'

start = 'statement'

def t_INTEGER(t):
	'''(\#[0-9]*)|(0x[0-9a-fA-F]*)'''
	t.value = arg.ArgInt(t.value)
	return t

def t_GENREG(t):
	'''[rR]1?[0-9]'''
	t.value = arg.ArgReg(t.value)
	return t

def t_PC(t):
	'''(pc)|(PC)'''
	t.value = arg.ArgReg(t.value)
	return t

def t_GBR(t):
	'''(gbr)|(GBR)'''
	t.value = arg.ArgReg(t.value)
	return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def p_statement(p):
	'''statement : bin_op_statement'''
	p[0] = p[1]

def p_bin_op_statement(p):
	'''bin_op_statement : bin_op_spec src ',' dst'''
	p[0] = p[1]
	p[0].append((p[2], p[4]))

def p_bin_op_spec(p):
	'''bin_op_spec : BIN_OP '.' TYPE_SPEC
	               | BIN_OP'''
	if len(p) == 4:
		p[0] = [p[1], p[3]]
	else:
		p[0] = [p[1], None]

def p_dst(p):
	'''dst : indirect_reg
	       | direct_reg
	       | sum'''
	p[0] = p[1]

def p_src(p):
	'''src : direct_reg
	       | indirect_reg
	       | sum
	       | INTEGER'''
	p[0] = p[1]

def p_indirect_reg(p):
	'''indirect_reg : '@' GENREG
	                | '@' mod_reg'''
	p[0] = p[2]
	p[0].set_indirect()

def p_direct_reg(p):
	'''direct_reg : raw_reg
	              | mod_reg'''
	p[0] = p[1]

def p_raw_reg(p):
	'''raw_reg : GENREG
	           | PC
	           | GBR'''
	p[0] = p[1]

def p_mod_reg(p):
	'''mod_reg : pre_dec_register
	           | post_inc_register'''
	p[0] = p[1]

def p_pre_dec_register(p):
	'''pre_dec_register : '-' GENREG'''
	p[0] = p[2]
	p[0].set_pre_decrement()
	

def p_post_inc_register(p):
	'''post_inc_register : GENREG '+' '''
	p[0] = p[1]
	p[0].set_post_increment()

def p_sum(p):
	'''sum : '@' '(' INTEGER ',' raw_reg ')'
	       | '@' '(' GENREG ',' GENREG ')'
	       | '@' '(' GENREG ',' GBR ')' '''
	p[0] = ArgSum(p[3], p[5])


ply.lex.lex()
asm_parser = ply.yacc.yacc()

#print parser.parse('mov.w R1,@R2')
