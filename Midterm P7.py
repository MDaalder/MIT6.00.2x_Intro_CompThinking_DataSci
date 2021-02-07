# -*- coding: utf-8 -*-
"""
Created on Mon May  6 14:20:58 2019

@author: md131
"""

def solveit(test):
    """ test, a function that takes an int parameter and returns a Boolean
        Assumes there exists an int, x, such that test(x) is True
        Returns an int, x, with the smallest absolute value such that test(x) is True 
        In case of ties, return any one of them. 
    """
    # IMPLEMENT THIS FUNCTION
    # we are going to do this with bisection search
    
    def bisection(low, high):
        """Solves a problem using bisection search.
            Takes in a low value, and a high value to compute the midpoint
            to find an answer.
            Returns the midpoint of high and low.
        """
    # guess at an answer
    x = 0
    high = 1000
    low = 0    
        
    if test(x) == True:
        return True
    
    else:
        
        while test(x) == False:
            
            if test(x) - x > 0:
                
                           
            elif test(x) - x < 0:
                x = (high - low)/2
            
            x = (high - low)/2
    
    
    return False    
        




#### This test case prints 49 ####
def f(x):
    return (x+15)**0.5 + x**0.5 == 15
print(solveit(f))

#### This test case prints 0 ####
def f(x):
    return x == 0
print(solveit(f))