# 
# CURTIN UNIVERISTY COMP1002
# Data Structures and Algorithms
# Assignment 1
#
# Author: Alastair Kho
# ID: 20214878
# 

# ======================================= #
# ========== EDITABLE SETTINGS ========== #
# ======================================= #

defaultNumRoutes = 1000000000  # SIMULATION MODE ONLY - number of routes to generate maximum routes. This may be changed depending on computer capabilities.
                               # CONSIDER Lowering this number if your computer does not have enough RAM.
                               # CONSIDER Increasing this number if your computer has sufficient RAM.


# ======================================= #
# ===== DO NOT EDIT BELOW THIS LINE ===== #
# ======================================= #


# ===== IMPORTS ===== #

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

from DSAGraph import *
from HashTable import *
from LinkedListClasses import *


# ===== FUNCTIONS ==== #

# Informative Outpus - Program Usage
def printProgramUsage() -> None:
    print("\nProgram Usage")
    print("Simulation Mode: python3 -s <inputFile> <outputFile>")
    print("Interactive Mode: python3 -i")

# Informative Output - Program Requirements
def printProgramRequirements() -> None:
    print("Required Modules")
    print(f"'networkx' - Required Version: 2.6.3 or later. Current version: {nx.__version__}")
    print(f"'matplotlib' - Required Version: 1.21.1 or later. Current version: {matplotlib.__version__}")
    print(f"'numpy' - Required Version: 3.4.3 or later. Current version: {np.__version__}")

# Menu Mode Input Manager
def isValidMenuChoice(pInput) -> bool:
    retVal = False
    try:
        intInput = int(pInput)
        if intInput >= 1 and intInput <= 9: # check if it's a valid option
            return True
    except:
        if pInput == "X" or pInput == "EXIT()": # commands available to exit
            retVal = True
        else:
            retVal = False
    return retVal 

def menuMode(fileName) -> str:

    print("\n \033[1m# ------ MENU ------ #\033[0m \n")
    if fileName != None:
        print(f"  Current Loaded File: {fileName} \n")
    print("  > [1] Load Input File")
    print("  > [2] Node Operations")
    print("  > [3] Edge Operations")
    print("  > [4] Parameter Tweaks")
    print("  > [5] Display Graph")
    print("  > [6] Display World")
    print("  > [7] Generate Routes")
    print("  > [8] Display Routes")
    print("  > [9] Save Network")
    print("  > [X] Exit Program")
    print("\nPlease Select An Option:\n ")

    menuModeInput = input(" > ").upper()

    while not isValidMenuChoice(menuModeInput): # demand for valid inputs
        print("\nInvalid Input, please select a valid option\n")
        menuModeInput = input(" > ").upper()

    return menuModeInput

    # Read Input File Manager

# Read file, updates DSA graph and visual graphs, puts information into dictionaries and lists.
def readInputFile(inFileName, nxGraph, nodeTypeDict, edgeTypeDict, nodeDict, edgeDict, startList, targetList) -> DSAGraph:
    try:
        newGraph = DSAGraph(100000, 100000) # automatic resize supressed in MinHeap class. Maxmium 100000 nodes and 100000 edges

        with open(f"{inFileName}", 'r') as dataFile:

            for line in dataFile:
                dataLine = line.strip().split(" ")
                
                # Read Node Types
                if dataLine[0] == "Ncode": # store NCode in hash dictionary
                    tableKey = dataLine[1] # node type label
                    tableValue = dataLine[2] #node weight
                    try:
                        nodeTypeDict.put(tableKey, int(tableValue))
                    except Exception as err:
                        raise err

                # Read Edge Types
                elif dataLine[0] == "Ecode": # store NCode in hash dictionary
                    tableKey = dataLine[1]
                    tableValue = dataLine[2]
                    try:
                        edgeTypeDict.put(tableKey, int(tableValue))
                    except Exception as err:
                        raise err

                # Read Nodes
                elif dataLine[0] == "Node":
                    vertexLabel = dataLine[1]
                    vertexValue = nodeTypeDict.get(dataLine[2])
                    try:
                        nxGraph.add_node(vertexLabel) # display graph
                        newGraph.addVertex(vertexLabel, vertexValue) # vertex holds label and vertex weight (from vertex type)
                        nodeDict.put(vertexLabel, dataLine[2]) # node dictionary holds vertex label and vertex label type
                    except Exception as err:
                        raise err
                
                # Read Edges
                elif dataLine[0] == "Edge":
                    fromVertexLabel = dataLine[1]
                    toVertexLabel = dataLine[2]
                    weight = edgeTypeDict.get(dataLine[3])
                    
                    try:
                        newGraph.addEdge(fromVertexLabel, toVertexLabel, weight)
                        nxGraph.add_edge(fromVertexLabel, toVertexLabel, weight=weight) # Graphing Display
                        edgeDict.put(f"{fromVertexLabel} {toVertexLabel}", dataLine[3]) # edge dictionary holds edge label and edge label type

                    except Exception as err:
                        raise err

                elif dataLine[0] == "Start":
                    try:
                        startList.insertLast(dataLine[1]) # hold start in linked list, potential future implementation for multiple starts
                    except Exception as err:
                        raise err

                elif dataLine[0] == "Target":
                    try:
                        targetList.insertLast(dataLine[1]) # hold start in linked list for multiple targets
                    except Exception as err:
                        raise err

    except OSError as err: # OSError includes FileNotFound, IOError, etc...
        raise err
    return newGraph

