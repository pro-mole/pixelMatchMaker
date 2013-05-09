#!/usr/bin/python

#I was going to document this in a way that was as generic as possible
#But that was way troublesom. Let's just refer to the things as they are in the game
import sys
import re
import random

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

#Get edge count for vertex or vertices
def edge_count(E,A,B=None):
    if (B == None):
        return len([e for e in E if e[0] == A or e[1] == A])
    else:
        return len([e for e in E if e == (A,B) or e == (B,A)])

#Solve the problem for graph G = (V,E)
# Return: the solution graph (Vs, Es)
def solve_heurist1(V,E):
    Vt = list(V)
    Et = list(E)
    
    Vs = []
    Es = []
    
    #Initial purge
    card = cardinality(Vt,Et)
    #print card
    
    for v in [k for k,v in card.iteritems() if v == 0]:
        Vs.append(v)
        card.pop(v)
        Vs.remove(v)
    
    while len(Vt) > 0:
        v1 = pickrandom(card)
        Vt.remove(v1)
        Vs.append(v1)
        
        for v2 in Vt:
            if edge_count(Et,v1,v2) > 0:
                Vs.append(v2)
                Es.append((v1,v2))
                Vt.remove(v2)
                for e in [(a,b) for a,b in Et if a == v1 or b == v1 or a == v2 or b == v2]:
                    Et.remove(e)
        
        card = cardinality(Vt,Et)
        #print card
        for v in [k for k,v in card.iteritems() if v == 0]:
            Vs.append(v)
            card.pop(v)
            Vt.remove(v)

    return V,Es

#Pick vertex from cardinality set
def pick(C):
    #print sorted(C, key=C.get)
    return sorted(C, key=C.get)[0]
    
#Pick vertex from cardinality set, deciding randomly on the minimum set of vertexes
#i.e., don't always pick the same vertex among the ones with minimum cardinality
def pickrandom(C):
    _min = C[sorted(C, key=C.get)[0]]
    _C = [c for c in C.iterkeys() if C[c] == _min]
    
    return random.choice(_C)

dataset = sys.argv[1]
#print dataset

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
    T = tuple(str(P) for P in re.findall("[A-Za-z0-9# ]+",pair))
    _T = T[1], T[0]
    if compatibility.count(T) + compatibility.count(_T) == 0:
        compatibility.append(T)
        
#print compatibility

#Read query, generate query set
for q in query.readlines():
    if q.strip() != "":
        query_set.append(q.strip())

query_set = list(enumerate(query_set))

#print query_set

#Apply compatibility set on query, generate the query graph
for P in compatibility:
    v1,v2 = P
    for A in [(i,Q) for i,Q in query_set if Q == v1]:
        for B in [(i,Q) for i,Q in query_set if Q == v2]:
            if (A != B) and edge_count(query_graph,A,B) == 0:
                query_graph.append((A,B))

#print query_graph
#print cardinality(query_set, query_graph)

print "Start Solution:"
solution = solve_heurist1(query_set, query_graph)
for v in solution[0]:
    print "{0}: {1}".format(v[0], v[1])
print
for e in solution[1]:
    print "{0}({1}) <-> {2}({3})".format(e[0][1],e[0][0],e[1][1],e[1][0])
print

lonely = []
leftout = []

for i in solution[0]:
    if edge_count(query_graph,i) == 0:
        lonely.append(i)
        continue
    if edge_count(solution[1],i) == 0:
        leftout.append(i)

print "Pairs: {0}".format(len(solution[1]))
print "Optimality: {0}".format(optimality(solution[0], solution[1]))