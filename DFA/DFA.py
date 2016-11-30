from graph import graph

"""
Basic DFA implementation:
1. Can build a basic DFA from strings 
2. Allows OR & AND using subset construction
3. Can plot current DFA
4. Can do state optimization
5. Can generate regex from DFA
"""
class DFA:

	"""
	Initialize a basic DFA that never accepts
	"""
	def __init__(self, sigma, string= ""):
		
		# Build trivial one-state DFA 
		self.numStates = 1
		self.sigma = sigma
		self.s = 0
		self.F = {}
		
		self.delta = {}
		for c in sigma:
			self.delta[(0,c)] = 0

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

		self.F[currState] = 'final'

	"""
	Using a wrapper on top of graphviz package to plot the DFA 
	"""
	def plot(self):
		currPlot = graph()

		for i in range(self.numStates):
			if i == self.s:
				currPlot.addNode(i, "start")
			elif i in self.F:
				currPlot.addNode(i, "final")
			else:
				currPlot.addNode(i)

		for edge in self.delta:
			_from = edge[0]
			_on   = edge[1]
			_to   = self.delta[edge]

			currPlot.addEdge(_from, _to, _on)

		currPlot.render()

	"""
	Overloading + operator to do OR of two DFAs using subset construction
	"""
	def __add__(self, other):
		
		# If alphabets are different, error DFA
		if(set(self.sigma) != set(other.sigma))
			return DFA([a,b])

		res = DFA(self.sigma)

	"""
	Overloading * operator to do AND of two DFAs using subset construction
	"""
	def __mul__(self, other):
		pass

	"""
	Manual functions: 
	Adds a state to DFA and returns its id
	"""
	def addState(self):
		newState = self.numStates
		self.numStates += 1
		return newState

	"""
	Manual functions: 
	Adds a transition to DFA
	"""		
	def addTransition(self, _from, _to, _on):
		self.delta[(_from, _on)] = _to

	"""
	Manual functions: 
	Adds a final state to DFA
	"""
	def addFinal(self, f):
		self.F[f] = 'final'

	"""
	Manual functions: 
	Sets start state of DFA
	"""
	def setStart(self, s):
		self.s = s
