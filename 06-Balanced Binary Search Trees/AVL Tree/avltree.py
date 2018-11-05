'''
  File:  avltree.py 
  Author: Steve Hubbard,  and 
  Date:  
  Description:  This module provides the AVLNode and AVLTree classes.
'''

# Paste stack code here.

class AVLNode:
  def __init__(self, item, balance = 0, left=None, right=None):
    self.item = item
    self.left = left
    self.right = right
    self.balance = balance

  def depth(node):
    # return depth of the node.
    # leaf node are depth 1.
    if node == None:
      return 0
    return max(node.left.depth() if node.left else 0, node.right.depth() if node.right else 0) + 1


    """
    check calls depth to check each of the balances. Maybe depth calls
    check. if balance is not correct raise an exception.
    """
    
  def __str__(self):
    '''  This performs an inorder traversal of the tree rooted at self, 
        using recursion.  Return the corresponding string.
    '''
    st = str(self.item) + ' ' + str(self.balance) + '\n'
    if self.left != None:
        st = str(self.left) +  st  # A recursive call: str(self.left)
    if self.right != None:
        st = st + str(self.right)  # Another recursive call
    return st
  
  def rotateLeft(self):
    '''  Perform a left rotation of the subtree rooted at the
      receiver.  Answer the root node of the new subtree.  
    '''
    child = self.right
    if (child == None):
        print( 'Error!  No right child in rotateLeft.' )
        return None  # redundant
    else:
        self.right = child.left
        child.left = self
        return child


        # A = self.node 
        # B = self.node.right.node 
        # T = B.left.node 
        
        # self.node = B 
        # B.left.node = A 
        # A.right.node = T 

  def rotateRight(self):
    '''  Perform a right rotation of the subtree rooted at the
      receiver.  Answer the root node of the new subtree.  
    '''
    child = self.left
    print(child.item)
    if (child == None):
        print( 'Error!  No left child in rotateRight.' )
        return None  # redundant
    else:
        self.left = child.right
        child.right = self
        return child

  def rotateRightThenLeft(self):
    '''Perform a double inside left rotation at the receiver.  We
      assume the receiver has a right child (the bad child), which has a left 
      child. We rotate right at the bad child then rotate left at the pivot 
      node, self. Answer the root node of the new subtree.  We call this 
      case 3, subcase 2.
    '''
    pass
    
  def rotateLeftThenRight(self):
    '''Perform a double inside right rotation at the receiver.  We
      assume the receiver has a left child (the bad child) which has a right 
      child. We rotate left at the bad child, then rotate right at 
      the pivot, self.  Answer the root node of the new subtree. We call this 
      case 3, subcase 2.
    '''
    pass
   
