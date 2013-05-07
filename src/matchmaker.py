#!/usr/bin/python

#I was going to document this in a way that was as generic as possible
#But that was way troublesom. Let's just refer to the things as they are in the game
import sys
import re

#Computation Functions

#Optimality, defined as: number of nodes that are not connected to anyone else
# Due to our graph's particularity, that is reeeeeally simple
def optimality(V,E):
    return len(V) - 2*len(E)

#Compute cardinality of vertices in graph G = (V,E)
# V: vertex set
# E: edge set 
# Return: a dictionary of cardinality values for each v in V
def cardinality(V,E):
    C = {}
    for v in V:
        C[v] = 0
    
    for e in E:
        C[e[0]] += 1
        C[e[1]] += 1

    return C
	
#Solve the problem for graph G = (V,E)
# Return: the solution graph (Vs, Es)
def solve_heurist1(V,E):
    Vt = list(V)
    Et = list(E)
    
    Vs = []
    Es = []
    
    #Initial purge
    card = cardinality(Vt,Et)
    print card
    for v in [k for k,v in card.iteritems() if v == 0]:
        Vs.append(v)
        card.pop(v)
        V.remove(v)
    
    while len(Vt) > 0:
        v1 = pick(card)
        Vt.remove(v1)
        Vs.append(v1)
        
        for v2 in Vt:
            if len([e for e in Et if e == (v1,v2) or e == (v2,v1)]) > 0:
                Vs.append(v2)
                Es.append((v1,v2))
                Vt.remove(v2)
                for e in [(a,b) for a,b in Et if a == v1 or b == v1 or a == v2 or b == v2]:
                    Et.remove(e)
        
        card = cardinality(Vt,Et)
        print card
        for v in [k for k,v in card.iteritems() if v == 0]:
            Vs.append(v)
            card.pop(v)
            Vt.remove(v)

    return V,Es

#Pick vertex from cardinality set
def pick(C):
    print sorted(C, key=C.get)
    return sorted(C, key=C.get)[0]
    
dataset = sys.argv[1]
print dataset

pairs = open(dataset+"/pairs","r")
query = open(dataset+"/query","r")

#Compatibility Set
# The professions, laid out in compatible pairs
compatibility = []

#Query Set
# The set of vertices of the query graph
query_set = []

#Query Graph
# The set of edges of the query graph; based on the profession graph applied over the query set
query_graph = []

#Solution
# Ta-da!
solution=[]

#Read pairs, generate compatibility set
for pair in pairs.readlines():
    T = tuple(str(P) for P in re.findall("[A-Za-z ]+",pair))
    _T = T[1], T[0]
    if compatibility.count(T) + compatibility.count(_T) == 0:
        compatibility.append(T)
        
print compatibility

#Read query, generate query set
for q in query.readlines():
    query_set.append(q.strip())

query_set = list(enumerate(query_set))

print query_set

#Apply compatibility set on query, generate the query graph
for P in compatibility:
    v1,v2 = P
    for A in [(i,Q) for i,Q in query_set if Q == v1]:
        for B in [(i,Q) for i,Q in query_set if Q == v2]:
            query_graph.append((A,B))

print query_graph
print cardinality(query_set, query_graph)

print "Start Solution:"
solution = solve_heurist1(query_set, query_graph)
print solution
print optimality(solution[0], solution[1])