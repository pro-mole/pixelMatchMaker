#!/usr/bin/python

#I was going to document this in a way that was as generic as possible
#But that was way troublesom. Let's just refer to the things as they are in the game
import sys
import re

dataset = sys.argv[1]
print dataset

pairs = open(dataset+"/pairs","r")
query = open(dataset+"/query","r")

#Compatibility Set
# The professions, laid out in compatible pairs
prof_graph = []

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
    if prof_graph.count(T) + prof_graph.count(_T) == 0:
        prof_graph.append(T)
        
print prof_graph

#Read query, generate query set
for q in query.readlines():
    query_graph.append(q.strip())

print query_set

#Applu compatibility set on query, generate the query graph
