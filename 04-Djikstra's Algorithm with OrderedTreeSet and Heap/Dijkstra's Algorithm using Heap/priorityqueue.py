"""
Using PriorityQueue as Heap.
"""

class PriorityQueue:
    """Docstring for PriorityQueue"""
    def __init__(self, degree = 2, contents = []):
        self.degree = degree
        self.data = list(contents)
        self.size = len(contents)
        
        parentIndex = (self.size-2) // self.degree
        for i in range(parentIndex,-1,-1):
            self.__siftDownFromTo(i, self.size-1)
        
    def __repr__(self):
        return "PriorityQueue(" + str(self.degree) + "," + str(self.data) + ")"
    
    def __str__(self):
        return repr(self)
    
    def __bestChildOf(self, parentIndex, toIndex):
        
        firstChildIndex = parentIndex * self.degree + 1
        endIndex = min(parentIndex * self.degree + self.degree, toIndex)
        
        if firstChildIndex > endIndex:
            return None
        
        bestChildIndex = firstChildIndex
        
        for k in range(firstChildIndex, endIndex+1):
            if self.data[k] < self.data[bestChildIndex]:
                bestChildIndex = k
                
        return bestChildIndex
        
        
    def __siftDownFromTo(self, fromIndex, toIndex):
        
        parentIndex = fromIndex
        done = False
        
        while not done:
            childIndex = self.__bestChildOf(parentIndex, toIndex)
            
            if childIndex == None:
                done = True
                
            elif self.data[parentIndex] > self.data[childIndex]:
                self.data[parentIndex], self.data[childIndex] = \
                    self.data[childIndex], self.data[parentIndex]
                
                parentIndex = childIndex
                
            else:
                done = True

    def __siftUpFrom(self, fromIndex):
        childIndex = fromIndex
        done = False

        while not done:
            parentIndex = (childIndex-1) // self.degree
            if childIndex == 0:
                done = True
            elif self.data[childIndex] < self.data[parentIndex]:
                self.data[childIndex], self.data[parentIndex] = \
                    self.data[parentIndex], self.data[childIndex]
                
                childIndex = parentIndex
            else:
                done = True

    def enqueue(self, item):
        if self.size == len(self.data):
            self.data.append(item)
            self.__siftUpFrom(self.size)
        else:
            self.data[self.size] = item
        self.size += 1

    def dequeue(self):
        if not self.isEmpty():
            rv = self.data[0]
            lastEl = self.data[self.size-1]
            self.data[0] = lastEl 
            self.size -= 1
            
            if self.size > 0:
                self.__siftDownFromTo(0, self.size-1)
            return rv
        raise IndexError("pop from empty PriorityQueue")

    def isEmpty(self):
        return self.size == 0
                
def main():
    lst = [100,10,20,25,5,8,2]
    h = PriorityQueue(2, lst)

    print(h)
    
    lst = [100,10,20,25,5,8]
    h = PriorityQueue(2,lst)
    print(h)    
    
    lst = []
    h = PriorityQueue(2,lst)
    print(h)   
    
    lst = [100,10,20,25,5,8]
    h = PriorityQueue(3,lst)

    print(h)
    
if __name__ == "__main__":
    main()