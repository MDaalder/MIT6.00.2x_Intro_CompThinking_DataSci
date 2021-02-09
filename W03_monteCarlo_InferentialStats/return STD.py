# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:22:55 2019

@author: md131
"""

def stdDevOfLengths(L):
    """
    L: a list of strings

    returns: float, the standard deviation of the lengths of the strings,
      or NaN if L is empty.
    """
    if len(L) == 0:
        return float('NaN')
    
    val = 0.0
    for i in range(len(L)):
        val += len(L[i])
    mean = val/len(L)
        
    tot = 0.0
    for t in L:
        tot += (len(t) - mean)**2
    std = (tot/len(L))**0.5
    return std

L = ['a', 'z', 'p']

print(stdDevOfLengths(L))

M = ['apples', 'oranges', 'kiwis', 'pineapples']

print(stdDevOfLengths(M))

def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std

X = [10, 4, 12, 15, 20, 5]
mean, std = getMeanAndStd(X)
coeff = std/mean
print(coeff)