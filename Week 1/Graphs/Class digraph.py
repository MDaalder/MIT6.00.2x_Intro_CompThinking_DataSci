# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 14:14:42 2019

@author: Matt
"""


# design allows for the possibility of having a more 
# complicated kind of node that has properties other than its name
class Node(object): 
    def __init__(self, name):
        """Assumes name is a string"""
        self.name = name
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    

# allows for the possibility of edges having directions
class Edge(object):
    def __init__(self, source, dest):
        """Assumes source and dest are nodes"""
        self.source = source
        self.dest = dest
    def getSource(self):
        return self.source
    def getDestination(self):
        return self.dest
    def __str__(self):
        return self.source.getName() + '->'\
                + self.dest.getName()


# adjacency list implementation of a graph
# class Digraph is a dictionary that maps values of type node
# to lists of type edge
class Digraph(object):
    """ edges is a dict mapping each node to a 
        list of its children"""
    
    def __init__(self):
        self.edges = {}
    
    def addNode(self, node):
        if node in self.edges:
            raise ValueError('Duplicate node')
        else:
            self.edges[node] = []
            
    def addEdge(self, edge):
        source = edge.getSource()
        dest = edge.getDestination()
        if not (source in self.edges and dest in self.edges):
            raise ValueError('Node not in graph')
        self.edges[source].append(dest)
        
    def childrenOf(self, node):
        return self.edges[node]

    def hasNode(self, node):
        return node in self.edges
    
    def getNode(self, name):
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)
        
    def __str__(self):
        result = ''
        for source in self.edges:
            for dest in self.edges[source]:
                result = result + source.getName() + '->'\
                        + dest.getName() + '\n'
        return result[:-1] # omit final newline
    

# Graph is a subclass of the superclass Digraph
# overwrite addEdge from Digraph, then
# Graph uses Digraph.addEdge to add two edges to a node
# one going in each direction
class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)



def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'):
        #Create 7 nodes as an adjacency matrix
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence')))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g


#print(buildCityGraph(Digraph))


def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result


# depth first search to determine shortest path of a graph by number of edges
    # can be modified to minimize weighted edges
# path and shortest are artifacts of the algorithm
# path is used to keep track of where we are in our exploration of the graph
# shortest used to keep track of the best solution found so far
def DFS(graph, start, end, path, shortest, toPrint = False):
    """ Assumes graph is a Digraph; start and end are nodes;
            path and shortest are lists of nodes
        Returns a shortest path from start to end in graph"""
    #choose one child of the start node
    path = path + [start]
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    # choose one child of the starting node
    for node in graph.childrenOf(start):
        if node not in path: # avoid cycles
            # only keep paths that are shorter, discard if longer
            if shortest == None or len(path) < len(shortest):
                newPath = DFS(graph, node, end, path,
                               shortest, toPrint)
                if newPath != None:
                    shortest = newPath
        
        elif toPrint:
            print('Already visited', node)
    # keep track of shortest path from start to end of problem                
    return shortest



# Breadth first search for minimizing the number of edges used
# BFS not great for minimizing weights of edges
# explores all paths with n hops before exploring any path with more than n hops
# therefore, can return the first answer that comes up (return tmpPath, line 195)    
def BFS(graph, start, end, toPrint = False):
    initPath = [start]
    pathQueue = [initPath]
        
    while len(pathQueue) != 0:
        #Get and remove oldest element in pathQueue
        tmpPath = pathQueue.pop(0)
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
        lastNode = tmpPath[-1]
        
        if lastNode == end:
            return tmpPath
        
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)
    
    return None
        



# This gets recursion started properly
# DFS does not require a path or shortest input to get going
# see commented explanation of def DFS
def shortestDFSPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph: start and end are nodes
        Returns a shortest path from start to end in graph"""
    return DFS(graph, start, end, [], None, toPrint)


def shortestBFSPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph: start and end are nodes
        Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)





def testSP(source, destination, searchType):
    g = buildCityGraph(Digraph)
    if searchType == DFS:
        sp = shortestDFSPath(g, g.getNode(source), g.getNode(destination),
                          toPrint = True)
    elif searchType == BFS:
        sp = shortestBFSPath(g, g.getNode(source), g.getNode(destination),
                          toPrint = True)
    
    
    if sp != None:
        print('Shortest path from', source, 'to', 
              destination, 'is', printPath(sp))
    else:
        print('There is no path from', source, 'to', destination)
        
#testSP('Chicago', 'Boston')
testSP('Boston', 'Phoenix', DFS)            
testSP('Boston', 'Phoenix', BFS)





    
def buildLineGraph(graphType):
    nodes = []
    nodes.append(Node("ABC")) # nodes[0]
    nodes.append(Node("ACB")) # nodes[1]
    nodes.append(Node("BAC")) # nodes[2]
    nodes.append(Node("BCA")) # nodes[3]
    nodes.append(Node("CAB")) # nodes[4]
    nodes.append(Node("CBA")) # nodes[5]
    
    h = Graph()
    for n in nodes:
        h.addNode(n)
    
    h.addEdge(Edge(h.getNode('ABC'), h.getNode('ACB')))
    h.addEdge(Edge(h.getNode('ACB'), h.getNode('CAB')))  
    h.addEdge(Edge(h.getNode('CAB'), h.getNode('CBA'))) 
    h.addEdge(Edge(h.getNode('CBA'), h.getNode('BCA'))) 
    h.addEdge(Edge(h.getNode('BCA'), h.getNode('BAC'))) 
    h.addEdge(Edge(h.getNode('BAC'), h.getNode('ABC'))) 
    return h
    
#print(buildLineGraph(Graph))