# 
# CURTIN UNIVERISTY COMP1002 - Data Structures and Algorithms
# Assignment 1 - Queue Class (Linked List Implementation. Used for assignment from Prac 04)
#
# Author: Alastair Kho
# ID: 20214878
#

from LinkedListClasses import *


## ---- DSA QUEUE ---- ##
class DSAQueue:
    
    # -- Constructor -- #
    def __init__(self) -> None:
        self.linkedList = DSALinkedList()
        self.count = 0

    # -- Accessors -- #
    def getCount(self) -> int:
        return self.count

    def isEmpty(self) -> bool:
        return True if self.count == 0 else (False)
    
    # -- Mutators -- #
    def enqueue(self, value):
        self.linkedList.insertLast(value)
        self.count += 1
    
    def dequeue(self):
        peekFirst = None
        if not self.linkedList.isEmpty():
            self.count -= 1
            peekFirst = self.linkedList.peekFirst()
            self.linkedList.removeFirst()
        return peekFirst
    
    def __iter__(self):
        return self.linkedList.__iter__()