# Update networkx Graph based on changes in DSA Graph
def updateGraph(graphStorage, nxGraph, edgeTypeDict, edgeDict) -> DSAGraph:
    nxGraph.clear()
    for vertex in graphStorage._vertices:
        vertexLabel = vertex.getLabel() # str
        nxGraph.add_node(vertexLabel)


    for edge in graphStorage._edges:
        edgeFrom = edge.getFromVertex().getLabel() # str
        edgeTo = edge.getToVertex().getLabel() # str
        # get Weights
        edgeTypeLabel = edgeDict.get(f"{edgeFrom} {edgeTo}") # str 
        edgeWeight = edgeTypeDict.get(edgeTypeLabel) # int
    
        nxGraph.add_edge(edgeFrom, edgeTo, weight=edgeWeight) # Graphing Display

# Display all routes
def displayRoutes(routeStorage, graphStorage, targetVertexLabel) -> None:
    routeList = routeStorage.get(targetVertexLabel)

    print(f"   |   Displaying routes to target: {graphStorage.getVertex(targetVertexLabel)}... ")
    print("   |")
    for count, route in enumerate(routeList):
        out = ""
        for node in route:
            out += f"{node}, "
        print(f"   |   [{count + 1}] Weight: {graphStorage.getRouteWeight(route)} Route: {out}")
                      
# Pseudo Interpreter - modified version from Prac05 test harness
def pseudoInterpreter(inputCall) -> DSAQueue:
    returnQueue = DSAQueue()

    funcName, funcArgs = "", ""
    try:
        index = 0
        if "(" in inputCall and ")" in inputCall: # seperate parenthesis

            while inputCall[index] != "(":
                funcName += inputCall[index] # extract function name
                index +=1

            index += 1
            
            while inputCall[index] != ")":
                funcArgs += inputCall[index] # extract arguments
                index +=1
            
            returnQueue.enqueue(funcName) # add function name to queue

            if funcArgs != "" and funcArgs and "," in funcArgs: # split arguments
                splitArgs = funcArgs.strip().split(",")
                for arg in splitArgs:

                    newArg = arg
                    if "\'" in arg:
                        newArg = arg.strip("\'")
                    elif "\"" in arg:
                        newArg = arg.strip("\"")

                    returnQueue.enqueue(newArg) # if multiple arguments
            elif funcArgs != "":
                returnQueue.enqueue(funcArgs) # if one argument
            
        else:
            print(f"   |   '{inputCall}' is not a valid method call. Methods require parenthesis.")
            raise Exception
                    
    except Exception as err:
        raise err
    
    return returnQueue # queue is structured information in the format;  [1]:funcName, [2]:arg1, [3]:arg2, [4]:arg3, etc...





# ===== MAIN ===== #

