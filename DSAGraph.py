# 
# CURTIN UNIVERISTY COMP1002 - Data Structures and Algorithms
# Assignment 1 - Graph Classes (Modified into Digraph from Prac 06)
#
# Author: Alastair Kho
# ID: 20214878
#


# ===== IMPORTS ===== #

import numpy as np
from LinkedListClasses import *
from QueueClass import *
from MinHeap import *

# ===== VERTEX ===== #

class _GraphVertex():

    # -- Constructor -- #
    def __init__(self, inLabel, inValue):
        self._label = str(inLabel) 
        self._value = inValue
        self._links = MinHeap(10000) # Adjacency List
        self._visited = False

    # -- Accessors -- #
    def getLabel(self) -> str:
        return self._label
    
    def getValue(self) -> object:
        return self._value

    def getAdjacent(self) -> MinHeap: 
        return self._links

    def getVisited(self) -> bool:
        return self._visited
    
    # -- Mutators -- #
    def setLabel(self, inLabel) -> None:
        self._label = inLabel
    
    def setValue(self, inValue) -> None:
        self._value = inValue

    def setVisited(self) -> None:
        self._visited = True
    
    def clearVisited(self) -> None:
        self._visited = False

    def insertEdge(self, vertex) -> None:
        self._links.add(vertex.getValue(), vertex) # Add to Adjacency List
    
    def removeEdge(self, vertexLabel) -> None:
        for count, adjacent in enumerate(self._links):
            if adjacent.getLabel() == vertexLabel:
                self._links.remove(count)

    # -- Private Methods -- #
    def __repr__(self) -> str:
        return (f"({self._label}, {self._value})")


# ===== EDGE ===== #
class _GraphEdge():
    
    # -- Constructor -- #
    def __init__(self, fromVertex, toVertex, inWeight) -> None:
        self._fromVertex = fromVertex
        self._toVertex = toVertex
        self._weight = inWeight

    # -- Accessors -- #
    def getFromVertex(self) -> _GraphVertex:
        return self._fromVertex

    def getToVertex(self) -> _GraphVertex:
        return self._toVertex

    def getWeight(self) -> object:
        return self._weight    

    # -- Mutators -- #
    def setWeight(self, inValue) -> None:
        self._weight = inValue    
            
    # -- Private Methods -- #
    def __repr__(self) -> str:
        return f"({self._fromVertex.getLabel()}, {self._toVertex.getLabel()}, {self._weight})"


