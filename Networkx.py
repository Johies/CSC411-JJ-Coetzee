try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
import sympy as sy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


#-------------------------------------------------------------------------
# Extraction of Equations and Graph Creation
eqns = [line.strip() for line in open('eqns.txt')]
unkns = symbols([line.strip() for line in open('Unknowns.txt')])

G = nx.MultiDiGraph()

for unkn in unkns:
    for k in range(0,len(eqns)):
        eqn = sy.parsing.sympy_parser.parse_expr(eqns[k])
        if unkn in eqn:
            curr_node = k
            for j in range(k,len(eqns)):
                eqn2 = sy.parsing.sympy_parser.parse_expr(eqns[j])
                if unkn in eqn2:
                    next_node = j
                    if G.has_edge(curr_node,next_node):
                        G.add_edge(next_node,curr_node,weight=1,label=str(unkn))
                    else:
                        G.add_edge(curr_node,next_node,weight=0.5,label=str(unkn))


#-------------------------------------------------------------------
# Tarjan Algorithm and Symbolic Solving of Equations

Tarjan = nx.strongly_connected_components(G)

simu = []
Tarjan.reverse()

for curr in Tarjan:
    for now in curr:
        simu.append(eqns[now])
    soln = sy.solve(simu,unkns)
    print soln

print Tarjan


#--------------------------------------------------------------------
# Drawing of Graph

pos = nx.spring_layout(G)
sypy = sy.sympify(eqns)
sol = sy.solve(sypy,unkns)

print sol

nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos)

plt.axis('off')
plt.show()