class AVLTree:
  def __init__(self, count=0, root=None):
    self.root = root
    self.count = count
      
  def __str__(self):
    st = 'There are ' + str(self.count) + ' nodes in the AVL tree.\n'
    return  st + str(self.root)  # Using the string hook for AVL nodes
 
  def insert(self, newItem):
    '''  Add a new node with item newItem, if there is not a match in the 
      tree.  Perform any rotations necessary to maintain the AVL tree, 
      including any needed updates to the balances of the nodes.  Most of the 
      actual work is done by other methods.
    '''
    self.count += 1
    found, pathStack, parent, pivot = self.search(newItem)

    if parent == None:
      self.root = AVLNode(newItem)

    elif not found:
      if pivot == None:
        print("CASE ONE INSERTING", newItem)

        if newItem > parent.item:
          parent.right = AVLNode(newItem)
        else:
          parent.left = AVLNode(newItem)
        self.case1(pathStack, pivot, newItem)
      else:
        print("PARENT OF NODE IS", parent.item)
        print("PIVOT IS", pivot.item)
        print("PIVOT BALANCE IS", pivot.balance)


        leftDepth = AVLNode.depth(pivot.left)
        rightDepth = AVLNode.depth(pivot.right)

        insertingDirection = "right" if newItem > pivot.item else "left"
        inbalanceDirection = "right" if rightDepth > leftDepth else "left"

        if newItem > parent.item:
            parent.right = AVLNode(newItem)
        else:
            parent.left = AVLNode(newItem)

        if insertingDirection != inbalanceDirection:
          print("CASE TWO INSERTING", newItem)
          self.case2(pathStack, pivot, newItem)
        else:
          self.case3(pathStack, pivot, newItem, inbalanceDirection)
        # else:
        #   self.case3(pathStack, pivot, newItem)


    return found, pathStack, parent, pivot

  def adjustBalances(self, theStack, pivot, newItem):
    '''  We adjust the balances of all the nodes in theStack, up to and
        including the pivot node, if any.  Later rotations may cause
        some of the balances to change.
    '''
    pivotAdjused = False
    while len(theStack) > 0 and not pivotAdjused:
      current = theStack.pop()
      if newItem > current.item:
        current.balance += 1
      else:
        current.balance -= 1
      if current == pivot:
        pivotAdjused = True       
    
  def case1(self, theStack, pivot, newItem):
    '''  There is no pivot node.  Adjust the balances of all the nodes
        in theStack.
    '''
    self.adjustBalances(theStack, pivot, newItem)
          
  def case2(self, theStack, pivot, newItem):
    ''' The pivot node exists.  We have inserted a new node into the
        subtree of the pivot of smaller height.  Hence, we need to adjust 
        the balances of all the nodes in the stack up to and including 
        that of the pivot node.  No rotations are needed.
    '''
    self.adjustBalances(theStack, pivot, newItem)
        
  def case3(self, theStack, pivot, newItem, pivotInbalanceDirection):
    '''  The pivot node exists.  We have inserted a new node into the
        larger height subtree of the pivot node.  Hence rebalancing and 
        rotations are needed.
    '''
    self.adjustBalances(theStack, pivot, newItem)
    # After adjusting balance
    print(pivot.balance)
    if pivot.balance > 0:
      badChild = pivot.right
    else:
      badChild = pivot.left

    print("BAD CHILD IS", badChild.item)

    badChildinsertingDirection = "right" if newItem > badChild.item else "left"

    print("BAD CHILD INSERTING DIR", badChildinsertingDirection)
    pivotsParent = theStack.pop() if len(theStack) > 0 else None

    if pivotInbalanceDirection == badChildinsertingDirection:
      print("CASE THREE (A) INSERTING", newItem)
      if badChildinsertingDirection == "left":
        print("ROTATING RIGHT")
        pivotsParent.right = pivot.rotateRight()
      else:
        print("ROTATING LEFT")
        pivotsParent.left = pivot.rotateLeft()
      
      pivot.balance = 0
      badChild.balance = 0
    else:
      # CASE 3b
      print("CASE THREE (B) INSERTING", newItem)
      pass
  # Lots more!!!!
        
  def search(self, newItem):
    '''  The AVL tree is not empty.  We search for newItem. This method will 
      return a tuple: (pivot, theStack, parent, found).  
      In this tuple, if there is a pivot node, we return a reference to it 
      (or None). We create a stack of nodes along the search path -- theStack. 
      We indicate whether or not we found an item which matches newItem.  We 
      also return a reference to the last node the search examined -- referred
      to here as the parent.  (Note that if we find an object, the parent is 
      reference to that matching node.)  If there is no match, parent is a 
      reference to the node used to add a child in insert().
    '''
    found, pathStack, parent, pivot = False, [], self.root, None
    if self.count > 0:
      node = self.root

      while node != None and not found:
        if newItem == node.item:
          found = True
        else:
          pathStack.append(node)
          parent = node

          if node.balance != 0:
            pivot = node

          if newItem > node.item:
            node = node.right
          else:
            node = node.left

    return found, pathStack, parent, pivot
  

            
            
def main():
  print()
  #  a = AVLNode(20, -1)
  #  b = AVLNode( 30, -1)
  #  c = AVLNode(-100)
  #  d = AVLNode(290)

  #  print(a)
  #  print(b)

  t = AVLTree()
  #  t.root = b
  #  b.left = a
  #  a.left = c
  #  b.right = d
  #  t.count = 4
  #  print(t)

  #  print(t.search(-100))
  # print(t.insert(10))
  # print(t)
  # print(t.insert(3))
  # print(t)
  # t.insert(18)
  # print(t)
  # t.insert(2)

  # print(t)
  # t.insert(13)
  # print(t)
  # t.insert(4)
  # print(t)
  # t.insert(40)
  # print(t)
  # t.insert(39)
  # print(t)
  # t.insert(12)
  # print(t)
  # t.insert(14)
  # print(t)
  # t.insert(38)
  # print(t)

  t.insert(25)
  print(t)
  t.insert(15)
  print(t)
  t.insert(40)
  print(t)
  t.insert(50)
  print(t)
  t.insert(65)
  print(t)

  # found, pathStack, parent, pivot = t.insert(65)
  # print(found)
  # print([n.item for n in pathStack])
  # print(parent.item)
  # print(parent.item)
  # print()
              
  #  a = AVLNode(50)
  #  b = AVLNode(30)
  #  c = AVLNode(40)
  #  a.left = b
  #  b.right = c
  #  print("Testing rotateLeftThenRight()")
  #  print(a.rotateLeftThenRight())
              
  #  (pivot, theStack, parent, found) = t.search(-70)
  #  print(pivot.item, parent.item, found)
  #  print()
  #  print("The items in the nodes of the stack are: ")
  #  while not theStack.isEmpty():
  #     current = theStack.pop()
  #     print(current.item)
  #  print()

  #  (pivot, theStack, parent, found) = t.search(25)
  #  print(pivot.item, parent.item, found)
   
  #  (pivot, theStack, parent, found) = t.search(-100)
  #  print(pivot.item, parent.item, found)

  #  n1 = AVLNode(50,0)
  #  n2 = AVLNode(75,0)
  #  n3 = AVLNode(62,0,n1,n2)

  #  tree = AVLTree(3,n3)
   
if __name__ == '__main__': main()
'''  The output from main():
[evaluate avltree.py]
Our names are
There are 4 nodes in the AVL tree.
-100 0
20 -1
30 -1
290 0

Testing rotateLeftThenRight()
30 0
40 0
50 0

20 -100 False

The items in the nodes of the stack are: 
-100
20
30

20 20 False
20 -100 True
'''
