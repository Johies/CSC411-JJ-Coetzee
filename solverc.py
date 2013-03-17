import networkx as nx
import sympy as sy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


def solvr():
    eqns = [sy.parsing.sympy_parser.parse_expr(line) for line in open('eqns.txt')]
    unkns = [x for x in set.union(*(eq.atoms() for eq in eqns)) if x.is_Symbol]

    G = nx.MultiDiGraph()

    for unkn in unkns:
        for curr_node in range(0,len(eqns)):
            if unkn in eqns[curr_node]:
                for next_node in range(curr_node,len(eqns)):
                    if unkn in eqns[next_node]:
                        if G.has_edge(curr_node,next_node):
                            G.add_edge(next_node,curr_node,weight=1,label=str(unkn))
                        else:
                            G.add_edge(curr_node,next_node,weight=0.5,label=str(unkn))

    Tarjan = nx.strongly_connected_components(G)

    simu = []
    sol = {}
    Tarjan.reverse()
    mul_var = []

    for curr in Tarjan:
        if len(curr) == 1:
            for now in curr:
                tel = 0
                eq = eqns[now]
                var = unkns[now]     #Find current unknown - not robust at all
                solv = solve(eq,var)
                eqns[now].replace(var,solv[0])
                val = solv[0]
                for repl in eqns:    #Replace unknowns with values in equations
                    repl = repl.subs(var,val)
                    eqns[tel] = repl
                    tel +=1
                sol[var] = solv[0]
        elif len(curr) > 1:
            tel = len(sol)
            for now in curr:
                simu.append(eqns[now])
                mul_var.append(unkns[now])
            soln = sy.solve(simu,unkns)
            
            sol = dict(sol.items() + soln.items())
    for key in sol:
        sol[key] = str(float(sol.get(key)))    
    return sol