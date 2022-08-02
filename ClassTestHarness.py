
#   Unit Test Framework ============================================ #
#
#   Methods within class test harnesses must be named in order of execution (i.e., case_1_test_name, case_2_test_name)
#   Methods which are tests cases must use assertEqual, assertNotEqual or raise Exception() when validating data
#   Print statements are disabled
#   Name of test harness is the name of the class
#   Process for each test case: Generate values, then validate values.
#
#   =================================================================#
# 
#   CURTIN UNIVERISTY COMP1002 - Data Structures and Algorithms
#   Test Harness File
#   Author: Alastair Kho
#   ID: 20214878
#

# ====== CORE MODULE ====== #
import UnitTestModule
# ========================= #


# ==== MODULES TO TEST ==== #
from MinHeap import *
from LinkedListClasses import *
from QueueClass import *
from HashTable import *
from DSAGraph import *
# ========================= #


# ==== CLASS ERRORS ==== #
class ListError(Exception):
    pass


# ==== HEAP TEST HARNESS ====#
class UnitTest_Heap(UnitTestModule.UnitTest):
    def __init__(self) -> None:
        self.testHeap = MinHeap(7)
        
    def case_1_Test_Heap_Is_Empty(self):
        self.assertEqual(self.testHeap.isEmpty(), True)
    
    def case_2_Test_Heap_Functional_Add(self):
        self.testHeap.add(6,1)
        self.assertEqual(self.testHeap.heapArray[0].getPriority(), 6)
        self.testHeap.add(5,1)
        self.testHeap.add(4,1)
        self.testHeap.add(3,1)
        self.testHeap.add(2,1)
        self.testHeap.add(1,1)
        self.testHeap.add(7,1)

    def case_3_Test_TrickleUp_Correct_Implementation_In_Add(self):
        # children always > parent
        self.assertEqual(self.testHeap.heapArray[0].getPriority(), 1)
        self.assertEqual(self.testHeap.heapArray[1].getPriority(), 3)
        self.assertEqual(self.testHeap.heapArray[2].getPriority(), 2)
        self.assertEqual(self.testHeap.heapArray[3].getPriority(), 6)
        self.assertEqual(self.testHeap.heapArray[4].getPriority(), 4)
        self.assertEqual(self.testHeap.heapArray[5].getPriority(), 5)
        self.assertEqual(self.testHeap.heapArray[6].getPriority(), 7)

    def case_4_Test_Heap_Is_Full(self):
        self.assertNotEqual(self.testHeap.isFull(), False)

    def case_5_Test_Heap_Functional_Remove(self):
        self.assertEqual(self.testHeap.remove(2).getPriority(), 2)

    def case_6_Test_TrickleDown_Correct_Implementation_In_Remove(self):
        # children always > parent
        self.assertEqual(self.testHeap.heapArray[0].getPriority(), 1)
        self.assertEqual(self.testHeap.heapArray[1].getPriority(), 3)
        self.assertEqual(self.testHeap.heapArray[2].getPriority(), 5)
        self.assertEqual(self.testHeap.heapArray[3].getPriority(), 6)
        self.assertEqual(self.testHeap.heapArray[4].getPriority(), 4)
        self.assertEqual(self.testHeap.heapArray[5].getPriority(), 7)
    
    def case_7_Test_Heap_Functional_And_Correct_Heap_Sorting_Algorithm(self):
        self.testHeap.heapSort()
        self.assertEqual(self.testHeap.heapArray[0].getPriority(), 1)
        self.assertEqual(self.testHeap.heapArray[1].getPriority(), 3)
        self.assertEqual(self.testHeap.heapArray[2].getPriority(), 4)
        self.assertEqual(self.testHeap.heapArray[3].getPriority(), 5)
        self.assertEqual(self.testHeap.heapArray[4].getPriority(), 6)
        self.assertEqual(self.testHeap.heapArray[5].getPriority(), 7)


# ==== LINKED LIST TEST HARNESS ====#
class UnitTest_Linked_List(UnitTestModule.UnitTest): # borrowed and modified from prac04 supplied testharness
    def __init__(self) -> None:
        self.ll = DSALinkedList()
        self.testString = ""

    def case_1_Normal_Conditions(self):
        self.ll = DSALinkedList()
        if (not self.ll.isEmpty()):
            raise ListError("Head must be None.")

    def case_2_Insert_First(self):
        self.ll.insertFirst("abc")
        self.ll.insertFirst("jkl")
        self.ll.insertFirst("xyz")

    def case_3_Iterator(self):
        temp = ""
        for i in self.ll:
            temp += f"{str(i)}, "
        if temp != "xyz, jkl, abc, ":
            raise ListError("Iterator failed")

    def case_4_Peek_First(self):
        self.testString = self.ll.peekFirst()
        if self.testString != "xyz":
            raise ListError("Peek First failed")

    def case_5_Remove_First(self):
        self.testString = self.ll.removeFirst()
        if self.testString != "xyz":
            raise ListError("Remove first failed")
        self.testString = self.ll.removeFirst()
        if self.testString != "jkl":
            raise ListError("Remove first failed")
        self.testString = self.ll.removeFirst()
        if self.testString != "abc":
            raise ListError("Remove first failed")

    def case_6_Remove_First_When_Empty(self):
        try:
            self.testString = self.ll.removeFirst()
            passed = False
        except Exception as e:
            passed = True

        if passed == False:
            raise ListError("Remove first when empty failed")

    def case_7_Insert_Last(self):
        self.ll.insertLast("abc")
        self.ll.insertLast("jkl")
        self.ll.insertLast("xyz")


