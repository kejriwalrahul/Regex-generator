import graphviz

class Node:
    def __init__(self,key):
    	self.key = key
        # store tuples of form(oppVal, wt)
    	self.adjList = []

class graph(graphviz.Digraph):

    def __init__(self, directed = 1):
        super(graph, self).__init__(comment="Graph State", engine="neato", format="svg")
        self.nodes = {}
        self.directed = directed

    def __getitem__(self,val):
        return self.nodes[val]
        
    def addNode(self, val, label = ""):
        if label != "":
            super(graph, self).node(str(val), label=label)
        else:
            super(graph, self).node(str(val), label=str(val))
        self.nodes[val] = Node(val)

    def addEdge(self, n1, n2, wt = 1):
        super(graph, self).edge(str(n1), str(n2), label = str(wt))
        if self.directed == 0:
            self[n1].adjList.append((n2,wt))
            self[n2].adjList.append((n1,wt))
        else:
            self[n1].adjList.append((n2,wt))

    def render(self):
        super(graph, self).render('graph-state', view=True)