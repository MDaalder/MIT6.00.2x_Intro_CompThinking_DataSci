# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:29:50 2019

@author: Matt
"""
import random

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    
    redBalls = ['red', 'red', 'red']
    greenBalls = ['green', 'green', 'green']
    
    count = 0
    
#    for __ in range(3):
#        balls.append('green')
#        balls.append('red')
    
    for trial in range(numTrials):
        balls = redBalls + greenBalls
        reds = 3
        
        for i in range(3):
            
            probRed = reds/len(balls)
            probGreen = 1 - probRed
                        
            colour = random.random()
            
            if colour <= probRed:
                balls.remove('red')
                reds -= 1
            else:
                balls.remove('green')
            
        if balls == redBalls or balls == greenBalls:
            count += 1
    
    return count/numTrials

print(noReplacementSimulation(1000000))
