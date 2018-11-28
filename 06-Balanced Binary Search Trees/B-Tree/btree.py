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
        
        print("Looking at node with index:", self.getIndex())
        print("Node's items:", self.items)
        print("Node's children:", self.child)
        if self.isLeaf():
            if not self.isFull():
                print("Not Full Leaf!")
                self.items[self.numberOfKeys] = item
                self.items = sorted(self.items, key=lambda x: (x is None, x))
                self.numberOfKeys += 1
                print(self.items)
                print("DONE")
                return self, None, None
            
            print("Full leaf!")
            print("Items:", self.items)

            return BTreeNode.splitNode(self, bTree, item, None)
        else:
            print("Not a leaf node!")
            index, done = 0, False

            while not done and self.items[index] < item:
                if self.items[index] == None or index == self.getNumberOfKeys()-1:
                    done = True
                
                index += 1

            print("RECURSIVE CALL")
            leftIndex, promoted, rightIndex = BTreeNode.insert(bTree.nodes[self.getChild(index)], bTree, item)

            if promoted != None and not self.isFull():
                self.items[self.getNumberOfKeys()] = promoted
                self.items = sorted(self.items, key=lambda x: (x is None, x))

                indexPromoted = self.items.index(promoted)
                self.child.insert(indexPromoted+1, rightIndex)
                print(self.child)
                self.child.pop()
                self.numberOfKeys += 1
            else:
                if promoted != None and self.isFull():
                    return self.splitNode(bTree, promoted, rightIndex)

            return self, None, None
                
        

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

        print(items)
        children = []

        indexInsertedItem = items.index(item)

        children.append(self.child[0])
        j = 1

        for i in range(bTree.degree*2+1):
            if i == indexInsertedItem:
                children.append(right)
            else:
                children.append(self.child[j])
                j += 1
        
        print(children)
        promotedItemIdx = len(items) // 2
        promotedItem = items[promotedItemIdx]

        self.items = items
        self.setNumberOfKeys(len(items[:promotedItemIdx]))

        print("ITEMS", self.items)

        right = bTree.getFreeNode()
        print("Created node with index:", right.getIndex())

        right.setNumberOfKeys(len(items[promotedItemIdx+1:]))

        z = 0
        start, end = promotedItemIdx+1, (promotedItemIdx + right.getNumberOfKeys()+1)
        for i in range(start, end):
            right.items[z] = items[i]
            z += 1

        leftChildren, rightChildren = children[:len(children)//2], children[len(children)//2:]
        for i in range(len(leftChildren)):
            self.child[i] = leftChildren[i]

        j = 0
        for i in range(len(rightChildren)):
            right.child[j] = rightChildren[i]
            j += 1

        self.items = items[:promotedItemIdx] + [None] * (bTree.degree*2 - len(items[:promotedItemIdx]))
        print("\nLeft Node items:", items[:promotedItemIdx])
        print("Promoted Item:", items[promotedItemIdx])
        print("Right Node items:", right.items)

        print("Children:", children)
        
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
        if item in self.items:
            itemIdx = self.items.index(item)
            if self == bTree.rootNode:
                pass

            else:
                if self.isLeaf():
                    print("I am a leaf node.")
                    if self.getNumberOfKeys() > bTree.degree:
                        self.items.pop(itemIdx)
                        self.items.append(None)
                        self.numberOfKeys -= 1

                        return item
                    else:
                        # Rebalancing!
                        pass
                else:
                    # Get left most and may cause a rebalancing again.
                    pass
                
        else:
            index, done = 0, False
            while not done and self.items[index] < item:
                if self.items[index] == None or index == self.getNumberOfKeys()-1:
                    done = True
                
                index += 1
            node = bTree.readFrom(self.getChild(index))
            return BTreeNode.delete(node, bTree, item)


        
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
        
        for i in range(self.getNumberOfKeys()):
            if self.items[i] == None:
                return {"found": False, "nodeIndex": None, "fileIndex": self.getIndex()}

            if self.items[i] == item:
                return {"found": True, "nodeIndex": i, "fileIndex": self.getIndex()}

            if self.items[i] > item and self.isLeaf() == False:
                node = bTree.nodes[self.getChild(i)]
                return node.search(bTree, item)

            if i == (self.getNumberOfKeys()-1) and self.isLeaf() == False:
                node = bTree.nodes[self.getChild(i+1)]
                return node.search(bTree, item)

        return {"found": False, "nodeIndex": None, "fileIndex": self.getIndex()}

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
        data = BTree.__searchTree(self, anItem)

        if data["found"] == False:
            return None

        # node = self.readFrom(data["fileIndex"])
        return BTreeNode.delete(self.rootNode, self, anItem)

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

        left, middle, right = BTreeNode.insert(self.rootNode, self, anItem)
    
        if middle != None:
            newNode = self.getFreeNode()
            newNode.items[0] = middle
            newNode.setChild(0, left)
            newNode.setChild(1, right)
            newNode.setNumberOfKeys(1)
            self.rootNode = newNode
            self.rootIndex = newNode.getIndex()

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
        # print(data)

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
        data = self.rootNode.search(self, anItem)
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

    lst = [100,80,220,140,120,180,200,500,150,90,110,160,170,130,190,151,152,111]
    # lst = [10,8,22,14,12,18,2,50,15]
    
    b = BTree(2)

    for x in lst:
        print(repr(b))
        print("="*60)
        print("***Inserting",x)
        b.insert(x)
    
    print("\n-----Tree after all inserts.-----")
    print(repr(b))

    # for x in lst:
    #     print(x, x in b)

    print(b.rootIndex)

    print(b.delete(180))
    print(repr(b))
    
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

def main():
    btreemain()


if __name__ == "__main__":
    main()