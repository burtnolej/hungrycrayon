#!/usr/bin/python

#l = [1,2,3,4,5]

#print [i for i in range(0,len(l)) if i > 2]

#print [i if i > 2 else 5 for i in range(0,len(l))]

d = {'a':1,'b':2,'c':3}
e = {'a':10,'b':20,'c':30}
f = {'a':100,'c':200,'c':300}
g = {'1':d,'2':e,'3':f}


#for i in (v.itervalues() for v in g.itervalues()).next(): print i

for i in (v for v in g.itervalues()).next(): print i

for i in (v for v in g.itervalues()).next(): print i

#print [u for u in v.itervalues() for v in g.itervalues()]
