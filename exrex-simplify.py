import exrex

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

print exrex.simplify("|".join(stringSet))