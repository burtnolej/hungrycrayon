#!/usr/bin/python

i=0
def qsort(L):
    global i
    i+=1
    print i,L
    if len(L) <= 1:
        return L
    #return qsort([lt for lt in L[1:] if lt < L[0]]) + L[0:1] + qsort([ge for ge in L[1:] if ge >= L[0]])
    return qsort([lt for lt in L[1:] if lt < L[0]]) + L[0:1]

print qsort([4,6,7,2,3,1,7,8,9,10,1])
