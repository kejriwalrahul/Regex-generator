from DFA.DFA import DFA

model = DFA(["a","b"])
s = model.addState()
p = model.addState()
q = model.addState()
model.addTransition(s, p, "a")
model.addTransition(s, q, "b")
model.addTransition(p, 0, "a")
model.addTransition(p, 0, "b")
model.addTransition(q, 0, "a")
model.addTransition(q, 0, "b")
model.setStart(s)
model.addFinal(0)

# s = model.addState()
# model.addTransition(s, 0, "a")
# model.addTransition(s, 0, "b")

model.plot()
model.stats()

model = model.optimize()

raw_input()
model.plot()
model.stats()