from evalgraph.nodes import Node, GraphEvaluator

GraphEvaluator.verbose = True

a = Node('a', lambda: 1)
b = Node('b', lambda: 2)
c = Node('c', lambda: a() + b())
d = Node('d', lambda: c() + a())
e = Node('e', lambda: c() + d())
f = Node('f', lambda: b())
g = Node('g', lambda: f()+e())
#d = Node('d', lambda: g())
print(g())
