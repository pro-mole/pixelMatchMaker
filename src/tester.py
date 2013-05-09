#!/usr/bin/python

#Now this is our "brute force" test generator, to try and get some results from our script.
#All's fine and dandy for our particular Pixel People examples, but will this algorithm work on extreme conditions?
#Let's find out
import sys
import random
import string
import matchmaker

pairs = open('pairs.test',"w")
query = open('query.test',"w")

qsize = int(sys.argv[1])
psize = int(sys.argv[2])

for i in range(qsize):
    query.write("{0}\n".format(random.choice(string.uppercase[:26])))

for i in range(psize):
    pairs.write("{0},{1}\n".format(random.choice(string.uppercase[:26]),random.choice(string.uppercase[:26])))

pairs.close()
query.close()
pairs = open('pairs.test',"r")
query = open('query.test',"r")
    
for i in range(10):
    pairs.seek(0)
    query.seek(0)
    sol = matchmaker.solve(pairs,query)
    #for e in sol[0][1]:
    #    print "{0} <-> {1}".format(e[0][0],e[1][0])
    #print
    print sol[1]