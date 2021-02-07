# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 16:05:15 2019

@author: md131
"""

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



# Read the save file "Tree Brute Force" to see the implementation of this with more explanation
def maxVal(toConsider, avail):
    """Assumes toConsider a list of items,
            avail a weight (or calories in this instance)
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
    







    

def fastMaxVal(toConsider, avail, memo = {}):
    # The key of memo is a tuple, ([items left to be considered], available weight)
    # Items left to be considered is represented by len(toConsider). It works because items are always removed form the front of the list
    """Assumes toConsider a list of subjects, avail a weight (or calories in this instance)
        memo supplied by recursive calls
      Returns a tuple of the total value of a solution to the 0/1 knapsack
        problem and the subjects of that solution"""
    
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
        
    elif toConsider == [] or avail == 0:
        result = (0, ())
        
    elif toConsider[0].getCost() > avail:
        #Explore right branch only
        result = fastMaxVal(toConsider[1:], avail, memo)
        
    else:
        nextItem = toConsider[0]
        #Explore left branch
        withVal, withToTake= fastMaxVal(toConsider[1:],
                                        avail - nextItem.getCost(), memo)
        withVal += nextItem.getValue()
        #Explore right branch
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
                                               avail, memo)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    
    memo[(len(toConsider), avail)] = result
    return result
        
        



def testMaxVal(foods, maxUnits, algorithm, printItems = True):
    print('Menu contains', len(foods), 'items')
    print('Use search tree to allocate', maxUnits, 'calories')
    val, taken = algorithm(foods, maxUnits) #maxVal(foods, maxUnits)
    itemTotal = 0
    print('Total value of items taken =', val)
    if printItems:
#        print('Total value of items taken =', val)
        for item in taken:
            itemTotal += item.getCost()
            print(' ', item)
        print('Total calories not used =', maxUnits - itemTotal)    


            
names = ['wine', 'beer', 'pizza', 'burger', 'fries', 'cola', 'apple', 'donut', 'cake']
values = [89, 90, 95, 100, 90, 79, 50, 10]
calories = [123, 154, 258, 354, 365, 150, 95, 195]
foods = buildMenu(names, values, calories)

print('')
testMaxVal(foods, 750, maxVal)



def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
                          random.randint(1, maxVal),
                          random.randint(1, maxCost)))
    
    return items 


for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
    items = buildLargeMenu(numItems, 90, 250)
    testMaxVal(items, 750, fastMaxVal, True) 
    
    