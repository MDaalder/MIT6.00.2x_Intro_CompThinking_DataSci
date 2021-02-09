# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:55:23 2019

@author: Matt
"""

import random
import pylab

"""Location is two dimensional there is no z coordinate, 
    which would imply flying or digging"""
class Location(object):
    def __init__(self, x, y):
        """ x and y are floats"""
        self.x = x
        self.y = y
        
    def move(self, deltaX, deltaY):
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX,
                        self.y + deltaY)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return (xDist**2 + yDist**2)**0.5
    
    def __str__(self):
        return '<' + str(self.x) + ', '\
                    + str(self.y) + '>'


""" A key design decision was to make the location of a drunk in
    a field an attribute of the field rather than an attribute
    of the drunk
    
    Think of a field as a mapping from drunks to locations.
    This puts a constraint on how we can implement calss drunk.
    Drunks = keys in a dict, so type drunk must be hashable."""
    
""" Aspects of Class Field
        
        - a mapping of drunks to locations
        - unbounded size
        - allows multiple drunks, with no constraints about how they relate to each other
            - ex two drunks can occupy the same space
"""
class Field(object):
    def __init__(self):
        self.drunks = {}
        
    def addDrunk(self, drunk, loc):
        # if the drunk already exists, raise an error
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        # otherwise, add a drunk to the dict
        else:
            self.drunks[drunk] = loc
            
    def getLoc(self, drunk):
        # if drunk not in the dict, it doesn't exist in the field
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        # returns the location of the drunk in the field
        return self.drunks[drunk]
    
    def moveDrunk(self, drunk):
        # is the drunk in the field? This is defensive programming
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        #use move method of Location to get the new location
        self.drunks[drunk] = currentLocation.move(xDist, yDist)
    
    



class OddField(Field):
    """This subclass of Field was implemented in Video:Random Walks
    at ~7:20 (quite a bit later than the other classes in this code)
    
    This subclass has "wormholes", as a dict. Maps locations to 
      locations.
    For instances of OddField, this dict is initialized with some randomly
      chosen locations as keys and other randomly chosen locations as values.    
    """
    def __init__(self, numHoles = 1000, xRange = 100, yRange = 100):
        Field.__init__(self)
        self.wormholes = {}
        for w in range(numHoles):
            x = random.randint(-xRange, xRange)
            y = random.randint(-yRange, yRange)
            newX = random.randint(-xRange, xRange)
            newY = random.randint(-yRange, yRange)
            newLoc = Location(newX, newY)
            self.wormholes[(x, y)] = newLoc

    def moveDrunk(self, drunk):
        Field.moveDrunk(self, drunk)
        x = self.drunks[drunk].getX()
        y = self.drunks[drunk].getY()
        if (x, y) in self.wormholes:
            self.drunks[drunk] = self.wormholes[(x, y)]




""" This class Drunk is not inteded to be useful on its own.
    This is a base class meant to be inherited.
    
    Can make several subclasses of drunks behaving differently:
        - one who wanders around at random, "usual drunk"
        - the "I hate winter" drunk, who tries to move southward"""        
        
class Drunk(object):
    def __init__(self, name = None):
        self.name = name
    
    def __str__(self):
        return 'This drunk is named ' + self.name


class UsualDrunk(Drunk):
    def takeStep(self):
        # no directional bias in the step choices
        stepChoices = [(0.0, 1.0), (0.0, -1.0), (1.0, 0.0),\
                       (-1.0, 0.0)]
        return random.choice(stepChoices)
    
class ColdDrunk(Drunk):
    def takeStep(self):
        # these step choices are slightly biased toward -y (i.e. southward movement to warmth)
        stepChoices = [(0.0, 0.9), (0.0, -1.1), (1.0, 0.0),\
                       (-1.0, 0.0)]
        return random.choice(stepChoices)
    

    

# Very little code needed to simulate a walk.
# Because we created useful data abstractions that would make
# building a simulation quite easy.
    
def walk(f, d, numSteps):
    """Assumes: f a Field, d a Drunk in f, and numSteps an int >= 0.
        Moves d numSteps times; returns the distance between the final
        location and the location at the start of the walk."""
        
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return start.distFrom(f.getLoc(d))


# can assign whatever subclass of Drunk we want as dClass
def simWalks(numSteps, numTrials, dClass):
    """Assumes numSteps an int >= 0, numTrials an int > 0,
        dClass a subclass of Drunk.
        Simulates numTrials walsk of numSteps steps each.
        Returns a list of the final distances for each trial."""
        
    Homer = dClass()
    origin = Location(0, 0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, origin)
#        print(walk(f, Homer, 0)) # this is debugging code
#        print(walk(f, Homer, 1))
#        assert False
        distances.append(round(walk(f, Homer, numSteps), 1))
    return distances


        
def drunkTest(walkLengths, numTrials, dClass):
    """Assumes walkLengths a sequence of ints >= 0 (a tuple)
        numTrials an int > 0,
        dClass a subclass of Drunk
       For each number of steps in walkLengths,
        runs simWalks with numTrials walk and prints results."""
    
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials, dClass)
        
        print(dClass.__name__, 'random walk of', numSteps, 'steps')
        print(' Mean =', round(sum(distances)/len(distances), 4))
        print(' Max =', max(distances), 'Min =', min(distances))
        


def simAll(drunkKinds, walkLengths, numTrials):
    """ will run drunkTest for each class input in drunkKinds, which is a tuple of Drunk subclasses"""
    for dClass in drunkKinds:
        drunkTest(walkLengths, numTrials, dClass)


#random.seed(0)
        
#drunkTest((10, 100, 1000, 10000), 100, UsualDrunk)
#simAll((UsualDrunk, ColdDrunk), (10, 100, 1000, 10000), 100) 




print('\n' 'New simulations being run with graphs!' '\n')



""" We will associate a distinct presentation style with each type of drunk
        for visualisation purposes.
    The style will have three aspects: color of line and marker, 
        shape of the marker, and the kind of line."""
        
class styleIterator(object):
    """ Style iterator class. 
        Iterates/rotates through a sequence of styles defined by
            the arguments to init"""
    def __init__(self, styles):
        self.index = 0
        # self.styles is treated as a ring. We return each style in it until we've returned them all
        # then we go back to the start.
        self.styles = styles
        
    def nextStyle(self):
        result = self.styles[self.index]
        if self.index == len(self.styles) -1:
            self.index = 0
        else:
            self.index += 1
        return result
   
    
def simDrunk(numTrials, dClass, walkLengths):
    meanDistances = []
    for numSteps in walkLengths:
        # print just to check we're making progress
        print('Starting simulation of', numSteps, 'steps')
        trials = simWalks(numSteps, numTrials, dClass)
        mean = sum(trials)/len(trials)
        meanDistances.append(mean)
    return meanDistances


def simAllPlot(drunkKinds, walkLengths, numTrials):
    styleChoice = styleIterator(('m-', 'b--', 'g-.'))
    for dClass in drunkKinds:
        curStyle = styleChoice.nextStyle()
        print('\n' 'Starting simulation of', dClass.__name__)
        means = simDrunk(numTrials, dClass, walkLengths)
        pylab.plot(walkLengths, means, curStyle, label = dClass.__name__)
    
    pylab.title('Mean distance from origin (' + str(numTrials) + ' trials)')
    pylab.xlabel('Number of Steps')
    pylab.ylabel('Distance from origin')
    pylab.legend(loc = 'best')


#random.seed(0)
    
#numSteps = (10, 100, 1000, 10000)
#simAllPlot((UsualDrunk, ColdDrunk), numSteps, 100)



def getFinalLocs(numSteps, numTrials, dClass):
    """ Gets the final location of a type of drunk (dClass) over (numTrials = int > 0) trials 
            for a given number of steps (numSteps = int >= 0)"""
    locs = []
    d = dClass()
    for t in range(numTrials):
        f = Field()
        f.addDrunk(d, Location(0, 0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs

def plotLocs(drunkKinds, numSteps, numTrials):
    styleChoice = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        
        xVals = pylab.array(xVals)
        yVals = pylab.array(yVals)
        meanX = sum(abs(xVals)/len(xVals))
        meanY = sum(abs(yVals)/len(yVals))
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle,
                   label = dClass.__name__ +\
                   ' mean abs dist = <' + str(meanX) +\
                   ', ' + str(meanY) + '>')
    pylab.title('Location at End of Walks (' +\
                str(numSteps) + ' steps)')
    pylab.ylim(-150, 150)
    pylab.xlim(-150, 150)
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc = 'upper left')
    
#random.seed(0)
plotLocs((UsualDrunk, ColdDrunk), 1000, 100)


def traceWalk(fieldKinds, numSteps):
    """ Iterates over types of fields, instead of drunks"""
    styleChoice = styleIterator(('b+', 'r^', 'ko'))
    for fClass in fieldKinds:
        d = UsualDrunk()
        f = fClass()
        f.addDrunk(d, Location(0, 0))
        locs = []
        for s in range(numSteps):
            f.moveDrunk(d)
            locs.append(f.getLoc(d))
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle, 
                   label = fClass.__name__)
        pylab.title('Spots Visited on Walk ('
                    + str(numSteps) + ' steps)')
        pylab.xlabel('Steps East/West of Origin')
        pylab.ylabel('Steps North/South of Origin')
        pylab.legend(loc = "best")

#random.seed(0)
#traceWalk((Field, OddField), 500)    
    
        
        