# ===== GRAPH ===== #
class DSAGraph(): # Directional Graph

    # -- Constructor -- #
    def __init__(self, numMaxVertices, numMaxEdges) -> None:
        self._vertices = MinHeap(numMaxVertices) # held in min based heap to maintain priority.
        self._edges = MinHeap(numMaxEdges) # held in min based heap to maintain priority.
        # min heap is important to generate routes in a ranked order from lower weight to higher weight. heapsort is also implemented

    # -- Accessors -- #
    def getVertex(self, label) -> _GraphVertex:
        for vertex in self._vertices:
            if vertex.getLabel() == label:
                return vertex
        # if function exits iterator, label not in graph 
        raise ValueError(f"'{label}' {type(label)} not in graph!")

    def getEdge(self, fromLabel, toLabel) -> _GraphEdge:
        for edge in self._edges:
            if edge.getFromVertex().getLabel() == fromLabel and edge.getToVertex().getLabel() == toLabel:
                return edge
        # if function exits iterator, label not in graph 
        raise ValueError(f"'{fromLabel}-{toLabel}' not in graph!")

    def hasVertex(self, label) -> bool:
        exists = True
        try:
            self.getVertex(label)
        except:
            exists = False
        return exists

    def hasEdge(self, fromLabel, toLabel) -> bool:
        exists = True
        try:
            self.getEdge(fromLabel, toLabel)
        except:
            exists = False
        return exists

    def getVertexCount(self) -> int:
        return self._vertices.getCount()

    def getEdgeCount(self) -> int:
        return self._edges.getCount()

    def getAdjacent(self, label) -> MinHeap:
        return self.getVertex(label).getAdjacent()

    def isAdjacent(self, label1, label2) -> bool:
        adjacent = False
        vertex1 = self.getVertex(label2)

        # Digraph, only checks one way edge.
        if (vertex1 in self.getAdjacent(label1)):
            adjacent = True

        return adjacent

    def displayAsList(self) -> None:
        print("   |   \n   |   # -- Graph Adjacency List -- #")
        
        for vertex in self._vertices:
            adjacentString = ""

            for adjVertex in self.getAdjacent(vertex.getLabel()):
                adjacentString += f"{adjVertex.getLabel()} "

            print(f"   |   {vertex.getLabel()} | {adjacentString}")

    def getMatrix(self) -> np.ndarray:

        matrixSize = self.getVertexCount() + 1
        array = np.empty((matrixSize, matrixSize), dtype=object)
        array[0][0] = " "
        # generate matrix
        for row, value1 in enumerate(self._vertices): # note: below works as it will always iterate until matrixSize-1
            for col, value2 in enumerate(self._vertices):

                value1Label = value1.getLabel()
                value2Label = value2.getLabel()

                if row == 0:
                    array[row][col + 1] = value2Label
                if col == 0:
                    array[row + 1][col] = value1Label

                if self.isAdjacent(value1Label, value2Label):
                    array[row + 1][col + 1] = self.getEdge(value1Label, value2Label).getWeight() # get weight
                else:
                    array[row + 1][col + 1] = "-"
        return array

    # -- Mutators -- #
    def addVertex(self, label, value) -> None:
        if self.hasVertex(label):
            raise ValueError(f"'{label}' already exists in graph!")
        else:
            newVertex = _GraphVertex(label, value)
            self._vertices.add(value, newVertex) # vertex holds weight and vertex object
    
    def addEdge(self, label1, label2, weight) -> None:
        if self.isAdjacent(label1, label2):
            raise ValueError(f"'{label1}' and '{label2}' are already connected with an edge")
        # directional graph
        else:

            vertex1 = self.getVertex(label1)
            vertex2 = self.getVertex(label2)
            
            vertex1.insertEdge(vertex2)
            newEdge = _GraphEdge(vertex1, vertex2, weight)

            self._edges.add(weight, newEdge) # _edges hold weight and edge object
    
    def removeVertex(self, label) -> _GraphVertex:
        if not self.hasVertex(label):
            raise ValueError(f"'{label}' not in graph!")
        else:
            # Vertex appears once in self._vertices
            retVal = None # one vertice
            for verticeIdx, vertex in enumerate(self._vertices):
                if vertex.getLabel() == label:
                    self._vertices.remove(verticeIdx)
                    retVal = vertex
        
            # Scan everywhere for any traces of the label. Vertex to delete may appear multiple times in self._Eedges
            edgeIdx = 0 
            while edgeIdx != self._edges.getCount():
                edgeEntry = self._edges.heapArray[edgeIdx]
                if edgeEntry != None:
                    edge = edgeEntry.getValue()

                    if edge.getFromVertex().getLabel() == label:
                        edge.getToVertex().removeEdge(label)
                        self._edges.remove(edgeIdx)
                        edgeIdx = 0
                    else:
                        edgeIdx += 1

            edgeIdx = 0 
            # Scan again for any traces of the label. This is to debug above, some vertices might be missed above, but above
            # will always remove the majority. This will do one last sweep.
            while edgeIdx != self._edges.getCount():
                edgeEntry = self._edges.heapArray[edgeIdx]
                if edgeEntry != None:
                    edge = edgeEntry.getValue()

                    if edge.getToVertex().getLabel() == label:
                        edge.getFromVertex().removeEdge(label)
                        self._edges.remove(edgeIdx)
                        edgeIdx = 0
                    else:
                        edgeIdx += 1
            return retVal

    def removeEdge(self, fromLabel, toLabel) -> _GraphEdge:
        if not self.hasEdge(fromLabel, toLabel):
            raise ValueError(f"Edge '{fromLabel} {toLabel}' not in graph!")
        else:
            for count, edge in enumerate(self._edges):
                if edge.getFromVertex().getLabel() == fromLabel and edge.getToVertex().getLabel() == toLabel:
                    retVal = edge
                    edge.getFromVertex().removeEdge(toLabel)

                    self._edges.remove(count)
                    return retVal

    # -- Traversals -- #

    def breadthFirstSearch(self, vertex0Label) -> DSAQueue: # breadth first search from lecture nodes
        exploreQueue = DSAQueue()
        discoveredQueue = DSAQueue()

        vertex0 = self.getVertex(vertex0Label)

        for vertex in self._vertices:
            vertex.clearVisited()
        
        vertex0.setVisited()
        exploreQueue.enqueue(vertex0)

        while not exploreQueue.isEmpty():

            tempVertex = exploreQueue.dequeue() # explore tempVertex

            for neighbour in tempVertex.getAdjacent():

                if neighbour.getVisited() != True:
                    edge = self.getEdge(tempVertex.getLabel(), neighbour.getLabel())

                    newEdge = _GraphEdge(tempVertex, neighbour, edge.getWeight())
                    discoveredQueue.enqueue(newEdge)
                    neighbour.setVisited()
                    exploreQueue.enqueue(neighbour)
        
        return discoveredQueue

    def depthFirstSearch(self, vertex0Label) -> DSAQueue: # depth first search from lecture nodes

        discoveredQueue = DSAQueue()
        
        for vertex in self._vertices:
            vertex.clearVisited()
        retVal = self._dfsRec(discoveredQueue, vertex0Label)
        return retVal

    def _dfsRec(self, discoveredQueue, vertex0Label) -> DSAQueue: # depth first search from lecture nodes

        vertex0 = self.getVertex(vertex0Label)
        vertex0.setVisited()

        for neighbour in vertex0.getAdjacent():
            if neighbour.getVisited() != True:

                edge = self.getEdge(vertex0Label, neighbour.getLabel())
                newEdge = _GraphEdge(vertex0, neighbour, edge.getWeight())
                discoveredQueue.enqueue(newEdge)
                self._dfsRec(discoveredQueue, neighbour.getLabel())

        return discoveredQueue

    def getRouteWeight(self, route) -> int:
        totalWeight = 0
        currNode = None
        prevNode = None
        for count, node in enumerate(route):
            totalWeight += int(node.getValue()) #add on node weight 
            if count == 0:
                currNode = node
            else:
                prevNode = currNode # this is required to keep track of edges. route heap stores vertices and not edges.
                currNode = node
                try: # edge exists weight is added on based on edge weight
                    totalWeight += int(self.getEdge(prevNode.getLabel(), currNode.getLabel()).getWeight())
                except: # edge does not exist, route weight = 0
                    totalWeight = 0
        return totalWeight

    def generateRoutes(self, startLabel, targetLabel, numRoutesToGen) -> MinHeap:
        startVertex = self.getVertex(startLabel)
        endVertex = self.getVertex(targetLabel)

        self._vertices.heapSort() # logn complexity
        
        for i in self._vertices:
           i._links.heapSort() # logn complexity

        vertexList = self._vertices

        for vertex in vertexList:
            vertex.clearVisited()
            
        route = DSALinkedList() # store the routes, not fixed as amount of routes can be dynamic
        routeList = MinHeap(numRoutesToGen)
        self._routingDFSRec(routeList, route, startVertex, endVertex)
        
        routeList.heapSort() # logn complexity
        
        return routeList

    def _routingDFSRec(self, routeList, route, startVertex, targetVertex) -> None: # Extended version of DFS to generate routes
        if not routeList.isFull(): # if routelist is not full (input given in generateRoutes for max amount of routes to generate)
            startVertex.setVisited()
            route.insertLast(startVertex)

            if targetVertex == startVertex: # base case

                newPath = DSALinkedList() # copy path and insert into route list
                for node in route:
                    newPath.insertLast(node)
                routeList.add(self.getRouteWeight(newPath), newPath)

                route.removeLast()
                startVertex.clearVisited()

            else: # recursive case
                # where startVertex.getAdjacent() returns a priority heap. This means that neighbours with lower weights are prioritised
                # first. Useful when generating less routes than possible routes to quickly find the top best routes.
                for neighbour in startVertex.getAdjacent():
                    if neighbour.getVisited() != True:
                        self._routingDFSRec(routeList, route, neighbour, targetVertex)

                startVertex.clearVisited()
                route.removeLast()



