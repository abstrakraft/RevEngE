import asm
import proc
#import parse_block

class Block(object):
	def __init__(self, address, code, outflows):
		self.address = address
		self.code = code
		self.outflows = outflows

delayed_bp = ['bf.s', 'bt.s', 'bra']
nondelayed_bp = ['bf', 'bt']
bp = delayed_bp + nondelayed_bp
indeterminant_bp = ['braf', 'bsrf', 'jmp']

def blockize(code_listing):
	#Separate code into blocks
	#A block is a piece of code that _always_ executes as a unit (within the context of a thread, anyway, i.e. barring interrupts)
	#A block is, therefore, ended by a branch/jmp instruction, and begins at the top of a function, or at the destination of local branch/jump

	#Annotated Code Listing, Mapping
	ACL = [(c, [], []) for c in code_listing.code]
	ACM = {}
	for c in ACL:
		ACM[c[0].address] = c

	#TODO: detect non-code - check to see if code is reachable before parsing
	#TODO: handle delay slots
	for cdx in xrange(len(ACL)):
		(c, inflows, outflows) = ACL[cdx]
		if c.instruction in bp:
			#TODO: this may not be the best way to access the value, but works for now
			branch_dest = c.args[0].address.val
			outflows.append(branch_dest)
			ACM[branch_dest][1].append(c.address)
			if c.instruction != 'bra':
				#conditional branches
				#TODO: handle last instruction condition somehow
				nobranch_dest = ACL[cdx+1][0].address
				outflows.append(nobranch_dest)
				ACM[nobranch_dest][1].append(c.address)
		elif c.instruction in indeterminant_bp:
			#TODO: currently ignoring indeterminant_bp's
			raise ValueError("indeterminant_bp's not yet implemented")

	block_start = [0] + [cdx for cdx in xrange(1, len(ACL)) if (len(ACL[cdx][1]) > 0) or (len(ACL[cdx-1][2]) > 0)] + [len(ACL)]
	blocks = []
	for bdx in xrange(len(block_start)-1):
		outflows = ACL[block_start[bdx+1]-1][2]
		outflows.sort()
		if (bdx < len(block_start)-2) and (len(outflows) == 0):
			outflows.append(ACL[block_start[bdx+1]][0].address)
		blocks.append(Block(code_listing[block_start[bdx]].address, code_listing[block_start[bdx]:block_start[bdx+1]], outflows))

	return blocks

class Function(object):
	def __init__(self, code):
		self.code = code
		self.block_tree = analyze()

	#currently dead code
	def old_analyze():
		control_points = []
		indeterminant = False
		code_map = {}
		for c in code:
			code_map[c.address] = c

		# Find control points
		for c in code:
			if c.instruction == 'rts':
				control_points.append((c, c.address, None))
			elif c.instruction in bp:
				src_address = c.address
				dst_address = c.args[0].get_address(None).val
				control_points.append((c, src_address, dst_address))
				if (c.instruction == 'bra') and (dst_address <= src_address):
					#Test for infinite loop
					break
					#infinite_loop = True
					#for (inst, s_addr, d_addr) in control_points[:-1]:
					#	if s_addr >= dst_address:
					#		infinite_loop = False
					#		break
					#if infinite_loop:
					#	break

			elif c.instruction in indeterminant_bp:
				indeterminant = True
				#Can't do anything with this now
				#control_points.append((c, c.address, None))

		#Split into blocks
		control_points.sort(key=lambda cp: (min(cp[1:]), max(cp[1:])), reverse=True)

		boundary = None
		for (branch, src_address, dst_address) in control_points:
			if src_address < dst_address:
				start_address = src_address
				end_address = dst_address
				head_branch = True
			else:
				start_address = dst_address
				end_address = src_address
				head_branch = False #this is a tail branch
			if boundary and ((boundary[0] < start_address) or (end_address < boundary[1])):
				raise ValueError('crossed blocks')
			else:
				boundary = (start_address, end_address)

			delay = branch.instruction in delayed_bp
			if head_branch:
				block_code = [c for c in code if (start_address + (delay and 2 or 0)) < c.address <= end_address]
				code = [c for c in code if c.address < start_address or (delay and (c.address == start_address+2))] + \
				       [Block(branch, start_address, end_address, block_code)] + \
				       [c for c in code if end_address < c.address]
			else:
				block_code = [c for c in code if (start_address <= c.address < end_address) or (delay and (c.address == end_address+2))]
				code = [c for c in code if c.address < start_address] + \
				       [Block(branch, start_address, end_address, block_code)] + \
				       [c for c in code if (end_address + (delay and 2 or 0)) < c.address]

		return Function(code)

def main():
	#Alex = asm.AsmListing.import_file('alex_disassembly.asm')
	#main_entry = (Alex[0].value << 16) | Alex[1].value
	proc_state = proc.SH7058(function_reset=True)
	test = asm.AsmListing.import_file('asm/test2.asm')

	import pdb; pdb.set_trace()
	print blockize(test.code)

	#print parse_block.parser.parse(test.code, lexer=parse_block.InstLexer())

	output = []

	for c in test.code:
		r = proc_state.execute(c)
		if r:
			output.extend(r)

	print '\n'.join(output + ['r%d=%s;' % (idx, str(proc_state.GPR[idx])) for idx in range(16) if proc_state.GPR.marked[idx]])

	return proc_state

if __name__ == '__main__':
	main()
