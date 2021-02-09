# -*- coding: utf-8 -*-
"""
Created on Wed May 15 15:27:31 2019

@author: md131
"""
import pylab
import random
import scipy.integrate

# discreet approximation of a normal distribution
# it's not continuous it's not generated from an infinite number of points
def plotNormal(mean, std):
    dist = []
    for i in range(100000):
        # pulls a random number from a normal distribution around the mean and standard deviation
        dist.append(random.gauss(mean, std)) 
    pylab.hist(dist, 30) # histogram with 30 bins

#plotNormal(0, 30)



# Takes in a point x, the mean mu, and std sigma
# returns the probability of x
def gaussian(x, mu, sigma):
    factor1 = (1.0/(sigma*((2*pylab.pi)**0.5)))
    factor2 = pylab.e**-(((x-mu)**2)/(2*sigma**2))
    return factor1*factor2


# Computes the area under portions of the normal distributions for some randomly chosen
    # means and standard deviations

def checkEmpirical(numTrials):
    for t in range(numTrials):
        mu = random.randint(-10, 10)
        sigma = random.randint(1, 10)
        print('For mu =', mu, 'and sigma =', sigma)
        # numStd is 1, 2, 3 stds (checking if 68%, 95%, 99.7% confidence intervals)
        for numStd in (1, 1.96, 3):
            # scipy.integrate.quad prints the integral from -2 to 2 of a normal distribution with mean 0 and std 1
            area = scipy.integrate.quad(gaussian,
                                        mu-numStd*sigma,
                                        mu+numStd*sigma,
                                        (mu, sigma))[0]
            print(' Fraction within', numStd, 'std =', round(area, 4))

checkEmpirical(3)