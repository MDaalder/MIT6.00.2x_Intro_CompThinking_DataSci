# -*- coding: utf-8 -*-
"""
Created on Mon May  6 14:56:45 2019

@author: md131
"""

def solveit(test):
    """ test, a function that takes an int parameter and returns a Boolean
        Assumes there exists an int, x, such that test(x) is True
        Returns an int, x, with the smallest absolute value such that test(x) is True 
        In case of ties, return any one of them. 
    """
    
    x = 0
    
    for j in range(0, 1000):
        
        if test(j) == True:
            x = j
#            print(j)
            return x
        
        elif test(-j) == True:
            x = -j
            return x
    
    
    
    #### This test case prints 49 ####
def f(x):
    return (x+15)**0.5 + x**0.5 == 15
print(solveit(f))

#### This test case prints 0 ####
def f(x):
    return x == 0
print(solveit(f))