'''
  File: btree.py
  Author: Kent D. Lee and Steve Hubbard
  Date: 06/30/2014
  Description: This module provides the BTree class, based on support from
    the BTreeNode class.  The BTreeNode class is also implemented in this 
    module. This module is meant to support the recursive implementation of 
    insert, lookup, and delete within a BTree. 

    The module requires the Queue class in the queue module.

    This program has two main functions, the btreemain function and the main
    function. The btreemain function tests the BTree datatype. The expected
    output is provided in a comment after the function. Once the btreemain 
    function runs and produces the proper output, the main function can be 
    run to test the BTree with the join functionality. 

    The main function either builds a new BTree or reads an existing BTree 
    from the index files, Feed.idx and FeedAttribType.idx files. If the idx
    file does not exist, then a new BTree is built and written to the 
    corresponding idx file.
'''
import datetime
import os
from copy import deepcopy
import sys
# import queue

class Queue:
    def __init__(self):
        self.items = []
        self.frontIdx = 0
        
    def __compress(self):
        newitems = []
        for i in range(self.frontIdx,len(self.items)):
            newitems.append(self.items[i])
            
        self.items = newitems
        self.frontIdx = 0
        
    def dequeue(self):
        if self.isEmpty():
            raise RuntimeError("Attempt to dequeue an empty queue")
        
        # When queue is half full, compress it. This 
        # achieves an amortized complexity of O(1) while
        # not letting the list continue to grow unchecked. 
        if self.frontIdx * 2 > len(self.items):
            self.__compress()
            
        item = self.items[self.frontIdx]
        self.frontIdx += 1
        return item
    
    def enqueue(self,item):
        self.items.append(item)
        
    def front(self):
        if self.isEmpty():
            raise RuntimeError("Attempt to access front of empty queue")
        
        return self.items[self.frontIdx]
        
    def isEmpty(self):
        return self.frontIdx == len(self.items)

    def clear(self):
        self.items = []
        self.frontIdx = 0
    