# ==== QUEUE TEST HARNESS ====#
class UnitTest_Queue(UnitTestModule.UnitTest): # Linked List derivative
    def __init__(self) -> None:
        self.queue = DSAQueue()

    def case_1_Test_Normal_Conditions(self):
        self.assertEqual(self.queue.isEmpty(), True)

    def case_2_Test_Enqueue(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.queue.enqueue(4)

        self.assertEqual(self.queue.isEmpty(), False)
    
    def case_3_Test_Correct_Queue_Count(self):
        self.assertEqual(self.queue.getCount(), 4)

    def case_4_Test_Dequeue(self):
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)
        self.assertEqual(self.queue.dequeue(), 4)
        self.assertEqual(self.queue.getCount(), 0)
    
    def case_5_Test_Is_Empty(self):
        self.assertEqual(self.queue.isEmpty(), True)


# ==== HASH TEST HARNESS ====#
class UnitTest_Hash(UnitTestModule.UnitTest):
    def __init__(self) -> None:
        self.testHash = DSAHashTable(7)

    def case_1_Test_Normal_Conditions(self):
        self.assertEqual(len(self.testHash.hashArray), 11) # 11 because it resizes to next prime
        self.assertEqual(self.testHash.isEmpty(), True)

    def case_2_Test_Put_And_Resize(self):
        self.testHash.put("Alpha", 123)
        self.testHash.put("Yankee", 456)
        self.testHash.put("Hotel", 789)
        self.testHash.put("Zulu", 101112)

    def case_3_Test_Hash_Count(self):
        self.assertEqual(self.testHash.getCount(), 4)

    def case_4_Test_Valid_Keys(self):
        self.assertEqual(self.testHash.hasKey('Alpha'), True)
        self.assertEqual(self.testHash.hasKey('Yankee'), True)
        self.assertEqual(self.testHash.hasKey('Hotel'), True)
        self.assertEqual(self.testHash.hasKey('Zulu'), True)

        self.assertEqual(self.testHash.get('Alpha'), 123)
        self.assertEqual(self.testHash.get('Yankee'), 456)
        self.assertEqual(self.testHash.get('Hotel'), 789)
        self.assertEqual(self.testHash.get('Zulu'), 101112)

    def case_5_Test_Remove(self):
        self.testHash.remove("Yankee")
        self.testHash.remove("Hotel")
        self.testHash.remove("Zulu")

    def case_6_Test_Valid_Keys(self):
        self.assertEqual(self.testHash.hasKey('Alpha'), True)
        self.assertEqual(self.testHash.hasKey('Yankee'), False)
        self.assertEqual(self.testHash.hasKey('Hotel'), False)
        self.assertEqual(self.testHash.hasKey('Zulu'), False)

    def case_7_Test_Hash_Count_After_Remove(self):
        self.assertEqual(self.testHash.getCount(), 1)

    def case_8_Test_Array_Size_After_Remove(self):
        self.assertEqual(len(self.testHash.hashArray), 3)
        self.assertEqual(self.testHash.isEmpty(), False)

       