def main() -> None:


    # --------- VARIABLES --------- #    
    graphStorage = None # Hold the graph
    routeStorage = DSAHashTable(5) # heap containing routes (linked list) that contain paths(linked list)

    nodeTypeDictionary = DSAHashTable(5) # Stores all nodes type labels (i.e. "-") and it's weight (integer)
    edgeTypeDictionary = DSAHashTable(5) # Stores all edge type labels (i.e. "-") and it's weight (integer)

    nodeDictionary = DSAHashTable(5) # Stores all nodes labels (i.e. "A") and it's node type (i.e. "-")
    edgeDictionary = DSAHashTable(5) # Stores all edge information (i.e. "A B") and it's edge type (i.e. "-")

    startList = DSALinkedList() # Stores all START node labels. Implementation for multiple targets.
    targetList = DSALinkedList() # Stores all TARGET node labels. Implementation for multiple targets.
    
    nxDiGraph = nx.DiGraph() # Visualisation
    fileName = None 

    
    # --------- PROGRAM START --------- #

    # Manage invalid command line arguments
    if len(sys.argv) == 1:
        print("\n\033[1m# ===== gameofcatz.py ===== #\033[0m\n")
        printProgramRequirements()
        printProgramUsage()

    # manage interative mode and simulation mode args. 
    elif (len(sys.argv) != 2 and sys.argv[1] == "-i") or (len(sys.argv) != 4 and sys.argv[1] == "-s"):
        print("\n\033[1;91mInvalid command line argument!")
        printProgramUsage()

    elif (sys.argv[1] != "-s" and sys.argv[1] != "-i"):
        print("\n\033[1;91mInvalid command line argument!")
        printProgramUsage()


    # --------- CORE --------- #
    else:

        # --------- Interactive Mode --------- #
        if sys.argv[1] == "-i":

            menuModeInput = menuMode(fileName)
            while menuModeInput != "X" and menuModeInput != "EXIT()": # exit commands
                
                
                # ------ Load input file ------ #
                if menuModeInput == "1":
                    print("   |   \033[1m> Load Input File <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")
                    fileName = input("   |   Please enter file name WITH extension: ")

                    # RESET ALL DATA WHEN LOADING FILE IF DATA EXISTS
                    nxDiGraph = nx.DiGraph()
                    graphStorage = None
                    routeStorage = DSAHashTable(5) # heap containing routes (linked list) that contain paths(linked list)
                    nodeTypeDictionary = DSAHashTable(5) # Stores all nodes type labels. 
                    edgeTypeDictionary = DSAHashTable(5) # Stores all edge type labels
                    nodeDictionary = DSAHashTable(5) # Stores all nodes labels labels 
                    edgeDictionary = DSAHashTable(5) # Stores all edge information
                    startList = DSALinkedList()
                    targetList = DSALinkedList() # Stores all TARGET node labels. Implementation for multiple targets.

                    # These are required in case of over-"reading". prev graphs routes != new loaded graph's routes
                    # Same with nodeDict, edgeDict and targetLis, etc...

                    try: 
                        print(f"   |   Reading {fileName} now...")

                        graphStorage = readInputFile(fileName, nxDiGraph, nodeTypeDictionary, edgeTypeDictionary, 
                                                                    nodeDictionary, edgeDictionary, startList, targetList)
                        print("   |   File read successful!")

                    except Exception as err:
                    # RESET ALL DATA IF FILE NOT FOUND
                        fileName = None
                        nxDiGraph = nx.DiGraph()
                        graphStorage = None
                        routeStorage = DSAHashTable(5) # heap containing routes (linked list) that contain paths(linked list)
                        nodeTypeDictionary = DSAHashTable(5) # Stores all nodes type labels. 
                        edgeTypeDictionary = DSAHashTable(5) # Stores all edge type labels
                        nodeDictionary = DSAHashTable(5) # Stores all nodes labels labels 
                        edgeDictionary = DSAHashTable(5) # Stores all edge information
                        startList = DSALinkedList()
                        targetList = DSALinkedList() # Stores all TARGET node labels. Implementation for multiple targets.
                        print(f"   |   {err}")
                        print(f"   |   Error: File has not been read!")
                
                # ------ Node Operations ------ #
                elif menuModeInput == "2":
                    print("   |   \033[1m> Node Operations <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")
                    
                    if graphStorage != None:

                        whiteListedNodeOp = np.array(("getVertex", "hasVertex", "removeVertex", "getVertexCount", "displayAsList", "addVertex", "updateCode"))

                        print("   |   Enter node operation functions to run.")
                        print("   |   i.e. addVertex(5 , 1)")
                        print("   |   Note that deleting/adding nodes may also alter edges. Available node operations:")
                        print("   |   \033[94mgetVertex(\033[33mlabel\033[94m)\033[0m, \033[94mhasVertex(\033[33mlabel\033[94m)\033[0m, \033[94mremoveVertex(\033[33mlabel\033[94m)\033[0m")
                        print("   |   \033[94mgetVertexCount(), \033[94mdisplayAsList(), \033[94maddVertex(\033[33mlabel\033[94m, \033[33mweightCode\033[94m)\033[0m")
                        print("   |   \033[94mupdateCode(\033[33mnode\033[94m, \033[33mnewCode\033[94m)\033[0m")
                        print("   |   The following are node types (for adding vertices) presented in the format: (Code, Weight)")
                        print("   |   ")
                        print(f"   |   Node Types: {nodeTypeDictionary.export()}")
                        print("   |   Enter node operation functions to run. Call exit() to return to menu.")
                        print("   |   ")
                        print("   |   \033[1m# ---  Pseudo Interpreter  --- #\033[0m")

                        inputCall = input("   |   \n   |   >>> ")

                        while inputCall != "exit()": # My "pseudo interpreter". Partly borrowed from Prac05 Test Harness
                            try:
                                interpretInput = pseudoInterpreter(inputCall)
                                numberOfArgs = interpretInput.getCount() - 1
                                funcName = interpretInput.dequeue() # first is always funcName, string type
                                #format;  [1]:funcName, [2]:arg1, [3]:arg2, [4]:arg3, etc...

                                if hasattr(graphStorage, funcName) and funcName in whiteListedNodeOp: # white listed = able to run
                                    func = getattr(graphStorage, funcName)
                                    # no params
                                    if (numberOfArgs == 0) and (funcName == "getVertexCount" or funcName == "displayAsList"):
                                        try:
                                            retVal = func.__call__() # try call function
                                            if retVal != None:
                                                print(f"   |   {retVal}")
                                        except Exception as err:
                                            raise err
                                    
                                    # 1 params
                                    elif (numberOfArgs == 1) and (funcName == "getVertex" or funcName == "hasVertex"):
                                        funcArg1 = interpretInput.dequeue().strip() # strip for precaution argument may arrive as " a" with space character.
                                        try:
                                            retVal = func.__call__(funcArg1)  # try call function with args
                                            if retVal != None:
                                                print(f"   |   {retVal}")
                                        except Exception as err:
                                            raise err

                                    elif (numberOfArgs == 1) and (funcName == "removeVertex"):
                                        funcArg1 = interpretInput.dequeue().strip()

                                        if funcArg1 in targetList or funcArg1 in startList:
                                            raise ValueError("Unabled to delete, node is binded to Target/Start type.")

                                        try:
                                            retVal = func.__call__(funcArg1) # try call function with args, requires nodeDictionary modification
                                            # so that data between graph object and this script remains alligned.
                                            nodeDictionary.remove(funcArg1)

                                            # remove vertices means removing adjacent edges.
                                            for element in edgeDictionary.hashArray: # remove the edge
                                                if element != None and element.getKey() != "":
                                                    edge = element.getKey().split(" ") # edge key is stored in str format "{fromvertex} {tovertex}"

                                                    if edge[0] == funcArg1 or edge[1] == funcArg1:
                                                        edgeDictionary.remove(f"{element.getKey()}")

                                            if retVal != None:
                                                print(f"   |   {retVal}")
                                        except Exception as err:
                                            raise err
                                    
                                    # 2 params
                                    elif (numberOfArgs == 2) and (funcName == "addVertex"):
                                        funcArg1 = interpretInput.dequeue().strip()
                                        funcArg2 = interpretInput.dequeue().strip() 
                                        
                                        try:
                                            if nodeTypeDictionary.get(funcArg2) != None:
                                                nodeDictionary.put(funcArg1, funcArg2) # adjust local data.
                                                retVal = func.__call__(funcArg1, nodeTypeDictionary.get(funcArg2)) # call add vertex
                                            else:
                                                raise ValueError(f"{nodeTypeDictionary.get(funcArg2)} not a valid vertex type!")
                                            if retVal != None:
                                                print(f"   |   {retVal}")
                                        except Exception as err:
                                            raise err    
                                    
                                    else:
                                        raise ValueError("Invalid arguments!")
                                
                                # Custom pseudo function (not in DSAGraph)
                                elif (numberOfArgs == 2) and (funcName == "updateCode"): # update code value
                                    nodeLabel = interpretInput.dequeue().strip()
                                    newCode = interpretInput.dequeue().strip()
                                    try:
                                        if not nodeTypeDictionary.hasKey(newCode):
                                            raise ValueError(f"{newCode} not in node type dictionary!")
                                        
                                        node = graphStorage.getVertex(nodeLabel)
                                        nodeDictionary.getEntry(nodeLabel).setValue(newCode)
                                        weight = nodeTypeDictionary.get(newCode)
                                        node.setValue(weight)

                                        print(f"   |   Updated node {nodeLabel}'s weight code to {newCode}")
                                        print(f"   |   Node :{node}")

                                    except Exception as err:
                                        raise err
                                
                                else:
                                    raise ValueError(f"'{funcName}' is not a valid method.")  

                            except Exception as err:
                                print(f"   |   {err}")
                                print("   |   Error, method has not been called")
                            inputCall = input("   |   \n   |   >>> ")

                        print("   |   Exiting pseudo-interpreter for node operations!")
                    else:
                        print("   |   Graph not found! Please use option 1 in the menu to load input file first.")

                
                # ------ Edge Operations ------ #
                elif menuModeInput == "3": 
                    print("   |   \033[1m> Edge Operations <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")
                    
                    if graphStorage != None:
                        whiteListedEdgeOp = np.array(("getEdge", "getEdgeCount", "hasEdge", "displayAsList", "removeEdge", "updateCode", "addEdge", "breadthFirstSearch", "depthFirstSearch"))

                        print("   |   Enter node operation functions to run.")
                        print("   |   i.e. addVertex(5 , 1)")
                        print("   |   Note that deleting/adding nodes may also alter edges. Available node operations:")
                        print("   |   \033[94mgetEdge(\033[33mlabel\033[94m)\033[0m, \033[94mhasEdge(\033[33mfromLabel\033[94m, \033[33mtoLabel\033[94m)\033[0m, \033[94mremoveEdge(\033[33mfromLabel\033[94m, \033[33mtoLabel\033[94m)\033[0m")
                        print("   |   \033[94mgetEdgeCount()\033[0m, \033[94mdisplayAsList()\033[0m, \033[94maddEdge(\033[33mfromLabel\033[94m, \033[33mtoLabel\033[94m, \033[33mweightCode\033[94m)\033[0m")
                        print("   |   \033[94mupdateCode(\033[33mfromLabel\033[94m, \033[33mtoLabel\033[94m, \033[33mnewCode\033[94m)\033[0m, \033[94mdepthFirstSearch(\033[33mstartLabel\033[94m)\033[0m, \033[94mbreadthFirstSearch(\033[33mstartLabel\033[94m)\033[0m")
                        print("   |   The following are node types (for adding vertices) presented in the format: (Code, Weight)")
                        print("   |   ")
                        print(f"   |   Edge Types: {edgeTypeDictionary.export()}")
                        print("   |   Enter node operation functions to run. Call exit() to return to menu.")
                        print("   |   ")
                        print("   |   \033[1m# ---  Pseudo Interpreter  --- #\033[0m")

                        inputCall = input("   |   \n   |   >>> ")

                        while inputCall != "exit()": # My "pseudo interpreter". Partly borrowed from Prac05 Test Harness
                            try:
                                interpretInput = pseudoInterpreter(inputCall)
                                numberOfArgs = interpretInput.getCount() - 1
                                funcName = interpretInput.dequeue() # first is always funcName, string type

                                if hasattr(graphStorage, funcName) and funcName in whiteListedEdgeOp:
                                    func = getattr(graphStorage, funcName)
                                    # no params
                                    if (numberOfArgs == 0) and (funcName == "getEdgeCount" or funcName == "displayAsList"):
                                        try:
                                            retVal = func.__call__() # try call the function
                                            if retVal != None:
                                                print(f"   |   {retVal}")
                                        except Exception as err:
                                            raise err
                                    
                                    # 1 params
                                    elif (numberOfArgs == 1) and (funcName == "depthFirstSearch" or funcName == "breadthFirstSearch"):
                                        funcArg1 = interpretInput.dequeue().strip()
                                        try:
                                            retVal = func.__call__(funcArg1) # try call the function with args
                                            if retVal != None:
                                                out = ""
                                                for index in retVal:
                                                    out += f"{index} "
                                                print(f"   |   {out}")

                                        except Exception as err:
                                            raise err
                                    
                                    # 2 params
                                    elif (numberOfArgs == 2) and (funcName == "getEdge" or funcName == "hasEdge"):
                                        funcArg1 = interpretInput.dequeue().strip()
                                        funcArg2 = interpretInput.dequeue().strip()

                                        try:
                                            retVal = func.__call__(funcArg1, funcArg2) # try call the function with two args
                                            if retVal != None:
                                                print(f"   |   {retVal}")
                                        except Exception as err:
                                            raise err

                                    elif (numberOfArgs == 2) and (funcName == "removeEdge"):
                                        funcArg1 = interpretInput.dequeue().strip()
                                        funcArg2 = interpretInput.dequeue().strip()

                                        try:
                                            retVal = func.__call__(funcArg1, funcArg2) # try call the function with two args
                                            edgeDictionary.remove(f"{funcArg1} {funcArg2}") # remove from the local dictionary

                                            if retVal != None:
                                                print(f"   |   {retVal}")
                                        except Exception as err:
                                            raise err
                                    
                                    # 3 params
                                    elif (numberOfArgs == 3) and (funcName == "addEdge"):
                                        funcArg1 = interpretInput.dequeue().strip()
                                        funcArg2 = interpretInput.dequeue().strip()
                                        funcArg3 = interpretInput.dequeue().strip()

                                        try:
                                            if edgeTypeDictionary.get(funcArg3) != None:
                                                edgeDictionary.put(f"{funcArg1} {funcArg2}", funcArg3) # add into the local dictionary
                                                retVal = func.__call__(funcArg1, funcArg2, edgeTypeDictionary.get(funcArg3)) # try call the function to add edge
                                            else:
                                                raise ValueError(f"{edgeTypeDictionary.get(funcArg3)} not a valid edge type!")
                                            if retVal != None:
                                                print(f"   |   {retVal}")
                                        except Exception as err:
                                            raise err    
                                    
                                    else:
                                        raise ValueError("Invalid arguments!")
                                
                                # Custom pseudo function (not in DSAGraph)
                                elif (numberOfArgs == 3) and (funcName == "updateCode"):
                                    nodeFromLabel = interpretInput.dequeue().strip()
                                    nodeToLabel = interpretInput.dequeue().strip()
                                    newCode = interpretInput.dequeue().strip()
                                    try:
                                        if not edgeTypeDictionary.hasKey(newCode):
                                            raise ValueError(f"{newCode} not in node type dictionary!")
                                        
                                        edge = graphStorage.getEdge(nodeFromLabel, nodeToLabel)
                                        edgeDictionary.getEntry(f"{nodeFromLabel} {nodeToLabel}").setValue(newCode) # update the code of the edge. 
                                        # Note: Code != Weight. code is used to access weight value
                                        weight = edgeTypeDictionary.get(newCode)
                                        edge.setWeight(weight)

                                        print(f"   |   Updated edge {nodeFromLabel}-{nodeToLabel}'s weight code to {newCode}")
                                        print(f"   |   Edge :{edge}")

                                    except Exception as err:
                                        raise err
                                
                                else:
                                    raise ValueError(f"'{funcName}' is not a valid method.")  

                            except Exception as err:
                                print(f"   |   {err}")
                                print("   |   Error, method has not been called")
                            inputCall = input("   |   \n   |   >>> ")
                        
                        print("   |   Exiting pseudo-interpreter for edge operations!")
                    else:
                        print("   |   Graph not found! Please use option 1 in the menu to load input file first.")
                
                
                # ------ Parameter Tweaks ------ #
                elif menuModeInput == "4": 
                    print("   |   \033[1m> Parameter Tweaks <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")
                    
                    if graphStorage != None:
                        print("   |   The following are paramaters stored in dictionaries")
                        print(f"   |   Node Types: {nodeTypeDictionary.export()}")
                        print(f"   |   Edge Types: {edgeTypeDictionary.export()}")
                        
                        out = ""
                        for index in startList:
                            out += f"{index}, "
                        print(f"   |   Start Nodes: {out}")
                        
                        out = ""
                        for index in targetList:
                            out += f"{index} "
                        print(f"   |   Target Nodes: {out}")
                        print("   |   ")
                        print("   |   Please call the following functions, this feature only lets you edit the above parameters:")
                        print("   |   \033[94msetNodeWeight(\033[33mnodeCode\033[0m\033[94m, \033[33mnewValue\033[0m\033[94m)\033[0m to edit weight of each node type")
                        print("   |   \033[94msetEdgeWeight(\033[33medgeCode\033[0m\033[94m, \033[33mnewValue\033[0m\033[94m)\033[0m to edit weight of each edge type")
                        print("   |   \033[94maddNewTarget(\033[33mTarget\033[0m) to add a new Target")
                        print("   |   \033[94msetNewStart(\033[33mStart\033[0m) to change the current Start value")

                        print("   |   \033[94mprintAll()\033[0m print all node types and edge types")
                        print("   |   \033[94mexit()\033[0m to return to the menu")
                        print("   |   ")
                        print("   |   Example: setNodeWeight(B, 5). This sets node B's weight to 5")
                        print("   |   ")

                        print("   |   \033[1m# ---  Pseudo Interpreter  --- #\033[0m")

                        inputCall = input("   |   \n   |   >>> ")

                        while inputCall != "exit()": # My "pseudo interpreter". Partly borrowed from Prac05 Test Harness (modified)
                            
                            try:
                                interpretInput = pseudoInterpreter(inputCall)
                                numberOfArgs = interpretInput.getCount() - 1 
                                # number of args is always input count - 1 as  first ias always funcName
                                funcName = interpretInput.dequeue() # first is always funcName

                                # Custom Pseudo Functions 
                                if funcName == "printAll": 
                                    print(f"   |   Nodes: {nodeTypeDictionary.export()}")
                                    print(f"   |   Edges: {edgeTypeDictionary.export()}")
                                    out = ""
                                    for index in startList:
                                        out += f"{index}, "
                                    print(f"   |   Start Nodes: {out}")
                                    out = ""
                                    for index in targetList:
                                        out += f"{index} "
                                    print(f"   |   Target Nodes: {out}")

                                elif numberOfArgs == 2: 
                                    arg0 = interpretInput.dequeue() # first argument
                                    arg1 = interpretInput.dequeue() # second argument
                                    
                                    codeArg = arg0.strip()
                                    #print(codeArg)
                                    valueArg = arg1.strip()
                                    #print(valueArg)
                                    
                                    # Pseudo function to set the weight of corresponding node supplied in argument
                                    if funcName == "setNodeWeight": 
                                        
                                        nodeTypeDictionary.getEntry(codeArg).setValue(int(valueArg)) # update local dictionary
                                        for vertexEntry in nodeDictionary.hashArray:
                                            if vertexEntry != None:
                                                if vertexEntry.getValue() == codeArg:
                                                    graphStorage.getVertex(vertexEntry.getKey()).setValue(nodeTypeDictionary.get(codeArg)) 
                                                    # update key's value in DSAGraph

                                        routeStorage = DSAHashTable(5)
                                        updateGraph(graphStorage, nxDiGraph, edgeTypeDictionary, edgeDictionary)
                                        print(f"   |   Set Node: {codeArg}'s weight to {valueArg}")


                                    # Pseudo function to set the weight of corresponding edge supplied in argument
                                    elif funcName == "setEdgeWeight": 
                                        edgeTypeDictionary.getEntry(codeArg).setValue(int(valueArg)) # update local dictionary
                                        for edgeEntry in edgeDictionary.hashArray:
                                            if edgeEntry != None:
                                                if edgeEntry.getValue() == codeArg:
                                                    vertexLabels = edgeEntry.getKey().split(" ") # edge key is in form "{fromKey} {toKey}"
                                                    graphStorage.getEdge(vertexLabels[0], vertexLabels[1]).setWeight(edgeTypeDictionary.get(codeArg)) 
                                                    # update key's Value in DSAGraph
                                        
                                        routeStorage = DSAHashTable(5) # reset route storage, route needs to be regenerated to be up to date with new params
                                        updateGraph(graphStorage, nxDiGraph, edgeTypeDictionary, edgeDictionary) # update networkX graph
                                        print(f"   |   Set Edge: {codeArg}'s weight to {valueArg}")

                                    else:
                                        raise ValueError("Invalid method!")

                                # changes the value in startList
                                # list is used for possible future implementation of multiple starting points
                                elif funcName == "setNewStart": 
                                    arg0 = interpretInput.dequeue() # second argument
                                    startList.removeLast()
                                    startList.insertLast(arg0)

                                # adds to targetList. User can pick between these targets when displaying routes
                                elif funcName == "addNewTarget":
                                    arg0 = interpretInput.dequeue() # second argument
                                    targetList.insertLast(arg0)

                                else:
                                    raise ValueError("Invalid method or arguments!")
                                
                            except Exception as err:
                                print(f"   |   {err}")
                                print("   |   Error, method has not been called")
                            inputCall = input("   |   \n   |   >>> ")

                        print("   |   Exiting pseudo-interpreter for parameter tweaks!")
                    else:
                        print("   |   Graph not found! Please use option 1 in the menu to load input file first.")
                

                # ------ Display Graph ------ #
                elif menuModeInput == "5":
                    print("   |   \033[1m> Display Graph <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")
                    if graphStorage != None:

                        matrix = graphStorage.getMatrix()
                        matrixSize = graphStorage.getVertexCount() + 1
                        
                        for row in range(matrixSize):
                            output = ""
                            for col in range(matrixSize):
                                output += f"{matrix[row][col]} "
                            print(f"   |   {output}")

                        print("   |   ")
                        saveOption = input("   |   Save matrix to file (Y/N)? ").upper()

                        if saveOption == "Y":
                            print("   |   ")
                            outputFileName = input("   |   Please enter file name without extension: ")
                            with open(f"{outputFileName}.txt","w") as outputFile:

                                for row in range(matrixSize):
                                    output = ""
                                    for col in range(matrixSize):
                                        output += f"{matrix[row][col]} "
                                    outputFile.write(f"{output}\n")
                            print(f"   |   Matrix written to file '{outputFileName}.txt'!")
                    else:
                        print("   |   Graph not found! Please use option 1 in the menu to load input file first.")


                # ------ Display World ------ #
                elif menuModeInput == "6":
                    print("   |   \033[1m> Display World <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")
                    if graphStorage != None:
                        


                        # -- Print statistics -- #
                        
                        print(f"   |   Total number of vertices: {graphStorage.getEdgeCount()}")
                        print(f"   |   Total number of edges: {graphStorage.getVertexCount()}")
                        print(f"   |   Node Types (Node, Weight): {nodeTypeDictionary.export()}")
                        print(f"   |   Edge Types (Edge, Weight): {edgeTypeDictionary.export()}")
                        print("   |   ")
                        
                        # print the amount of times a node type appears in node dictionary
                        for nodeElement in nodeTypeDictionary.hashArray: # iterate through dictionary
                            if nodeElement.getState() == 1:
                                count = 0
                                nodeTypeName = nodeElement.getKey()

                                for node in nodeDictionary.hashArray:
                                    if node.getValue() == nodeTypeName:
                                        count += 1
                                
                                print(f"   |   Number of times node type '{nodeTypeName}' is found: {count}")
                        
                        # print the amount of times an edge type appears in edge dictionary
                        for edgeElement in edgeTypeDictionary.hashArray:
                            if edgeElement.getState() == 1:
                                count = 0
                                edgeTypeName = edgeElement.getKey()

                                for edge in edgeDictionary.hashArray:
                                    if edge.getValue() == edgeTypeName:
                                        count += 1
                                
                                print(f"   |   Number of times edge type '{edgeTypeName}' is found: {count}")

                        # Plot the grapg and show it. NetworkX and matplotlib may present a 3D form of the graph when using plt.show()
                        # hence different settings are used when compared to saving the plot.
                        pos = nx.spring_layout(nxDiGraph, k=0.3, iterations=90)                        
                        labels = nx.get_edge_attributes(nxDiGraph,'weight')
                        nx.draw_networkx_edge_labels(nxDiGraph , pos, edge_labels=labels, font_size=10)
                        nx.draw(nxDiGraph, pos, node_color="#A0CBE2", node_size=400, with_labels=True, font_size=10, 
                                                            arrowstyle="->", linewidths=1, edge_color="black",width=1)
                        plt.show()

                        saveOption = input("   |   Save graph to file (Y/N)? ").upper()

                        if saveOption == "Y":
                            plt.cla()
                            # reset the plot and plot the graph again so it appears better in 2D format
                            print("   |   ")
                            outputFileName = input("   |   Please enter file name without extension: ")
                            
                            nxDiGraph.clear()
                            updateGraph(graphStorage, nxDiGraph, edgeTypeDictionary, edgeDictionary)
                            pos = nx.spring_layout(nxDiGraph, k=0.3, iterations=90)

                            labels = nx.get_edge_attributes(nxDiGraph,'weight')
                            nx.draw_networkx_edge_labels(nxDiGraph , pos, edge_labels=labels, font_size=3)
                            nx.draw(nxDiGraph, pos, node_color="#A0CBE2", node_size=30, with_labels=True, font_size=4, 
                                                            arrowstyle="->", arrowsize =5, linewidths=0.5, edge_color="black",width=0.5)
                            
                            plt.savefig(f"{outputFileName}.png", dpi=600)
                            print(f"   |   Graph saved to file as '{outputFileName}.png'!")
                    else:
                        print("   |   Graph not found! Please use option 1 in the menu to load input file first.")


                # ------ Generate Routes ------ #
                elif menuModeInput == "7":
                    print("   |   \033[1m> Generate Routes <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")
                    if graphStorage != None:
                        

                        updateGraph(graphStorage, nxDiGraph, edgeTypeDictionary, edgeDictionary)
                        print("   |   Note: Route generation times highly depends on the complexity of the graph. ")
                        print("   |   As the complexity of the graph increases (number of nodes -> inf, number of edges -> inf), there will be more permutations of paths.") 
                        print("   |   Recommendation: generate less routes for any highly complex graph unless all routes are needed. ")
                        print("   |   To generate all routes, enter a large number. ")

                        numRoutesToGen = int(input("   |   Please enter maximum amount of routes to generate: "))
                        print("   |   ")

                        routeStorage = DSAHashTable(5)
                        startVertexLabel = startList.peekFirst() # assumed 1 start point (for now).
                        print(f"   |   Start vertex: {graphStorage.getVertex(startVertexLabel)}") 

                        for targetVertexLabel in targetList: # Generate route for every target
                            print(f"   |   Generating routes to target: {graphStorage.getVertex(targetVertexLabel)} ...")

                            # Call function from DSAGraph to generate routes, stored in routeStorage
                            routeStorage.put(targetVertexLabel, graphStorage.generateRoutes(startVertexLabel, targetVertexLabel, numRoutesToGen)) 

                        print("   |   Routes Generated!")
                    else:
                        print("   |   Graph not found! Please use option 1 in the menu to load input file first.")


                # ------ Display Routes ------ #
                elif menuModeInput == "8": 
                    print("   |   \033[1m> Display Routes <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")


                    if graphStorage == None: 
                        print("   |   Graph not found! Please use option 1 in the menu to load input file first.")
                    elif routeStorage.isEmpty(): # routes need to be generated First before using this feature
                        print("   |   Routes not found! Please use option 7 in the menu to generate routes first.")
                    else:
                        displayOption = input("   |   Would you like to display Routes (Y/N)? ").upper() 
                        if displayOption == "Y":
                            targetVertexLabel = targetList.peekFirst() 
                            print(f"   |   Start vertex: {graphStorage.getVertex(startVertexLabel)}")

                            if routeStorage.getCount() > 1: # i.e. if list has more than 1 item O(1) check
                                print("   |   ") 
                                print("   |   Multiple Targets Detected!") 
                                for target in targetList:
                                    print(f"   |   Target: {target}") 
                                # multiple targets implementation
                                routeOption = input("   |   Please select the target for the route (case sensitive): ")
                                if routeOption in targetList:
                                    displayRoutes(routeStorage, graphStorage, routeOption)
                                else:
                                    print("   |   Invalid route selected! Exiting Display Routes mode.")

                            else: # if just 1 target, display  the routes
                                displayRoutes(routeStorage, graphStorage, targetVertexLabel)
                        
                        print("   |   ") # routes saving
                        saveOption = input("   |   Save Route(s) to file (Y/N)? ").upper()

                        if saveOption == "Y":
                            outputFileName = input("   |   Please enter output file name without extension: ")

                            routeList = routeStorage.get(targetVertexLabel)

                            print("   |   Saving routes... ")
                            with open(f"{outputFileName}.txt","w") as outputFile: # write the routes to an output file

                                for count, route in enumerate(routeList):
                                    out = ""
                                    for node in route:
                                        out += f"{node}, "
                                    outputFile.write(f"Rank: {count + 1} Weight: {graphStorage.getRouteWeight(route)} Route: {out}\n")
                            print(f"   |   Routes have been saved to '{outputFileName}.txt'!")


                # ------ Save Network ------ #
                elif menuModeInput == "9": 
                    print("   |   \033[1m> Save Network <\033[0m")
                    print("   |   \033[1m------------------------------\033[0m\n   |")
                    if graphStorage != None:
                        outFileName = input("   |   Enter file name to output without extension: ")
                        with open(f"{outFileName}.txt","w") as outFile: 
                                
                            # SAVE NETWORK FEATURE, outputs in the same format as input files. This allows for the file to be read again with the new changes.
                            outFile.write(f"# {outFileName}\n")
                            outFile.write(f"# Node Types {nodeTypeDictionary.export()}\n")
                            # write every node type
                            for nodeTypeElement in nodeTypeDictionary.hashArray:
                                if nodeTypeElement.getState() == 1:
                                    outFile.write(f"Ncode {nodeTypeElement.getKey().strip()} {nodeTypeElement.getValue()}\n")
                            
                            outFile.write(f"# Define Node and Labels\n")
                            # write every node
                            for nodeElement in nodeDictionary.hashArray:
                                if nodeElement.getState() == 1: 
                                    outFile.write(f"Node {nodeElement.getKey()} {nodeElement.getValue()}\n")

                            outFile.write(f"# Edge Types {edgeTypeDictionary.export()}\n")
                            # write every edge type
                            for edgeTypeElement in edgeTypeDictionary.hashArray:
                                if edgeTypeElement.getState() == 1:
                                    outFile.write(f"Ecode {edgeTypeElement.getKey().strip()} {edgeTypeElement.getValue()}\n")

                            outFile.write(f"# Define Edges\n")
                            # write every edge
                            for edgeElement in edgeDictionary.hashArray:
                                if edgeElement.getState() == 1: 
                                    outFile.write(f"Edge {edgeElement.getKey()} {edgeElement.getValue()}\n")
                    
                            outFile.write(f"# Define Start and Target(s)\n")
                            # write start nodes
                            for start in startList:
                                outFile.write(f"Start {start}\n")
                            # write target nodes
                            for target in targetList:
                                outFile.write(f"Target {target}\n")

                        print(f"   |   Graph network saved to '{outFileName}.txt'. This file can be used again to read using this program. ")

                    else:
                        print("   |   Graph not found! Please use option 1 in the menu to load input file first.")


                print("   |   \n")
                menuModeInput = menuMode(fileName)


        # --------- Simulation Mode --------- #
        elif sys.argv[1] == "-s":
            fileName = sys.argv[2]
            outFileName = sys.argv[3]

            print("\n \033[1m# ------ Simulation Mode ------ #\033[0m \n")
            print(f"Reading {fileName} now...")

            nxDiGraph = nx.DiGraph()

            graphStorage = None

            routeStorage = DSAHashTable(100) # heap containing routes (linked list) that contain paths(linked list)
            nodeTypeDictionary = DSAHashTable(100) # Stores all nodes type labels. 
            edgeTypeDictionary = DSAHashTable(100) # Stores all edge type labels
            nodeDictionary = DSAHashTable(100) # Stores all nodes labels labels 
            edgeDictionary = DSAHashTable(100) # Stores all edge information
            startList = DSALinkedList()
            targetList = DSALinkedList() # Stores all TARGET node labels. Implementation for multiple targets.

            try:
                graphStorage = readInputFile(fileName, nxDiGraph, nodeTypeDictionary, edgeTypeDictionary, 
                                                            nodeDictionary, edgeDictionary, startList, targetList)
                
                print("File read successful!\n")

                
                startVertexLabel = startList.peekFirst() # assumed 1 start point.
                
                with open(f"{outFileName}.txt","w") as outputFile:

                    for targetVertexLabel in targetList:
                        # generate every route for every target
                        print(f"Start vertex: {graphStorage.getVertex(startVertexLabel)}")
                        print(f"Generating routes to target: {graphStorage.getVertex(targetVertexLabel)} ...")

                        routeList = graphStorage.generateRoutes(startVertexLabel, targetVertexLabel, defaultNumRoutes)


                        print(f"Saving routes to target {graphStorage.getVertex(targetVertexLabel)}...\n")

                        outputFile.write(f"\n\n# ========== Routes From {graphStorage.getVertex(startVertexLabel)} To {graphStorage.getVertex(targetVertexLabel)} ========== #\n\n")

                        # for every route, output to outputfile.
                        for count, route in enumerate(routeList):
                            out = ""
                            for node in route:
                                out += f"{node}, "
                            outputFile.write(f"Rank: {count + 1} Weight: {graphStorage.getRouteWeight(route)} Route: {out}\n")

                print(f"Routes have been saved to '{outFileName}.txt'!")
                print("Route generation complete!")
            
            except Exception as e:
                print(e)
                print("Error! File has not been read")

# --------- END MAIN --------- #




# ===== RUN MAIN ==== #
if __name__ == "__main__":
    main()
