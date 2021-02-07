# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:26:49 2019

@author: md131
"""
#Left-first, depth-first enumeration
#Decision tree

#Header for decision tree implementation
def maxVal(toConsider, avail):
    """Assumes toConsider a list of items,
            avail a weight
        Returns a tuple of the total value of a solution to
            0/1 knapsack problem and the items of that solution"""
            
            # toConsider. Those items that nodes higher up in the tree (Corresponding
            # to earlier calls in the recursive call stack) have not yet considered.
            
            # avail. The amount of space still available.

    if toConsider == [] or avail == 0: # if nothing else to consider, return tuple 0 and empty
        result = (0, ())
    
    elif toConsider[0].getUnits() > avail: # look at first item that's still in "to consider", but if it's weight is
        result = maxVal(toConsider[1:], avail) # greater than what's still available, then we know we can't take it.
                                                # so return max val of "to consider" without that item. avail is unchanged.
    
    else: # Go to the next item in "to consider". We know we can take it, because it passed the last elif statement.
        nextItem = toConsider[0]
        #Explore the left branch (take the next item)
        withVal, withToTake = maxVal(toConsider[1:], avail - nextItem.getUnits()) #withVal is the max value of the list without the first item, so that doesn't change.
                                                # avail has to change to reduce it by the units of that item to consider subzero
        withVal += nextItem.getValue() # now we can increase withVal by the value of that item (recall nextItem is toConisder[0])
        #Explore the right branch (do not take the next item)
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail) # withoutVal, value if we don't take the item. and withoutToTake, so available weight doesn't change.
                                                # we consider the max value without taking the new item, so the value doesn't change
        
        #Choose the better of the left and right branch to return
        if withVal > withoutVal: # test if left or right branch is better. Return the best answer.
            result = (withVal, withToTake + (nextItem,))
            
        else:
            result = (withoutVal, withoutToTake)
            
    return result
    

# notice that we aren't building the search tree.
# The local variable result records the best solution found so far.    