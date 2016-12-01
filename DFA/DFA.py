from graph import graph
from random import shuffle

"""
Basic DFA implementation:

1. Can build a basic DFA from strings 
2. Allows building DFA manually 
3. Allows OR & AND using subset construction
4. Can plot current DFA
5. Can do state optimization
6. Can generate regex from DFA
7. Allows toString of DFA for human readable form of DFA
8. Allows small DFA stats summary
"""

class DFA:

	"""
	Initialize a basic DFA that never accepts
	"""
	def __init__(self, sigma, string= "", clean=False):
		
		# If clean, leave uninitialized
		if clean:
			self.numStates = 0
			self.sigma = sigma
			self.s = 0
			self.F = {}
			self.delta = {}
		else:
			# Build trivial one-state DFA 
			self.numStates = 1
			self.sigma = sigma
			self.s = 0
			self.F = {}
			
			# Build error state transitions
			self.delta = {}
			for c in sigma:
				self.delta[(0,c)] = 0

			# Build from string if reqd
			if string != "":
				self.buildFromString(string)


	"""
	Runs DFA on the string param and returns true if the string is accepted by it
	"""
	def accepts(self, string):
		currState = self.s
		for ch in string:
			if (currState, ch) in self.delta: 
				currState = self.delta[(currState, ch)]
			else:
				raise AttributeError('Undefined transition from ' + str(currState) + ' on ' + ch + "!")

		if currState in self.F:
			return True
		else:
			return False

		
	"""
	Builds a naive DFA from given string
	"""
	def buildFromString(self, string):
		self.s = self.numStates
		self.numStates += 1

		currState = self.s
		for ch in string:
			for alpha in self.sigma:
				if alpha != ch:
					self.delta[(currState, alpha)] = 0
				else:
					self.delta[(currState, alpha)] = self.numStates

			currState = self.numStates
			self.numStates += 1

		# Process final state
		self.F[currState] = 'final'
		for alpha in self.sigma:
			self.delta[(currState, alpha)] = 0


	"""
	Using a wrapper on top of graphviz package to plot the DFA 
	"""
	def plot(self):
		currPlot = graph()

		for i in range(self.numStates):
			if i == self.s:
				currPlot.addNode(i, "start(" + str(i) +")")
			elif i in self.F:
				currPlot.addNode(i, "final(" + str(i) +")")
			else:
				currPlot.addNode(i)

		for edge in self.delta:
			_from = edge[0]
			_on   = edge[1]
			_to   = self.delta[edge]

			currPlot.addEdge(_from, _to, _on)

		currPlot.render()


	"""
	Builds a new DFA from 2 given DFAs using subset construction
	Final states are left to caller for implementation
	"""
	def subset_construct(self, other):

		# If alphabets are different, error DFA
		if set(self.sigma) != set(other.sigma):
			return DFA([a,b])

		# Build State translation dictionary 
		translation = {}
		curr = 0
		for q1 in range(self.numStates):
			for q2 in range(other.numStates):
				translation[(q1, q2)] = curr
				curr += 1

		# Build new DFA and clean transitions
		res = DFA(self.sigma, clean=True)

		# Update State set and start state
		res.numStates = self.numStates * other.numStates
		res.s = translation[(self.s, other.s)]

		# Build transition matrix 
		for q1 in range(self.numStates):
			for q2 in range(other.numStates):
				currState = translation[(q1, q2)]
				for c in self.sigma:
					res.delta[(currState, c)] = translation[(self.delta[(q1,c)], other.delta[(q2, c)])]

		return res, translation


	"""
	Overloading + operator to do OR of two DFAs using subset construction
	"""
	def __add__(self, other):
		resultant, translation = self.subset_construct(other)

		# Update Final state set
		for q1 in self.F:
			for q2 in range(other.numStates):
				resultant.F[translation[(q1, q2)]] = 'final'

		for q1 in range(self.numStates):
			for q2 in other.F:
				resultant.F[translation[(q1, q2)]] = 'final'

		return resultant


	"""
	Overloading * operator to do AND of two DFAs using subset construction
	"""
	def __mul__(self, other):
		resultant, translation = self.subset_construct(other)

		# Update Final state set
		for q1 in self.F:
			for q2 in other.F:
				resultant.F[translation[(q1, q2)]] = 'final'

		return resultant


	"""
	Generate equivalent DFA by removing unreachable states
	"""
	def rmUnreachable(self):

		# Initialize reachable state set
		reachable = set([]);
		new_reachable = set([self.s]);
		
		# Compute reachable states
		while len(new_reachable):
			reachable = reachable.union(new_reachable)
			iterate_over = new_reachable
			new_reachable = set([])

			for q in iterate_over:
				for c in self.sigma:
					newS = self.delta[(q,c)] 
					if newS not in reachable:
						new_reachable.add(newS)

		# Build translation matrix
		translation = {}
		curr = 0
		for q in reachable:
			translation[q] = curr
			curr += 1

		# Build new DFA based on computed translation
		reduced = DFA(self.sigma, clean=True)
		
		# Initialize state set and start set
		reduced.numStates = len(translation)
		reduced.s 		  = translation[self.s]

		# Initialize final states
		for f in self.F:
			if f in translation:
				reduced.F[translation[f]] = 'final'
		
		# Initialize transition matrix
		for q in range(self.numStates):
			if q not in translation:
				continue

			for c in self.sigma:
				reduced.delta[(translation[q], c)] = translation[self.delta[(q,c)]]

		return reduced


	"""
	Generate equivalent DFA by merging equivalent states
	"""
	def mergeEquivalent(self):
		# Mark all pairs as equivalent initially
		notEquivalent = [[0 for j in range(self.numStates)] for i in range(self.numStates)]

		# Mark all pairs of q1, q2 as not equivalent where
		# q1 not in F and q2 in F and vice-versa
		for q1 in range(self.numStates):
			if q1 in self.F:
				continue

			for q2 in self.F:
				notEquivalent[q1][q2] = 1
				notEquivalent[q2][q1] = 1

		# Repeat till convergence:
		flag = True
		while flag:
			flag = False
			# Iterate over all unique (q1,q2) pairs
			for q1 in range(self.numStates):
				for q2 in range(q1+1, self.numStates):
					# If already non-equivalent, no need to process
					if notEquivalent[q1][q2]:
						continue

					# If possibly equivalent, try to find distinguishing letter
					for c in self.sigma:
						if notEquivalent[self.delta[(q1, c)]][self.delta[(q2, c)]]:
							notEquivalent[q1][q2] = 1
							notEquivalent[q2][q1] = 1
							flag = True
							break

		# Genereate translation
		curr = 0
		translation = {}
		for q in range(self.numStates):
			if q in translation:
				continue

			translation[q] = curr
			for q2 in range(q+1, self.numStates):
				if not notEquivalent[q][q2]:
					translation[q2] = curr

			curr += 1

		# Build new DFA based on computed translation
		reduced = DFA(self.sigma, clean=True)
		
		# Initialize state set and start set
		reduced.numStates = curr
		reduced.s 		  = translation[self.s]

		# Initialize final states
		for f in self.F:
			reduced.F[translation[f]] = 'final'
		
		# Initialize transition matrix
		for q in range(self.numStates):
			for c in self.sigma:
				reduced.delta[(translation[q], c)] = translation[self.delta[(q,c)]]

		return reduced


	"""
	Performs state minimization and returns minimized DFA 
	"""
	def optimize(self):
		resultant = self.rmUnreachable()
		resultant = resultant.mergeEquivalent()
		return resultant


	"""
	Returns regex equivalent of the DFA
	"""
	def toRE(self):

		# B array initialize
		B = []
		for i in range(self.numStates):
			if i in self.F:
				B.append(regex.epsilon())
			else:
				B.append(regex.empty())

		# A array initialization
		A = [["" for j in range(self.numStates)] for i in range(self.numStates)]
		for i in range(self.numStates):
			for j in range(self.numStates):
				cset = []
				for c in self.sigma:
					if self.delta[(i,c)] == j:
						cset.append(c)
				A[i][j] = regex.options(cset)

		# Build solver order

		# Solve iteratively
		x = range(self.numStates-1, -1, -1)
		shuffle(x)
		for n in x:
			"""
			For debugging: 
			print "\n\nState:", n
			print "A: \n", A
			print "B: \n", B
			"""
			B[n] = regex.concat(regex.star(A[n][n]), B[n])
			for j in range(self.numStates):
				A[n][j] = regex.concat(regex.star(A[n][n]), A[n][j])
			for i in range(self.numStates):
				B[i] = regex.alt(B[i], regex.concat(A[i][n],  B[n])) 
				for j in range(self.numStates):
					A[i][j] = regex.alt(A[i][j], regex.concat(A[i][n], A[n][j])) 

		return B[self.s]


	"""
	Returns some statistics regarding the DFA
	"""
	def stats(self):
		print "\nDFA Statistics: "
		print "No. of States = " , self.numStates
		print "No. of Final States = ", len(self.F)


	"""
	Prints the DFA in sort of human-readaable form
	"""
	def toString(self):
		s  = "NumStates: "   + str(self.numStates) + "\n"
		s += "Start State: " + str(self.s) + "\n"
		s += "Final State: " + str(self.F.keys()) + "\n"
		s += "Alphabet: "    + str(self.sigma) + "\n"
		s += "Transition Matrix: " + str(self.delta) + "\n"

		return s


	"""
	Manual Functions ahead:
	Proceed with caution

	For complete manual control on building DFA
	DFA correctness is user responsibility
	"""


	"""
	Manual function: 
	Adds a state to DFA and returns its id
	"""
	def addState(self):
		newState = self.numStates
		self.numStates += 1
		return newState


	"""
	Manual function: 
	Adds a transition to DFA
	"""		
	def addTransition(self, _from, _to, _on):
		self.delta[(_from, _on)] = _to


	"""
	Manual function: 
	Adds a final state to DFA
	"""
	def addFinal(self, f):
		self.F[f] = 'final'


	"""
	Manual function: 
	Sets start state of DFA
	"""
	def setStart(self, s):
		self.s = s


"""
Class for RE building 
Contains a few generic RE building methods
"""
class regex:

	@staticmethod
	def epsilon():
		return ""

	@staticmethod
	def empty():
		return None

	@staticmethod
	def options(cset):
		if not len(cset):
			return regex.empty()

		if len(cset) == 1:
			return cset[0]

		return "[" + "".join(cset) + "]"

	@staticmethod
	def alt(l,r):
		# Handle epsilon
		if l == None:
			return r
		if r == None:
			return l

		if l == "":
			return "(" + r + ")?"
		if r == "":
			return "(" + l + ")?"

		return  "(" + l + "|" + r + ")"

	@staticmethod
	def star(l):
		if l == "" or l == None:
			return ""

		return "(" + l + ")*"

	@staticmethod
	def concat(l,r):
		# Handle epsilon
		if l == None or r == None:
			return None

		return  l + r