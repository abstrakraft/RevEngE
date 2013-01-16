def main():
	fm = FlowMatch()

class FlowMatch(object):
	#('outflows')
	patterns = {'infinite loop': ('A',),
				'if': ('BC', 'C', ''),
				'if-else': ('BC', 'D', 'D', ''),
				'do-while': ('AB', ''),
				'skip': ('C', '', ''),
				#('inflows', 'outflows')
				#'infinite loop': (('A', 'A')),
				#'if': (('', 'BC'), ('A', 'C'), ('A', '')),
				#'if-else': (('', 'BC'), ('A', 'D'), ('A', 'D'), ('BC', '')),
				#'do-while': (('', 'B'), ('AB', 'BC'), ('B', '')),
				}

	def __init__(self):
		self.stack = []

	def push(self, val):
		self.stack.append(val)

	def pop(self):
		return self.stack.pop()

	def tail_parse(self):
		#import pdb; pdb.set_trace()
		match = False
		for (name, outflows) in self.patterns.items():
			if len(self.stack) < len(outflows):
				continue
			substack = self.stack[-len(outflows):]
			#bind positional block symbols to candidate block address
			symbols = dict([(chr(ord('A') + x), substack[x][0]) for x in xrange(len(outflows))])
			match = (name, symbols)
			for cursor in xrange(len(outflows)):
				#verify pattern symbols against block outflows
				if cursor != len(outflows)-1:
					if len(outflows[cursor]) != len(substack[cursor][1]):
						match = False
						break
					for (s, v) in zip(outflows[cursor], substack[cursor][1]):
						if (s not in symbols) or (symbols[s] != v):
							match = False
							break
					if not match: break
				else:
					#last block is special - the block can have extra outflows besides those specified
					#in the pattern, but those specified in the pattern must match the symbol dict
					#and any other outflows must not match existing symbols

					#TODO: really it's simpler than this - if the pattern specifies nothing for the final block,
					#then that block's outflows aren't relevant to the pattern (as long as they don't match existing symbols)
					#If the pattern does specify _any_ outflows, they must all match as for any other block.  This condition
					#should only arise for infinite loops.

					final_outflows = list(substack[cursor][1])
					for s in outflows[cursor]:
						v = symbols[s]
						if v not in final_outflows:
							match = False
							break
						else:
							final_outflows.remove(v)
					if not match: break

					for v in final_outflows:
						if v in symbols.values():
							match = False
							break
			if match:
				break
		return match

	def bind_symbols(bound_symbols, new_bindings):
		for (k,v) in new_bindings:
			bv = bound_symbols.get(k)
			if bv is None:
				bound_symbols[k] = v
			elif bv != v:
				return False
		return True

if __name__ == '__main__':
	main()
