# -*- coding: utf-8 -*-
"""
Created on Wed May 15 12:07:12 2019

@author: md131
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:34:33 2019

@author: md131
"""

import random

class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1, 37):
            self.pockets.append(i)
        self.ball = None
        self.blackOdds, self.redOdds = 1.0, 1.0
        self.pocketOdds = len(self.pockets) - 1.0
        
    def spin(self):
        self.ball = random.choice(self.pockets)
    
    def isBlack(self):
        if type(self.ball) != int:
            return False
        if ((self.ball > 0 and self.ball <= 10)\
            or (self.ball > 18 and self.ball <= 28)):
            return self.ball%2 == 0
        else:
            return self.ball%2 == 1
    
    def isRed(self):
        return type(self.ball) == int and not self.isBlack()
    
    def betBlack(self, amt):
        if self.isBlack():
            return amt*self.blackOdds
        else:
            return -amt
    
    def betRed(self, amt):
        if self.isRed():
            return amt*self.redOdds
        else:
            return -amt
    
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            # how much you win
            return amt*self.pocketOdds
        else:
            # how much you lose
            return -amt
    
    def __str__(self):
        return 'Fair Roulette'

# European Roulette adds an extra pocket '0'
class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0')
    def __str__(self):
        return 'European Roulette'

# American Roulette adds another pocket '00'
class AmRoulette(EuRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00')
    def __str__(self):
        return 'American Roulette'

def playRoulette(game, numSpins, toPrint = True):
    luckyNumber = '2'
    bet = 1
    totRed, totBlack, totPocket = 0.0, 0.0, 0.0
    
    for i in range(numSpins):
        game.spin()
        totRed += game.betRed(bet)
        totBlack += game.betBlack(bet)
        totPocket += game.betPocket(luckyNumber, bet)
    
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting red =', str(100*totRed/numSpins) + '%')
        print('Expected return betting black =', str(100*totBlack/numSpins) + '%')
        print('Expected return betting', luckyNumber, '=', str(100*totPocket/numSpins) + '%\n')
        
    return (totRed/numSpins, totBlack/numSpins, totPocket/numSpins)
    

def findPocketReturn(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    for i in range(numTrials):
        trialVals = playRoulette(game, trialSize, toPrint)
        pocketReturns.append(trialVals[2])
    return pocketReturns

# Gives the expected returns of each type of roulette game with a given
random.seed(0)
numTrials = 20
resultDict = {}
games = (FairRoulette, EuRoulette, AmRoulette)
# Initializes a dictionary with the string value (keys) of each game tied to an output List (value)
# This dictionary stores the results
for G in games:
    resultDict[G().__str__()] = []
for numSpins in (100, 1000, 10000, 100000):
    print('\nSimulate betting a pocket for', numTrials, 'trials of',
          numSpins, 'spins each')
    # iterates over each type of game for each trial of numSpins
    for G in games:
        pocketReturns = findPocketReturn(G(), numTrials, numSpins, False)
        print('Exp. return for', G(), '=',
              str(100*sum(pocketReturns)/float(len(pocketReturns))) + '%')

def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std
    
# Applying the Empirical Rule using mean and standard deviation to get
# confidence intervals and levels
numTrials = 20
resultDict = {}
games = (FairRoulette, EuRoulette, AmRoulette)
# Initializes a dictionary with the string value (keys) of each game tied to an output List (value)
# This dictionary stores the results
for G in games:
    resultDict[G().__str__()] = []
for numSpins in (100, 1000, 10000, 100000):
    print('\nSimulate betting a pocket for', numTrials, 'trials of',
          numSpins, 'spins each')
    # iterates over each type of game for each trial of numSpins
    for G in games:
        pocketReturns = findPocketReturn(G(), numTrials, numSpins, False)
        mean, std = getMeanAndStd(pocketReturns)
        resultDict [G().__str__()].append((numSpins, 100*mean, 100*std))
        
        print('Exp. return for', G(), '=', str(round(100*mean, 3))
              + '%, ', '+/- ' + str(round(100*1.96*std, 3)) # 1.96 is used to compute confidence interval of 95%
              + '% with 95% confidence')
                



