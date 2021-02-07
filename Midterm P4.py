# -*- coding: utf-8 -*-
"""
Created on Mon May  6 13:28:16 2019

@author: md131
"""

def solve(s):
    """ 
    s: positive integer, what the sum should add up to
    Solves the following optimization problem:
        x1 + x2 + x3 + x4 is minimized 
        subject to the constraint x1*25 + x2*10 + x3*5 + x4 = s
        and that x1, x2, x3, x4 are non-negative integers.
    Returns a list of the coefficients x1, x2, x3, x4 in that order
    """
    
    # list of non-negative integers that represent x1, x2, x3, x4
    xList = [0, 0, 0, 0]
  
    number = s
    
    while number > 0:
        
        if number >= 25:
            xList[0] += number//25
            number = number - xList[0]*25
    
        elif number >= 10:
            xList[1] += number//10
            number = number - xList[1]*10
            
        elif number >= 5:
            xList[2] += number//5
            number = number - xList[2]*5
            
        else:
            xList[3] += number
            number = number - xList[3]
    
    result = sum(xList[:])
    
    return (xList)

print(solve(1532))