# ==== GRAPH TEST HARNESS ====#
class UnitTest_Graph(UnitTestModule.UnitTest):
    def __init__(self) -> None:
        self.testGraph = DSAGraph(5, 10)

    def case_1_Test_Normal_Conditions(self):
        self.assertEqual(self.testGraph.getVertexCount(), 0)
        self.assertEqual(self.testGraph.getEdgeCount(), 0)
    
    def case_2_Test_Add_Vertex(self):
        self.testGraph.addVertex("A", 1)
        self.testGraph.addVertex("B", 2)
        self.testGraph.addVertex("C", 3)
        self.testGraph.addVertex("D", 4)
        self.testGraph.addVertex("E", 5)
        self.assertEqual(self.testGraph._vertices.isFull(), True)
        self.assertEqual(self.testGraph.getVertexCount(), 5)
        self.assertEqual(self.testGraph.getEdgeCount(), 0)

    def case_3_Test_Vertex_Properties(self):
        self.assertEqual(self.testGraph.hasVertex("A"), True)
        self.assertEqual(self.testGraph.hasVertex("B"), True)
        self.assertEqual(self.testGraph.hasVertex("C"), True)
        self.assertEqual(self.testGraph.hasVertex("D"), True)
        self.assertEqual(self.testGraph.hasVertex("E"), True)

        self.assertEqual(self.testGraph.getVertex("A").getValue(), 1)
        self.assertEqual(self.testGraph.getVertex("B").getValue(), 2)
        self.assertEqual(self.testGraph.getVertex("C").getValue(), 3)
        self.assertEqual(self.testGraph.getVertex("D").getValue(), 4)
        self.assertEqual(self.testGraph.getVertex("E").getValue(), 5)

    def case_4_Test_Add_Directed_Edge(self):
        self.testGraph.addEdge("A", "B", 1)
        self.testGraph.addEdge("C", "E", 0)
        self.assertEqual(self.testGraph.getVertexCount(), 5)
        self.assertEqual(self.testGraph.getEdgeCount(), 2)

    def case_5_Test_Directed_Edge_Properties(self):
        self.assertEqual(self.testGraph.hasEdge("A", "B"), True)
        self.assertEqual(self.testGraph.hasEdge("C", "E"), True)

        self.assertEqual(self.testGraph.getEdge("A","B").getWeight(), 1)
        self.assertEqual(self.testGraph.getEdge("C", "E").getWeight(), 0)

        self.assertEqual(self.testGraph.hasEdge("B", "A"), False)
        self.assertEqual(self.testGraph.hasEdge("E", "C"), False)

        self.testGraph.addEdge("B", "A", 1)
        self.testGraph.addEdge("E", "C", 0)
        self.testGraph.addEdge("B", "D", 1), self.testGraph.addEdge("D", "B", 1)
        self.testGraph.addEdge("A", "D", 1), self.testGraph.addEdge("D", "A", 1)
        self.testGraph.addEdge("A", "E", 1)
        self.testGraph.addEdge("C", "B", 1)

        self.assertEqual(self.testGraph.hasEdge("B", "A"), True)
        self.assertEqual(self.testGraph.hasEdge("E", "C"), True)
        self.assertEqual(self.testGraph.hasEdge("B", "D"), True), self.assertEqual(self.testGraph.hasEdge("D", "B"), True)
        self.assertEqual(self.testGraph.hasEdge("A", "D"), True), self.assertEqual(self.testGraph.hasEdge("D", "A"), True)

        self.assertEqual(self.testGraph.hasEdge("A", "E"), True), self.assertEqual(self.testGraph.hasEdge("E", "A"), False)
        self.assertEqual(self.testGraph.hasEdge("C", "B"), True), self.assertEqual(self.testGraph.hasEdge("B", "C"), False)


    def case_6_Test_Breadth_First_Search(self):
        retVal = self.testGraph.breadthFirstSearch('E')
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "E"), self.assertEqual(edge.getToVertex().getLabel(), "C")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "C"), self.assertEqual(edge.getToVertex().getLabel(), "B")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "B"), self.assertEqual(edge.getToVertex().getLabel(), "A")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "B"), self.assertEqual(edge.getToVertex().getLabel(), "D")

        retVal = self.testGraph.breadthFirstSearch('A')
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "A"), self.assertEqual(edge.getToVertex().getLabel(), "B")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "A"), self.assertEqual(edge.getToVertex().getLabel(), "D")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "A"), self.assertEqual(edge.getToVertex().getLabel(), "E")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "E"), self.assertEqual(edge.getToVertex().getLabel(), "C")

    def case_7_Test_Depth_First_Search(self):
        retVal = self.testGraph.depthFirstSearch('E')
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "E"), self.assertEqual(edge.getToVertex().getLabel(), "C")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "C"), self.assertEqual(edge.getToVertex().getLabel(), "B")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "B"), self.assertEqual(edge.getToVertex().getLabel(), "A")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "A"), self.assertEqual(edge.getToVertex().getLabel(), "D")

        retVal = self.testGraph.depthFirstSearch('A')
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "A"), self.assertEqual(edge.getToVertex().getLabel(), "B")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "B"), self.assertEqual(edge.getToVertex().getLabel(), "D")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "A"), self.assertEqual(edge.getToVertex().getLabel(), "E")
        edge = retVal.dequeue()
        self.assertEqual(edge.getFromVertex().getLabel(), "E"), self.assertEqual(edge.getToVertex().getLabel(), "C")

    def case_8_Test_Route_Generation(self):
        retVal = self.testGraph.generateRoutes('E', 'A', 1)

        route = retVal.heapArray[0].getValue()
        vertex = route.removeFirst()
        self.assertEqual(vertex.getLabel(), "E")
        vertex = route.removeFirst()
        self.assertEqual(vertex.getLabel(), "C")
        vertex = route.removeFirst()
        self.assertEqual(vertex.getLabel(), "B")
        vertex = route.removeFirst()
        self.assertEqual(vertex.getLabel(), "A")

        retVal = self.testGraph.generateRoutes('D', 'C', 1)

        route = retVal.heapArray[0].getValue()
        vertex = route.removeFirst()
        self.assertEqual(vertex.getLabel(), "D")
        vertex = route.removeFirst()
        self.assertEqual(vertex.getLabel(), "A")
        vertex = route.removeFirst()
        self.assertEqual(vertex.getLabel(), "E")
        vertex = route.removeFirst()
        self.assertEqual(vertex.getLabel(), "C")


# ==== TEST HARNESS RUNNER ====#
if __name__ == "__main__":
    
    UnitTest_Heap().run()
    UnitTest_Linked_List().run()
    UnitTest_Queue().run()
    UnitTest_Hash().run()
    UnitTest_Graph().run()