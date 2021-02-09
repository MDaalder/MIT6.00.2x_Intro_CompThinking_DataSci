###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    # creates a list from the dict cows, sorted in descending value of weight
    cowsCopy = sorted(cows.items(),
                      key = lambda kv:(kv[1], kv[0]),
                      reverse = True)
       
    ship = []
    cowsLeft = cows.copy()
    
    
    while sum(cowsLeft.values()) > 0:
        result = []
        totalCost = 0

        for i in range(len(cowsCopy)):
            cow = cowsCopy[i]
            cowsName = cow[0]
            cowsWeight = cow[1]
            
            if (totalCost + cowsWeight) <= limit and cowsWeight != 0:
                result.append(cowsName)
                totalCost += cowsWeight
#                cowsLeft[cowsName] = 0
                cowsLeft.pop(cowsName, None)
        cowsCopy = sorted(cowsLeft.items(),
                  key = lambda kv:(kv[1], kv[0]),
                  reverse = True)
        ship.append(result)
    
    return ship



# Problem 2
def brute_force_cow_transport(cows,limit=60):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
     
    # creates a list of tuples from the dict cows [(name (str), weight (int))]
    cowsCopy = sorted(cows.items())

    
    # dictionary copy of cows {name(key str): weight(value int)}
    cowsLeft = cows.copy()
    
#    print(cowsCopy, 'hello')
    
#    fam = {'Matt': 27, 'Jordan': 26, 'Arie': 55, 'Kelly': 59}
#    cowLeft = fam.copy()
    
    # get all available cow partitions
    
    minTrips = len(cows)
    
    minTrips = limit
    
#    while sum(cowsLeft.values()) > 0:
   
    tempSum = 0
    result = []
    
    for partition in get_partitions(cows):
    
        # want to extract the names from the dictionary
        # use these to get the sum of values (weight), do not exceed limit
        # minimize the number of trips: sort by len of partition
        
        for subPart in partition:
            tempSum = 0
            cowsLeft = cows.copy()
            
            while tempSum <= limit:
#            while sum(cowsLeft.values()) != 0:
                
                for cow in subPart:
                    print('Name', cow, 'Value', cows[cow])
                    print('Partition', partition,'subPart', subPart)
                    print('Left', cowsLeft)
                    
                    tempSum += cows[cow]    
                    print(tempSum, 'Sum', '\n')
                    
                if tempSum > limit:
                    next(partition)
                                                           
                if tempSum <= limit and len(partition) < minTrips:
                    
                    result.append(subPart)
                    minTrips = len(partition)
                    cowsLeft[cow] = 0
                    print(result)
                    
            
#            if len(partition) == minTrips:
#                print(len(partition))
#                print(partition)
        
        
    return result
    # TODO: Your code here
    pass

        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=60
#print(cows)

fam = {'Matt': 27, 'Jordan': 26, 'Arie': 55, 'Kelly': 59}

#print('This is the final greedy cow:', greedy_cow_transport(cows, limit))
print('\n''This is the final brute force:',brute_force_cow_transport(fam, limit))
#for partition in get_partitions(cows):
#    print(partition)


