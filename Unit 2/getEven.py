# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 15:23:46 2019

@author: Matt
"""

import random

def genEven():
    '''
    Returns a random even number x, where 0 <= x < 100
    '''
    
    nums = []
    
    for i in range(0,100,2):
        nums.append(i)
    
    return random.choice(nums)
    
print(genEven())



def deterministicNumber():
    '''
    Deterministically generates and returns an even number between 9 and 21
    '''
    
    nums = []
    
    for i in range(9,21):
        if i % 2 == 0:
            nums.append(i)
    
    return nums[2]

print(deterministicNumber())



def stochasticNumber():
    '''
    Stochastically generates and returns a uniformly distributed even number between 9 and 21
    '''
    nums = []
    
    for i in range(9,21):
        if i % 2 == 0:
            nums.append(i)
            
    return random.choice(nums)
    

    
    
    
    