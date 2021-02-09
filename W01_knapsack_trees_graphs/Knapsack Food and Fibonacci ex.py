# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:05:41 2019

@author: md131
"""

import random

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:35:23 2019

@author: md131
"""

class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w
    
    def getValue(self):
        return self.value
    
    def getCost(self):
        return self.calories
    
    def density(self):
        return self.getValue()/self.getCost()
    
    def __str__(self):
        return self.name + ': <' + str(self.value) + ', ' + str(self.calories) + '>'




def buildMenu(names, values, calories):
    """names, values, calories lists of same length.
    name is a list of strings.
    values and calories are lists of numbers.
    returns list of Foods --- it's a menu of items of class Food!"""
    
    menu = []
    for i in range(len(values)):
        menu.append(Food(names[i], values[i], calories[i]))
    
    return menu



# this approximation alogrithm is nlogn + n = nlogn complexity.
def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
    keyFunction maps elements of items to numbers"""
    
    # 'sorted' is a function that returns a new sorted list whereas# 'sort' sorts items in the original list and mutates it. we don't want to mutate the menu given
    itemsCopy = sorted(items, key = keyFunction,  # items are put in a list from best to worst, as we use the keyFunction to define best
                       reverse = True)   # and we reverse the list to go from best to worst.
     
    result = []
    totalValue, totalCost = 0.0, 0.0
    
    for i in range (len(itemsCopy)):
        if (totalCost + itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
            
    return (result, totalValue)


def testGreedy(items, constraint, keyFunction): # keyFunction is what we mean by best
    taken, val = greedy(items, constraint, keyFunction)
    print('Total value of items taken =', val)
    for item in taken:
        print(' ', item)
        

def testGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    
    print('\nUse greedy by cost to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, lambda x: 1/Food.getCost(x)) # we want the inverse of getCost, so list is sorted from least cost (calories) to highest cost (calories)
    
    print('\nUse greedy by density to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.density)



# Read the save file "Tree Brute Force" to see the implementation of this with more explanation
def maxVal(toConsider, avail):
    """Assumes toConsider a list of items,
            avail a weight
        Returns a tuple of the total value of a solution to
            0/1 knapsack problem and the items of that solution"""
            
            
    if toConsider == [] or avail == 0: 
        result = (0, ())
    
    elif toConsider[0].getCost() > avail: # cost is greater than what's available if item taken, so can only take right branch.
        #Explore right branch only
        result = maxVal(toConsider[1:], avail) 
                                                    
    else: 
        nextItem = toConsider[0]
        #Explore left branch
        withVal, withToTake = maxVal(toConsider[1:], avail - nextItem.getCost()) 
        withVal += nextItem.getValue() 
        #Explore right branch
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail) 
        #Choose better branch
        if withVal > withoutVal: 
            result = (withVal, withToTake + (nextItem,))
        
        else:
            result = (withoutVal, withoutToTake)
        
    return result
    



def testMaxVal(foods, maxUnits, printItems = True):
    print('Use search tree to allocation', maxUnits, 'calories')
    val, taken = maxVal(foods, maxUnits)
    print('Total value of items taken =', val)
    if printItems:
        for item in taken:
            print(' ', item)

names = ['wine', 'beer', 'pizza', 'burger', 'fries', 'cola', 'apple', 'donut', 'cake']
values = [89, 90, 95, 100, 90, 79, 50, 10]
calories = [123, 154, 258, 354, 365, 150, 95, 195]
foods = buildMenu(names, values, calories)

testGreedys(foods, 750)
print('')
testMaxVal(foods, 750)
    


# Week 1, Lecture 2: Recurseive Fibonacci

def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
                          random.randint(1, maxVal),
                          random.randint(1, maxCost)))
    
    return items 


for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45):
    items = buildLargeMenu(numItems, 90, 250)
    testMaxVal(items, 750, False) 