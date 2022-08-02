# 
# CURTIN UNIVERISTY COMP1002 - Data Structures and Algorithms
# Assignment 1 - Linked List Classes (Modified for assignment from Prac 04)
#
# Author: Alastair Kho
# ID: 20214878
#

class DSAListNode():
    
    # -- Constructor -- #
    def __init__(self, inValue):
        self.value = inValue
        self.next = None
        self.prev = None

    # -- Accessor -- #
    def getValue(self):
        return self.value

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev

    # -- Mutator -- #
    def setValue(self, inValue):
        self.value = inValue

    def setNext(self, newNext):
        self.next = newNext

    def setPrev(self, newPrev):
        self.prev = newPrev

class DSALinkedList():

    # -- Constructor -- #
    def __init__(self):
        self.head = None
        self.tail = None
        
    # -- Accessors -- #
    def isEmpty(self):
        return True if (self.head == None and self.tail == None) else (False)
    
    def peekFirst(self):
        if self.isEmpty():
            raise Exception("Linked List is Empty!")
        else:
            return self.head.getValue()

    def peekLast(self):
        if self.isEmpty():
            raise Exception("Linked List is Empty!")
        else:
            currNode = self.head
            while currNode.getNext() != None:
                currNode = currNode.getNext()
            return currNode.getValue()

    # -- Mutators -- #
    def insertFirst(self, newValue):
        newNode = DSAListNode(newValue)
        if self.isEmpty():
            self.head = newNode
        
        else:
            newNode.setNext(self.head)
            self.head.setPrev(newNode)
            self.head = newNode

    def insertLast(self, newValue):
        newNode = DSAListNode(newValue)
        if self.isEmpty():
            self.head = newNode
        else:
            currNode = self.head
            while currNode.getNext() != None:
                currNode = currNode.getNext()
            currNode.setNext(newNode)
            newNode.setPrev(currNode)

    def removeFirst(self):
        if self.isEmpty():
            raise Exception("Linked List is Empty!")
        else:
            nodeValue = self.head.getValue()
            nextValue = self.head.getNext()
            if nextValue is not None:
                nextValue.setPrev(None)
                self.head = nextValue
            else:
                self.head = None
                self.tail = None

            return nodeValue

    def removeLast(self):
        if self.isEmpty():
            raise Exception("Linked List is Empty!")
        elif self.head.getNext() == None:
            nodeValue = self.head.getValue()
            self.head = None
            self.tail = None
            return nodeValue
        else:
            prevNode = None
            currNode = self.head
            while currNode.getNext() != None:
                prevNode = currNode
                currNode = currNode.getNext()
            prevNode.setNext(None)
            nodeValue = currNode.getValue()
            self.tail = prevNode
            return nodeValue   

    def __iter__(self):
        currNode = self.head
        while currNode is not None:
            yield currNode.getValue()
            currNode = currNode.getNext()    

    