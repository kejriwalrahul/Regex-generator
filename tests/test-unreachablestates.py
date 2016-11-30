from DFA.DFA import DFA

model = DFA(["a","b"])
s = model.addState()
model.addTransition(s, 0, "a")
model.addTransition(s, 0, "b")
model.setStart(s)
model.addFinal(s)

s = model.addState()
model.addTransition(s, 0, "a")
model.addTransition(s, 0, "b")

model.plot()
model.stats()

model = model.optimize()

raw_input()
model.plot()
model.stats()