class PriorityQueue(object):
    def __init__(self, degree=2, contents = []):
        self.degree = degree
        # we are using the list built due to the empty list contents default
        # parameter. The second time you go to use it, is not going to be the same.
        # because it was mutated. The empty list is shared across different same objects.
        self.data = list(contents)
        # This is the first parents idx.
        parentIdx = (len(self.data) - 2 ) // self.degree

        for i in range(parentIdx, -1, -1):
            self.__siftDownFromTo(i, len(self.data)-1)

    
    def __siftDownFromTo(self, parentIdx, endIdx):
        done = False
        while not done and parentIdx < (endIdx - 1) // self.degree:
            bestChildIdx = self.__bestChildOf(parentIdx, endIdx)
            if self.data[parentIdx] > self.data[bestChildIdx]:
                self.data[parentIdx], self.data[bestChildIdx] = self.data[bestChildIdx], self.data[parentIdx]
                
                parentIdx = bestChildIdx
            else:
                done = True
        
    def __bestChildOf(self, parentIdx, endIdx):
        bestChildIdx = parentIdx * self.degree + 1
        endIdx = min(bestChildIdx + self.degree - 1, endIdx)
        for i in range(bestChildIdx+1, endIdx):
            if self.data[i] < self.data[bestChildIdx]:
                bestChildIdx = i
        return bestChildIdx


    # dequeue
    # 0 index

    # enqueue
    # end of array, siftup from last idx.