class BTreeNode:
    '''
      This class will be used by the BTree class.  Much of the functionality of
      BTrees is provided by this class.
    '''
    def __init__(self, degree = 1, numberOfKeys = 0, items = None, child = None, \
        index = None):
        ''' Create an empty node with the indicated degree'''
        self.numberOfKeys = numberOfKeys
        self.degree = degree
        if items != None:
            self.items = items
        else:
            self.items = [None]*2*degree
        if child != None:
            self.child = child
        else:
            self.child = [None]*(2*degree+1)
        self.index = index

    def __repr__(self):
        ''' This provides a way of writing a BTreeNode that can be
            evaluated to reconstruct the node.
        '''
        return "BTreeNode("+str(len(self.items)//2)+","+str(self.numberOfKeys)+ \
            ","+repr(self.items)+","+repr(self.child)+","+str(self.index)+")\n"

    def __str__(self):
        st = 'The contents of the node with index '+ \
             str(self.index) + ':\n'
        for i in range(0, self.numberOfKeys):
            st += '   Index   ' + str(i) + '  >  child: '
            st += str(self.child[i])
            st += '   item: '
            st += str(self.items[i]) + '\n'
        st += '                 child: '
        st += str(self.child[self.numberOfKeys]) + '\n'
        return st
    
    def insert(self,bTree,item):
        '''
        Insert an item in the node. Return three values as a tuple, 
        (left,item,right). If the item fits in the current node, then 
        return self as left and None for item and right. Otherwise, return 
        two new nodes and the item that will separate the two nodes in the parent. 
        '''
        print("Looking at", self.getIndex())
        print("children", self.child)
        if self.isLeaf() and not self.isFull():
            self.items[self.numberOfKeys] = item
            self.items = sorted(self.items, key=lambda x: (x is None, x))
            self.numberOfKeys += 1

            return self, None, None

        elif self.isFull() and self.isLeaf():
            print("Splitting!")
            leftIndex, promoted, rightIndex = BTreeNode.splitNode(self, bTree, item, bTree.getFreeNode())
            if self == bTree.rootNode:
                newNode = bTree.getFreeNode()
                newNode.items[newNode.getNumberOfKeys()] = promoted
                newNode.numberOfKeys += 1

                newNode.setChild(0, leftIndex)
                newNode.setChild(1, rightIndex)

                bTree.rootNode = newNode
            else:
                print(self.index)
                print("HERE")
                print(leftIndex, promoted, rightIndex)
                print(bTree.rootNode)
                return leftIndex, promoted, rightIndex

        else:
            index, done = 0, False
            while not done and self.items[index] < item:
                index += 1
                if self.items[index] == None:
                    done = True
                
            nodeIdx = bTree.nodes[self.getIndex()].child[index]

            print("Node", bTree.nodes[nodeIdx])
            leftIndex, promoted, rightIndex = BTreeNode.insert(bTree.nodes[nodeIdx], bTree, item)`

            if promoted != None:
                print("NOT NONE")
                if not self.isFull():
                    self.items[self.getNumberOfKeys()] = promoted
                    self.child[self.getNumberOfKeys()] = leftIndex
                    self.child[self.getNumberOfKeys()+1] = rightIndex

                    self.numberOfKeys += 1
                
        

    def splitNode(self,bTree,item,right):
        '''
        This method is given the item to insert into this node and the node 
        that is to be to the right of the new item once this node is split.
        
        Return the indices of the two nodes and a key with the item added to 
        one of the new nodes. The item is inserted into one of these two 
        nodes and not inserted into its children.
        '''
        items = self.items + [item]
        items.sort()

        children = []

        indexInsertedItem = items.index(item)

        children.append(self.child[0])
        j = 1

        for i in range(bTree.degree*2+1):
            if i == indexInsertedItem:
                children.append(right.getIndex())
            else:
                children.append(self.child[j])
                j += 1
        
        promotedItemIdx = len(items) // 2
        promotedItem = items[promotedItemIdx]
        print(items)
        print(promotedItemIdx)

        self.items = items
        self.setNumberOfKeys(len(items[:promotedItemIdx]))

        right.setNumberOfKeys(len(items[promotedItemIdx+1:]))

        z = 0
        start, end = promotedItemIdx+1, (promotedItemIdx + right.getNumberOfKeys()+1)
        for i in range(start, end):
            right.items[z] = items[i]
            z += 1

        print(self.items)
        print(right.items)

        print(items[promotedItemIdx])

        print(children)
        
        return self.getIndex(), promotedItem, right.getIndex()

    
    def getLeftMost(self,bTree):
        ''' Return the left-most item in the 
            subtree rooted at self.
        '''
        if self.child[0] == None:
            return self.items[0]
        
        return bTree.nodes[self.child[0]].getLeftMost(bTree)

    def delete(self,bTree,item):
        '''
           The delete method returns None if the item is not found
           and a deep copy of the item in the tree if it is found.
           As a side-effect, the tree is updated to delete the item.
        '''
        pass
        
    def redistributeOrCoalesce(self,bTree,childIndex):
        '''
          This method is given a node and a childIndex within 
          that node that may need redistribution or coalescing.
          The child needs redistribution or coalescing if the
          number of keys in the child has fallen below the 
          degree of the BTree. If so, then redistribution may
          be possible if the child is a leaf and a sibling has 
          extra items. If redistribution does not work, then 
          the child must be coalesced with either the left 
          or right sibling.

          This method does not return anything, but has the 
          side-effect of redistributing or coalescing
          the child node with a sibling if needed. 
        '''
        pass 


    def getChild(self,i):
        # Answer the index of the ith child
        if (0 <= i <= self.numberOfKeys):
            return self.child[i]
        else:
            print( 'Error in getChild().' )
            
    def setChild(self, i, childIndex):
        # Set the ith child of the node to childIndex
        self.child[i] = childIndex 

    def getIndex(self):
        return self.index

    def setIndex(self, anInteger):
        self.index = anInteger

    def isFull(self):
        ''' Answer True if the receiver is full.  If not, return
          False.
        '''
        return (self.numberOfKeys == len(self.items))

    def isLeaf(self):
        return self.child == [None]*(2*self.degree+1)

    def getNumberOfKeys(self):
        return self.numberOfKeys

    def setNumberOfKeys(self, anInt ):
        self.numberOfKeys = anInt

    def clear(self):
        self.numberOfKeys = 0
        self.items = [None]*len(self.items)
        self.child = [None]*len(self.child)

    def search(self, bTree, item):
        '''Answer a dictionary satisfying: at 'found'
          either True or False depending upon whether the receiver
          has a matching item;  at 'nodeIndex' the index of
          the matching item within the node; at 'fileIndex' the 
          node's index. nodeIndex and fileIndex are only set if the 
          item is found in the current node. 
        '''
        data = {"found": False, "nodeIndex": None, "fileIndex": None}

        q, done = Queue(), False
        q.enqueue(self)

        while not done and not q.isEmpty():
            current = q.dequeue()
            # print(self)
            for i in range(current.numberOfKeys):
                # print(current.items)
                # print(current.child)
                # print(current.items[i])
                # print(i)
                if current.items[i] == item:
                    data["found"] = True
                    data["nodeIndex"] = i
                    data["fileIndex"] = current.index
                    print(data)
                    return data
    
                elif current.items[i] > item and not current.isLeaf():
                    newNode = bTree.nodes[current.getChild(i)]
                    q.enqueue(newNode)

                elif i == current.numberOfKeys -1 and not current.isLeaf():
                    newNode = bTree.nodes[current.getChild(i+1)]
                    q.enqueue(newNode)

                else:
                    data["fileIndex"] = current.index
                    done = True

        # print(data)
        return data



class BTree:
    def __init__(self, degree, nodes = {}, rootIndex = 1, freeIndex = 2):
        self.degree = degree
        
        if len(nodes) == 0:
            self.rootNode = BTreeNode(degree)
            self.nodes = {}
            self.rootNode.setIndex(rootIndex)
            self.writeAt(1, self.rootNode)  
        else:
            self.nodes = deepcopy(nodes)
            self.rootNode = self.nodes[rootIndex]
              
        self.rootIndex = rootIndex
        self.freeIndex = freeIndex
        
    def __repr__(self):
        return "BTree("+str(self.degree)+",\n "+repr(self.nodes)+","+ \
            str(self.rootIndex)+","+str(self.freeIndex)+")"

    def __str__(self):
        st = '  The degree of the BTree is ' + str(self.degree)+\
             '.\n'
        st += '  The index of the root node is ' + \
              str(self.rootIndex) + '.\n'
        for x in range(1, self.freeIndex):
            node = self.readFrom(x)
            if node.getNumberOfKeys() > 0:
                st += str(node) 
        return st


    def delete(self, anItem):
        ''' Answer None if a matching item is not found.  If found,
          answer the entire item.
        ''' 
        pass

    def getFreeIndex(self):
        # Answer a new index and update freeIndex.  Private
        self.freeIndex += 1
        return self.freeIndex - 1

    def getFreeNode(self):
        #Answer a new BTreeNode with its index set correctly.
        #Also, update freeIndex.  Private
        newNode = BTreeNode(self.degree)
        index = self.getFreeIndex()
        newNode.setIndex(index)
        self.writeAt(index,newNode)
        return newNode

    def inorderOn(self, aFile):
        '''
          Print the items of the BTree in inorder on the file 
          aFile.  aFile is open for writing.
        '''
        aFile.write("An inorder traversal of the BTree:\n")
        self.inorderOnFrom( aFile, self.rootIndex)

    def inorderOnFrom(self, aFile, index):
        ''' Print the items of the subtree of the BTree, which is
          rooted at index, in inorder on aFile.
        '''
        pass

    def insert(self, anItem):
        ''' Answer None if the BTree already contains a matching
          item. If not, insert a deep copy of anItem and answer
          anItem.
        '''
        data = BTree.__searchTree(self, anItem)

        if data["found"] == True:
            return None
        
        anItem = deepcopy(anItem)

        BTreeNode.insert(self.rootNode, self, anItem)

        return anItem

    def levelByLevel(self, aFile):
        ''' Print the nodes of the BTree level-by-level on aFile. )
        '''
        pass

    def readFrom(self, index):
        ''' Answer the node at entry index of the btree structure.
          Later adapt to files
        '''
        if self.nodes.__contains__(index):
            return self.nodes[index]
        else:
            return None

    def recycle(self, aNode):
        # For now, do nothing
        aNode.clear()

    def retrieve(self, anItem):
        ''' If found, answer a deep copy of the matching item.
          If not found, answer None
        '''
        data = self.__searchTree(anItem)

        if data["found"] == True:
            fileIndex = data["fileIndex"]

            return deepcopy(self.nodes[fileIndex])
        
        return None

    def __contains__(self, item):
        data = self.__searchTree(item)

        if data["found"] == True:
            return True
        return False

    def __searchTree(self, anItem):
        ''' Answer a dictionary.  If there is a matching item, at
          'found' is True, at 'fileIndex' is the index of the node
          in the BTree with the matching item, and at 'nodeIndex'
          is the index into the node of the matching item.  If not,
          at 'found' is False, but the entry for 'fileIndex' is the
          leaf node where the search terminated.
        '''
        data = BTreeNode.search(self.rootNode, self, anItem)
        return data

 
    def update(self, anItem):
        ''' If found, update the item with a matching key to be a
          deep copy of anItem and answer anItem.  If not, answer None.
        '''
        pass

    def writeAt(self, index, aNode):
        ''' Set the element in the btree with the given index
          to aNode.  This method must be invoked to make any
          permanent changes to the btree.  We may later change
          this method to work with files.
          This method is complete at this time.
        '''
        self.nodes[index] = aNode

def btreemain():
    print("My/Our name(s) is/are ")

    lst = [10,8,22,14,12,18,2,50,15]
    # lst = [10,8,22,14,12,18,2,50,15]
    
    b = BTree(2)

    # b.nodes[1].numberOfKeys = 1
    # b.nodes[1].items[0] = 20
    # b.nodes[1].child[0] = 3
    # b.nodes[1].child[1] = 2

    # b.writeAt(2, BTreeNode(2, numberOfKeys=2))
    # b.nodes[2].setIndex(2)
    # b.nodes[2].items[0] = 40
    # b.nodes[2].items[1] = 60

    # b.writeAt(3, BTreeNode(2, numberOfKeys=1))
    # b.nodes[3].setIndex(3)
    # b.nodes[3].items[0] = 10
    # b.nodes[3].items[1] = 60


    # print(20 in b)
    # print(40 in b)
    # print(60 in b)
    # print(10 in b)
    # print(80 in b)
    # print(30 in b)
    # print(5 in b)

    # print(b.retrieve(20))
    # print(b.retrieve(40))
    # print(b.retrieve(60))
    # print(b.retrieve(10))
    # print(b.retrieve(80))

    
    for x in lst:
        print(repr(b))
        print("***Inserting",x)
        b.insert(x)
    
    print(repr(b))

    print(b.rootNode)
    
    # lst = [14,50,8,12,18,2,10,22,15]
    
    # for x in lst:
    #     print("***Deleting",x)
    #     b.delete(x) 
    #     print(repr(b))
    
    # #return 
    # lst = [54,76]
    
    # for x in lst:
    #     print("***Deleting",x)
    #     b.delete(x)
    #     print(repr(b))
        
    # print("***Inserting 14")
    # b.insert(14)
    
    # print(repr(b))
    
    # print("***Deleting 2")
    # b.delete(2)
    
    # print(repr(b))
    
    # print ("***Deleting 84")
    # b.delete(84)
    
    # print(repr(b))
    
'''
Here is the expected output from running this program. Depending on the order of 
redistributing or coalescing, your output may vary. However, the end result in 
every case should be the insertion or deletion of the item from the BTree. 

My/Our name(s) is/are 
BTree(2,
 {1: BTreeNode(2,0,[None, None, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 10
BTree(2,
 {1: BTreeNode(2,1,[10, None, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 8
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
},1,2)
***Inserting 22
BTree(2,
 {1: BTreeNode(2,3,[8, 10, 22, None],[None, None, None, None, None],1)
},1,2)
***Inserting 14
BTree(2,
 {1: BTreeNode(2,4,[8, 10, 14, 22],[None, None, None, None, None],1)
},1,2)
***Inserting 12
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[14, 22, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 18
BTree(2,
 {1: BTreeNode(2,2,[8, 10, None, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[14, 18, 22, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 2
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[14, 18, 22, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 50
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[14, 18, 22, 50],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, None, None, None],[1, 2, None, None, None],3)
},3,4)
***Inserting 15
BTree(2,
 {1: BTreeNode(2,3,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[14, 15, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[12, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 14
**Redistribute From Left**
BTree(2,
 {1: BTreeNode(2,2,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[12, 15, None, None],[None, None, None, None, None],2)
, 3: BTreeNode(2,2,[10, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,2,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 50
**Coalesce with Left Sibling in node with index 3
BTree(2,
 {1: BTreeNode(2,2,[2, 8, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,4,[12, 15, 18, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[10, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 8
**Redistribute From Right**
BTree(2,
 {1: BTreeNode(2,2,[2, 10, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,3,[15, 18, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[12, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 12
BTree(2,
 {1: BTreeNode(2,2,[2, 10, 10, None],[None, None, None, None, None],1)
, 2: BTreeNode(2,2,[18, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,1,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},3,5)
***Deleting 18
**Coalesce with Left Sibling in node with index 3
BTree(2,
 {1: BTreeNode(2,4,[2, 10, 15, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 2
BTree(2,
 {1: BTreeNode(2,3,[10, 15, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 10
BTree(2,
 {1: BTreeNode(2,2,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 22
BTree(2,
 {1: BTreeNode(2,1,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 15
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 54
54 not found during delete.
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 76
76 not found during delete.
BTree(2,
 {1: BTreeNode(2,0,[15, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Inserting 14
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 2
2 not found during delete.
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
***Deleting 84
84 not found during delete.
BTree(2,
 {1: BTreeNode(2,1,[14, 22, 22, 22],[None, None, None, None, None],1)
, 2: BTreeNode(2,1,[22, 22, 22, 22],[None, None, None, None, None],2)
, 3: BTreeNode(2,0,[15, 18, None, None],[1, 2, 4, None, None],3)
, 4: BTreeNode(2,1,[22, 50, None, None],[None, None, None, None, None],4)
},1,5)
'''

def main():
    btreemain()


if __name__ == "__main__":
    main()