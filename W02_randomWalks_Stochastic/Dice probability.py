# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:44:34 2019

@author: Matt
"""
import random
random.seed(0)
# this sets the seed from which the random number generator will check
# to determine what the "random" number will be. Usually the seed is 
# something unknown, but if we set the seed to 0 (something known) the
# result from our code will always be the same.
# This is useful for debugging, wince we can expect a certain answer.

def rollDie():
    """ returns a random int between 1 and 6"""
    return random.choice([1, 2, 3, 4, 5, 6])


def testRoll(n = 10):
    result = ''
    for i in range(n):
        result = result + str(rollDie())
    print(result)
    


#testing the probability of rolling a sequence of numbers using
# 6 sided die    
def runSim(goal, numTrials):
    total = 0
    for i in range(numTrials):
        result = ''
        for j in range(len(goal)):
            result += str(rollDie())
        if result == goal:
            total += 1
            
    print('Actual probability =',
          round(1/(6**len(goal)), 8)) # rounded to look nice
    
    estProbability = round(total/numTrials, 8)
    print('Estimated Probability =',
          round(estProbability, 8))

runSim('11111', 10000)
# this will result in a different answer every run, UNLESS
# the seed is set ourselves to a specific number, in which case
# the result will always be the same.


# How common are boxcars? Meaning, rolling double 6's with 6 sided die
# 6^2 possible combinations of two die # of which only 1 is double 6's. 
# Probability is 1/36 = 1/6^2, ~0.026777 (2.6777%)
def fracBoxCars(numTests):
    numBoxCars = 0
    for i in range(numTests):
        if rollDie() == 6 and rollDie() == 6:
            numBoxCars += 1
    return numBoxCars/numTests

print('Frequency of double 6 =',
      str(fracBoxCars(100000)*100) +'%')
