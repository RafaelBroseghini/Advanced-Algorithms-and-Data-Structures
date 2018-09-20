import random

class OrderedTreeSet:
    class BinarySearchTree:
        # This is a Node class that is internal to the BinarySearchTree class. 
        class Node:
            def __init__(self,val,left=None,right=None):
                self.val = val
                self.left = left
                self.right = right
                
            def getVal(self):
                return self.val
            
            def setVal(self,newval):
                self.val = newval
                
            def getLeft(self):
                return self.left
            
            def getRight(self):
                return self.right
            
            def setLeft(self,newleft):
                self.left = newleft
                
            def setRight(self,newright):
                self.right = newright
            
            def getLeftMost(self, node):
                if node.getLeft() == None:
                    return node
                return self.getLeftMost(node.getLeft())
                
            # This method deserves a little explanation. It does an inorder traversal
            # of the nodes of the tree yielding all the values. In this way, we get
            # the values in ascending order.
            def __iter__(self):
                if self.left != None:
                    for elem in self.left:
                        yield elem
                        
                yield self.val
                
                if self.right != None:
                    for elem in self.right:
                        yield elem

            def __repr__(self):
                return "BinarySearchTree.Node(" + repr(self.val) + "," + repr(self.left) + "," + repr(self.right) + ")"            
                
        # Below are the methods of the BinarySearchTree class. 
        def __init__(self, root=None):
            self.root = root
            
        def insert(self,val):
            self.root = OrderedTreeSet.BinarySearchTree.__insert(self.root,val)
            
        def __insert(root,val):
            if root == None:
                return OrderedTreeSet.BinarySearchTree.Node(val)
            
            if val < root.getVal():
                root.setLeft(OrderedTreeSet.BinarySearchTree.__insert(root.getLeft(),val))
            else:
                root.setRight(OrderedTreeSet.BinarySearchTree.__insert(root.getRight(),val))
                
            return root
   
        def delete(self, val):
            self.root = OrderedTreeSet.BinarySearchTree.__delete(self.root, val)

        def __delete(root, val):
            if root == None:
                return None

            if val < root.getVal():
                root.setLeft(OrderedTreeSet.BinarySearchTree.__delete(root.getLeft(),val))
            elif val > root.getVal():
                root.setRight(OrderedTreeSet.BinarySearchTree.__delete(root.getRight(),val))

            elif val == root.getVal():
                if root.getLeft() == None:
                    return root.getRight()
                elif root.getRight() == None:
                    return root.getLeft()    
                elif root.getLeft() and root.getRight():
                    # print("Root:, ", root.getVal(), "left: ", root.getLeft().getVal(), "right: ", root.getRight().getVal())
                    # print(root.getLeft())

                    # print()
                    # print(root.getRight())
                    sub = root.getLeftMost(root.getRight())
                    # print("the left most node is", sub.val)

                    # sub_val = sub.getVal()
                    # root_val = root.getVal()

                    # sub.setVal(root_val)
                    # root.setVal(sub_val)

                    root.setVal(sub.getVal())
                    root.setRight(OrderedTreeSet.BinarySearchTree.__delete(root.getRight(), sub.getVal()))

            return root

            
        def __iter__(self):
            if self.root != None:
                return iter(self.root)
            else:
                return iter([])

        def __str__(self):
            return "BinarySearchTree(" + repr(self.root) + ")"
            
    def __init__(self,contents=None):
        self.tree = OrderedTreeSet.BinarySearchTree()
        if contents != None:
            # randomize the list
            indices = list(range(len(contents)))
            random.shuffle(indices)
            
            for i in range(len(contents)):
                self.tree.insert(contents[indices[i]])
                
            self.numItems = len(contents)
        else:
            self.numItems = 0
            
    def __str__(self):
        pass
    
    def __iter__(self):
        return iter(self.tree)
    
    # Following are the mutator set methods 
    def add(self, item):
        self.tree.insert(item)
        self.numItems += 1
                
    def remove(self, item):
        self.tree.delete(item)
        # raise KeyError("Value not found.")
        self.numItems -= 1
        
    def discard(self, item):
        self.tree.delete(item)
        self.numItems -= 1
        
    def pop(self):
        pass
            
    def clear(self):
        self.tree = OrderedTreeSet.BinarySearchTree()
        self.numItems = 0
        
    def update(self, other):
        for item in other:
            if item not in self:
                self.add(item)
            
    def intersection_update(self, other):
        # Review.
        contents = list(self)

        for item in contents:
            if item not in other:
                self.discard(item)
            
    def difference_update(self, other):
        pass
                
    def symmetric_difference_update(self, other):
        pass
                
    # Following are the accessor methods for the HashSet  
    def __len__(self):
        return self.numItems
    
    def __contains__(self, item):
        root = self.tree.root

        found = False
        if root:
            while not found and root != None:
                if item == root.getVal():
                    found = True
                elif item > root.getVal():
                    root = root.getRight()
                elif item < root.getVal():
                    root = root.getLeft()
        return found
            
    
    # One extra method for use with the HashMap class. This method is not needed in the 
    # HashSet implementation, but it is used by the HashMap implementation. 
    def __getitem__(self, item):
        pass      
        
    def not__contains__(self, item):
        pass
    
    def isdisjoint(self, other):
        pass
    
    
    def issubset(self, other):
        for item in self:
            if item not in other:
                return False
        return True
            
    
    def issuperset(self, other):
        for item in other:
            if item not in self:
                return False
        return True
    
    def union(self, other):
        pass
    
    def intersection(self, other):
        pass
    #done
    def difference(self, other):
        new_set = OrderedTreeSet()
        
        for item in self:
            if item not in other:
                new_set.add(item)
        
        return new_set
    
    def symmetric_difference(self, other):
        pass
    
    def copy(self):
        return self
    
    # Operator Definitions
    def __or__(self, other):
        pass
    
    def __and__(self,other):
        pass
    
    def __sub__(self,other):
        pass
    
    def __xor__(self,other):
        pass
    
    def __ior__(self,other):
        pass
    
    def __iand__(self,other):
        pass
    
    def __ixor(self,other):
        pass    
    
    def __le__(self,other):
        pass
    
    def __lt__(self,other):
        pass
    
    def __ge__(self,other):
        pass
    
    def __gt__(self,other):
        pass
    
    def __eq__(self,other):
        return self.issubset(other) and other.issubset(self)     
                
            
    
 
def main():
    s = input("Enter a list of numbers: ")
    lst = s.split()
    
    tree = OrderedTreeSet()
    
    for x in lst:
        tree.add(float(x))
        
    for x in tree:
        print(x)

if __name__ == "__main__":
    main()