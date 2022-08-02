# 
# CURTIN UNIVERISTY COMP1002 - Data Structures and Algorithms
# Assignment 1 - Min Heap Classes (Modified for assignment from Prac 07)
#
# Author: Alastair Kho
# ID: 20214878
#

import numpy as np

# Heap Entry Class
# Used by Heap class in a composition
class _HeapEntry:

    # --- Constructor --- #
    def __init__(self, inPriority, inValue) -> None:
        self.priority = inPriority
        self.value = inValue

    # --- Accessors --- #
    def getPriority(self) -> int:
        return self.priority

    def getValue(self) -> object:
        return self.value

    # --- Mutators --- #
    def setPriority(self, inPriority) -> None:
        self.priority = inPriority
    
    def setValue(self, inValue) -> None:
        self.value = inValue

    # --- Private --- #
    def __repr__(self) -> str:
        return f"<Object: {hex(id(self))} | priority: {self.priority} | value: {self.value}>"


# Heap Class
class MinHeap:

    # --- Constructor --- #
    def __init__(self, maxSize) -> None:
        self.heapArray = np.empty(maxSize, dtype=_HeapEntry)
        self.count = 0

    # --- Accessors --- #
    def getCount(self) -> int:
        return self.count
        
    def isFull(self) -> bool:
        retValue = False
        if len(self.heapArray) == self.count:
            retValue = True
        return retValue

    def isEmpty(self) -> bool:
        retValue = False
        if self.count == 0:
            retValue = True
        return retValue

    def displayHeapArray(self) -> None:
        output = ""
        for entry in self.heapArray:
            if type(entry) == _HeapEntry:
                output += f" {entry.getPriority()},"
            else:
                output += f" None,"
        print(output)
        
    # --- Mutators --- #
    """def _resizeHeapArray(self, size) -> None:

        oldArr = self.heapArray # store old array
        self.heapArray = np.empty(size, dtype=_HeapEntry) # reset Hash Array

        self.count = 0
        for oldEntry in oldArr:
            if oldEntry != None:
                self.add(oldEntry.getPriority(), oldEntry.getValue())"""

    def add(self, priority, value) -> None:

        """if len(self.heapArray) - self.count <= 10 :
            currSize = len(self.heapArray)
            self._resizeHeapArray(currSize + 100)""" # Resize supressed.

        if self.isFull() != True:
            newEntry = _HeapEntry(priority, value)

            self.heapArray[self.count] = newEntry # self.count is also an index for the last index + 1 
            self._trickleUp(self.count) # now self.count is the last index
            self.count += 1 # update self.count to be last index + 1
    
    def remove(self, index) -> _HeapEntry:
        if self.heapArray[index] != None:
            retValue = self.heapArray[index]
            self.heapArray[index] = self.heapArray[self.count-1]
            self.heapArray[self.count-1] = None
            self.count -= 1
            self._trickleDownRemove(index, self.count)

            return retValue

    def heapSort(self) -> None:
        self._heapify()
        for index in range(self.count-1, 0, -1):
            self._swap(0, index)
            self._trickleDown(0, index)


    """def heapSort(self) -> None:
        self._heapify()
        for index in range(self.count-1, 1, -1):
            self._swap(0, index)
            self._trickleDown(0, index)"""

    # --- Private --- #
    def _heapify(self) -> None:
        for index in range((self.count//2)-1, -1, -1):
            self._trickleDown(index, self.count)

    def _trickleUp(self, currIdx) -> None:
        parentIdx = (currIdx-1)//2
        if currIdx > 0:
            if self.heapArray[currIdx].getPriority() < self.heapArray[parentIdx].getPriority():
                # swap
                self._swap(parentIdx, currIdx)
                # recurse
                self._trickleUp(parentIdx)

    def _trickleDown(self, currIdx, numItems) -> None: # Modified from lecture notes and prac08
        leftChildIdx = currIdx * 2 + 1
        rightChildIdx = leftChildIdx + 1
        largeIdx = currIdx
        # left should always exist, heap tree/heap array always inserts left to right. largest always at the top (index 0)
        if leftChildIdx < numItems and self.heapArray[leftChildIdx] != None: # if current entry not leaf and left child not none
            if self.heapArray[largeIdx].getPriority() < self.heapArray[leftChildIdx].getPriority(): # if large is less than left child
                largeIdx = leftChildIdx # set large to left child idx
            if rightChildIdx < numItems and self.heapArray[rightChildIdx] != None: # if right child not leaf nor none
                if self.heapArray[largeIdx].getPriority() < self.heapArray[rightChildIdx].getPriority(): # if large child is less than right child
                    largeIdx = rightChildIdx # set largeidx to right child idx
            # large idx used to trickle and swap until largest at index 0.
            if self.heapArray[largeIdx].getPriority() > self.heapArray[currIdx].getPriority(): #if large entry is greater than current entry
                self._swap(largeIdx, currIdx) # swap entries with corresponding index
                self._trickleDown(largeIdx, numItems) # recurse (note, largeidx is not changed after _swap() is called)

    def _trickleDownRemove(self, currIdx, numItems) -> None: # Modified from lecture notes and prac08
        leftChildIdx = currIdx * 2 + 1
        rightChildIdx = leftChildIdx + 1
        largeIdx = currIdx
        # left should always exist, heap tree/heap array always inserts left to right. largest always at the top (index 0)
        if leftChildIdx < numItems and self.heapArray[leftChildIdx] != None: # if current entry not leaf and left child not none
            if self.heapArray[largeIdx].getPriority() > self.heapArray[leftChildIdx].getPriority(): # if large is less than left child
                largeIdx = leftChildIdx # set large to left child idx
            if rightChildIdx < numItems and self.heapArray[rightChildIdx] != None: # if right child not leaf nor none
                if self.heapArray[largeIdx].getPriority() > self.heapArray[rightChildIdx].getPriority(): # if large child is less than right child
                    largeIdx = rightChildIdx # set largeidx to right child idx
            # large idx used to trickle and swap until largest at index 0.
            if self.heapArray[largeIdx].getPriority() < self.heapArray[currIdx].getPriority(): #if large entry is greater than current entry
                self._swap(largeIdx, currIdx) # swap entries with corresponding index
                self._trickleDown(largeIdx, numItems) # recurse (note, largeidx is not changed after _swap() is called)

    def _swap(self, entryIdx_1, entryIdx_2) -> None:
        temp = self.heapArray[entryIdx_1]
        self.heapArray[entryIdx_1] = self.heapArray[entryIdx_2]
        self.heapArray[entryIdx_2] = temp

    def __iter__(self):
        currNode = self.heapArray[0]
        idx = 0
        while (currNode is not None) and (idx < len(self.heapArray)):
            currNode = self.heapArray[idx]
            if currNode != None:
                yield currNode.getValue()
            idx = idx + 1


    