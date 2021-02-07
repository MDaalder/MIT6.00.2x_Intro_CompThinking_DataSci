# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
#from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6

# For Python 3.7:
from ps2_verify_movement37 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.7


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        
        # tile position will be keys, 'clean' or 'dirty' will be values
        self.tiles = {}
        
        # fills the dictionary with all possible tiles in width and range
        # each tile is assumed to start as dirty
        # key is a position (w, h) as a tuple 
        # value is 'dirty' or 'clean' as a string
        for w in range(self.width):
            for h in range(self.height):
                tile = (w, h)
                self.tiles[tile] = 'dirty'     
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.pos = pos
        
        # initiate a tuple to be the current position
        # the position will be converted to a tuple of integers in case the robot's position is a tuple of floats
        intPos = (int(pos.getX()), int(pos.getY()))
 
        # changes the tile to 'clean'
        self.tiles[intPos] = 'clean'
        

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        
        if self.tiles[(m, n)] == 'clean':
            return True
        else:
            return False
        
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        
        return (self.width*self.height)
        

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        numCleanTiles = 0
        
        for tile in self.tiles.values():
            if tile == 'clean':
                numCleanTiles += 1
        
        return numCleanTiles


    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        
        randomW = math.floor(random.uniform(0, (self.width - 0.01)))
        randomH = math.floor(random.uniform(0, (self.height - 0.01)))
        
        randomPos = Position(randomW, randomH)
        
        return randomPos
            

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        
        if pos.getX() >= 0 and pos.getX() <= (self.width - 0.01):
            if pos.getY() >= 0 and pos.getY() <= (self.height - 0.01):
                return True
        
        return False
        

# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        
        
        self.robots = {}
        
        
        # sets the robot down at a random position within the room
        # robotPos will be of type Position (from getRandomPosition function)
        robotPos = self.room.getRandomPosition()
        self.robotPos = robotPos
        # initialises the robot with a random direction
        robotAngle = random.randint(0, 360)
        self.robotAngle = robotAngle
        
        # cleans the tile the robot is initialised on
        self.room.cleanTileAtPosition(self.robotPos)
        


    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        # robotPost should be of class Position: getX() and getY() work
        # self.robotPos should be updated constantly
        positionNow = Position(self.robotPos.getX(), self.robotPos.getY())
        
        return positionNow

    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        
        directionNow = self.robotAngle
        
        return directionNow


    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.robotPos = position
        

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.robotAngle = direction
        

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
#        self.robotPos = self.robotPos.getNewPosition(self.getRobotDirection(), self.speed)
#        cleanTileAtPosition(self.robotPos)
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # current position of robot
        curPos = self.getRobotPosition()
        # new position of robot after a single time-step
        newPos = self.robotPos.getNewPosition(self.getRobotDirection(), self.speed)
        
        # if the new position is inside the room (not a wall or outside)
        # then move to that tile and clean the tile
        if self.room.isPositionInRoom(newPos) == True:
            self.robotPos = newPos
            self.room.cleanTileAtPosition(newPos)
            
        # if the new position is not inside ther oom (hit a wall, or moved outside)
        # then choose a new direction to move in, and do not move yet
        elif self.room.isPositionInRoom(newPos) == False:
            self.setRobotDirection(random.randint(0, 360))
            self.robotPos = curPos


# Uncomment this line to see your implementation of StandardRobot in action!
testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    # this will record the time ticks taken per trial
    timesList = []
    
    # completes the number of trials requested
    for trial in range(num_trials):
        # for animation purposes. Delay is default 0.2 (5 frames/s) Also uncomment lines 381 & 388
#        anim = ps2_visualize.RobotVisualization(num_robots, width, height, 0.2)

        # initiates a list to store robots of class robot_type
        # initiates our time counter, and the percent of the room that is clean
        # and our room of class RectangularRoom to assign to every robot, so they share the same room dictionary
        robotList = []
        clockTicks = 0
        percClean = 0.0
        room = RectangularRoom(width, height) 
        
        # assigns the appropriate number of robots to the same room
        # the robots are stored in a list for easy access ['robot1', 'robot2'... 'robotn']
        for robot in range(num_robots):
            robotName = 'robot' + str(robot + 1)
            robotName = robot_type(room, speed)
            robotList.append(robotName)
            percClean = (robotName.room.getNumCleanedTiles())/(robotName.room.getNumTiles())
        
        # will run the trial until the minimum of cleaned room tiles is achieved
        while percClean < min_coverage:
            # stores and keeps track of the time clicks taken
            clockTicks += 1

            # iterates through all possible robots for 1 time tick
            # cleans a tile and moves, or sets a new direcction
            # updates the percentage of the room cleaned
            for robot in robotList:
#                anim.update(room, robotList)
                robot.updatePositionAndClean()
                percClean = (robot.room.getNumCleanedTiles())/(robot.room.getNumTiles())
        
        # stores the time taken per trial
        timesList.append(clockTicks)
        
#        anim.done()

    # gets the average time over all trials     
    avgTime = sum(timesList)/len(timesList)
    
    return avgTime
    
    return print(num_robots, 'robots of type', str(robot_type), 'takes around', avgTime, 
                 'clock ticks to clean', int(min_coverage*100), '% of a',
                 width, 'by', height, 'room.')    

  
# Uncomment these lines to see how much your simulation takes on average    
#random.seed(0)
#runSimulation(1, 1.0, 5, 5, 1.0, 50, StandardRobot)


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        # current position of robot
        curPos = self.getRobotPosition()
        # new position of robot after a single time-step
        newPos = self.robotPos.getNewPosition(self.getRobotDirection(), self.speed)
        
        # if the new position is inside the room (not a wall or outside)
        # then move to that tile and clean the tile
        if self.room.isPositionInRoom(newPos) == True:
            self.robotPos = newPos
            self.room.cleanTileAtPosition(newPos)
            self.setRobotDirection(random.randint(0, 360))
            
        # if the new position is not inside ther oom (hit a wall, or moved outside)
        # then choose a new direction to move in, and do not move yet
        elif self.room.isPositionInRoom(newPos) == False:
            self.setRobotDirection(random.randint(0, 360))
            self.robotPos = curPos
        
#        raise NotImplementedError

#random.seed(0)
#runSimulation(1, 1.0, 6, 6, 1.0, 1, StandardRobot)
#runSimulation(1, 1.0, 6, 6, 1.0, 1, RandomWalkRobot)




def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#showPlot1('Time it takes 1-10 robots to clean 80% of a room (20x20)', 'Num_Robots', 'Time')

#showPlot2('Time it takes 2 robots to clean 80% of variously shaped rooms', 'Aspect Ratio', 'Time')
    


