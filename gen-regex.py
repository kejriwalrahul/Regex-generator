from DFA.DFA import DFA

alpha = ["a", "b"]
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

# resDFA = resDFA.optimize()
resDFA.plot()
resDFA.stats()

# Validation Test
print len(stringSet)
for s in stringSet:
	print resDFA.accepts(s)