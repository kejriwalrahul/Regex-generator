from DFA.DFA import DFA

# Currently used alphabet for DFAs
alpha = ["a", "b"]

# Obtain input strings
stringSet = []
while True:
	try:
		s = raw_input()
		stringSet.append(s)
	except EOFError:
		break

# Build DFA for accepting all given strings
resDFA = DFA(alpha)
for s in stringSet:
	resDFA += DFA(alpha, s)

# Optimize using state minimization
resDFA = resDFA.optimize()

# Plot resultant DFA and show stats
resDFA.plot()
resDFA.stats()

# Validation Test
print "\n\nValidation: "
print len(stringSet)
for s in stringSet:
	print resDFA.accepts(s)