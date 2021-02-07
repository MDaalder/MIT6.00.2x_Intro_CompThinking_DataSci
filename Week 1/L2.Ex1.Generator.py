# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:29:50 2019

@author: md131
"""

def yieldAllCombos(items):
    """
        Generates all combinations of N items into two bags, whereby each 
        item is in one or zero bags.

        Yields a tuple, (bag1, bag2), where each bag is represented as a list 
        of which item(s) are in each bag.
    """
    
    N = len(items)
    
    #   enumerate the 3**N possible combinations (item is in bag1, bag2, or no bag)
    for i in range(3**N):
        bag1 = []
        bag2 = []
        for j in range(N):
            if (i // 3**j) % 3 == 1:
                bag1.append(items[j])
            if (i // 3**j) % 3 == 2:
                bag2.append(items[j])   
        
        yield (bag1, bag2)        
#    return (bag1, bag2)