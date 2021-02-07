# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:20:03 2019

@author: md131
"""

def fastFib(n,  memo = {}):
    """Assumes n is an int >= 0, memo used only by recursive calls
        Returns Fibonacci of n"""
        
    if n == 0 or n == 1: # the base case, return the answer of 1
        return 1
    
    try:    # check if the fibonacci number of n is already in the dictionary
        return memo[n]
    except KeyError: # if fib(n) is not in the dictionary, compute it, store it, and return the answer
        result = fastFib(n-1, memo) + fastFib(n-2, memo)
        
        memo[n] = result
        return result


for i in range(121):
    print('fib(' + str(i) + ') =', fastFib(i))