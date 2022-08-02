# 
# CURTIN UNIVERISTY COMP1002 - Data Structures and Algorithms
# Assignment 1 - Hash Table Classes (Modified for assignment from Prac 07)
#
# Author: Alastair Kho
# ID: 20214878
#


# ===== MODULE IMPORTS ===== #
import numpy as np


# ===== CLASSES ===== #


# ---- Hash Entry ---- #

class _HashEntry():
    # --- Constructor --- #
    def __init__(self, inKey="", inValue=None) -> None:
        self._key = inKey
        self._value = inValue
        self._state = 0 # 0 = never used, 1 = used, -1 = formerly used
    
    # --- Accessors --- #
    def getKey(self) -> str:
        return self._key

    def getValue(self) -> object:
        return self._value

    def getState(self) -> int:
        return self._state

    # --- Mutators --- #
    def setKey(self, pKey) -> None:
        self._key = pKey

    def setValue(self, pValue) -> None:
        self._value = pValue

    def setState(self, pState) -> None:
        self._state = pState

    # --- Private --- #
    def __repr__(self) -> str:
        key = None if self._key == "" else(self._key)
        return f"(key: '{key}' value: {self._value})"


# ---- Hash Table ---- #

class DSAHashTable():
    _maxStep = None
    _upperlf = 0.7
    _lowerlf = 0.4

    # --- Constructor --- #
    def __init__(self, inTableSize) -> None:
        self.primedSize = self._nextPrime(inTableSize)
        self.hashArray = np.empty(self.primedSize, dtype=_HashEntry)
        self.count = 0

        for ii in range(len(self.hashArray)):
            self.hashArray[ii] = _HashEntry()

    # --- Accessors --- #
    def get(self, inKey) -> object: # returns the value of specified key
        hashIdx = self._find(inKey)
        retValue = self.hashArray[hashIdx].getValue()
        return retValue

    def getEntry(self, inKey) -> _HashEntry: # returns the entry of specified key

        hashIdx = self._find(inKey)
        retValue = self.hashArray[hashIdx]
        return retValue

    def getCount(self) -> int: # returns the value of specified key
        return self.count

    def isEmpty (self) -> bool: # returns the value of specified key
        return True if self.count == 0 else(False)

    def getLoadFactor(self) -> float: # returns the load factor as a float value
        lf = float(self.count/len(self.hashArray))
        return lf

    def export(self) -> str: # returns a string of all entries in hash table
        strExport = ""

        for ii in self.hashArray:
            if ii.getState() == 1:
                strExport += f"(Code: {ii.getKey()}, Weight: {ii.getValue()}), "

        return strExport

    def hasKey(self, inKey) -> bool: # returns true if key exists else false
        keyExists = False
        hashIdx = self._find(inKey)
        #print(hashIdx)

        if self.hashArray[hashIdx].getKey() == inKey:
            keyExists = True
        else:
            #print(f"HASKEY '{inKey}' doesnt exist at index {hashIdx}")
            keyExists = False

        return keyExists

    # --- Mutators --- #
    def put(self, inKey, inValue) -> None:
            
        hashIdx = self._find(inKey)
        origIdx = self._hash(inKey)
        spotFound = False

        while (spotFound == False):
            if (self.hasKey(inKey) == True): # if key already exists, can't put in table
                raise ValueError(f"'{inKey}' already in hash table!")

            elif (self.hashArray[hashIdx].getState() == 0) or (self.hashArray[hashIdx].getState() == -1): # key not found, found a place to put key.
                spotFound = True
                hashEntry = self.hashArray[hashIdx]
                hashEntry.setKey(inKey), hashEntry.setValue(inValue), hashEntry.setState(1) #set key and value
                self.count += 1

                if (self.getLoadFactor() > self._upperlf):
                    nextPrimeSize = self._nextPrime(len(self.hashArray))
                    self._resizeHashArray(nextPrimeSize) # resize will clear array, do second line for every valid key (with state = 1)
                    # after resizing, every key will have new hashes. This means we cannot access again through "hopping" or "double hashing"

                #print(f"adding index: {hashIdx} key: {inKey}")

            elif (hashIdx == origIdx) or (self.getLoadFactor() > self._upperlf): # if we wrap around or detect it's too full, resize
                    nextPrimeSize = self._nextPrime(len(self.hashArray))
                    self._resizeHashArray(nextPrimeSize) 
                    # resize will dynamically change array size through clearing array, do condition: 
                    # (self.hashArray[hashIdx].getState() == 0) or (self.hashArray[hashIdx].getState() == -1) for every valid key (with state = 1)
                    # after resizing, every key will have new hashes. This means we cannot access again through original key with "hopping" or "double hashing"
                    # we need the next line below so that we can access the keys with new hashes.

                    hashIdx = self._find(inKey) # IMPORTANT. This line tries and find hashIdx again of given key after resizing > valid keys should be readded to self.hashArray via _resizeHashArray()
                    # then meets condition of second line of this while loop; if (self.hashArray[hashIdx].getState() == 0) or (self.hashArray[hashIdx].getState() == -1)

    def remove(self, inKey) -> None:
        if self.hasKey(inKey) == True:
            hashIdx = self._find(inKey)
            hashEntry = self.hashArray[hashIdx]
            hashEntry.setKey(""), hashEntry.setValue(None), hashEntry.setState(-1)
            self.count -= 1

            if (self.getLoadFactor() < self._lowerlf): # if we wrap around or detect it's too full, resize
                nextPrimeSize = self._nextPrime(len(self.hashArray)//2)
                self._resizeHashArray(nextPrimeSize)
        else:
            hashIdx = self._find(inKey)
            raise ValueError(f"'{inKey}' not in hash table at index {hashIdx}!")
    
    # --- Private Methods --- #
    def _resizeHashArray(self, size) -> None:

        oldArr = self.hashArray # store old array
        self.hashArray = np.empty(size, dtype=_HashEntry) # reset Hash Array
        for ii in range(len(self.hashArray)):
            self.hashArray[ii] = _HashEntry()

        self.count = 0
        for oldEntry in oldArr:
            if oldEntry.getState() == 1:
                self.put(oldEntry.getKey(), oldEntry.getValue())

    def _find(self, inKey) -> int: # returns an available hash index

        hashIdx = self._hash(inKey) # hash first
        #print(hashIdx)
        origIdx = hashIdx
        found, giveUp = False, False

        while (not found) and (not giveUp):
            # if key is not found, end loop return the hashIdx of the empty entry.
            if (self.hashArray[hashIdx].getState() == 0): # key not found
                giveUp = True
                #print(f"key {inKey} hash {hashIdx} has state 0")

            # if key is found, end loop return the hashIdx of the found entry.
            elif (self.hashArray[hashIdx].getKey() == inKey): # key found
                found = True
                #print(f"{inKey} key exists")
            else:
                hashIdx = (hashIdx + self._hashStep(origIdx)) % len(self.hashArray) # else a key exists, but its not the right key = double hash probe
                if (hashIdx == origIdx): 
                    # if we loop around, just end and return the original hashIdx. This will be validated outside 
                    # when origIdx = hashIdx. Use is for "putting" to know when to resize

                    #  print(f"hash = orig = {hashIdx}")
                    giveUp = True
        
        return hashIdx

    def _hash(self, pKey) -> int: # returns hash index 
        hashIdx = 0
        if type(pKey) == str:
            for char in pKey:
                hashIdx = (33 * hashIdx) + ord(char)
            retVal = hashIdx % len(self.hashArray)
        else:
            raise ValueError(f"'{pKey}' is not of type 'str'")
        return retVal

    def _hashStep(self, pKey) -> int: # double hashing
        currMaxStep = int(len(self.hashArray)) if (self._maxStep == None) else (self._maxStep) #get current max step
        hashStep =  currMaxStep - (pKey % currMaxStep)
        return hashStep

    def _nextPrime(self, pStartVal) -> int: # returns next prime number
        if (pStartVal % 2 == 0):
            primeVal = pStartVal - 1
        else:
            primeVal = pStartVal
        
        isPrime = False

        while (not isPrime):
            
            primeVal = primeVal +2
            ii = 3
            isPrime = True

            while (ii * ii <= primeVal) and (isPrime):
                if (primeVal % ii == 0): 
                    isPrime = False
                else:
                    ii = ii + 2
        return primeVal