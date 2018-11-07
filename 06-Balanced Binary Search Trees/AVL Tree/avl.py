'''
  File:  avltree.py 
  Author: Steve Hubbard,  and 
  Date:  
  Description:  This module provides the AVLNode and AVLTree classes.
'''

class Stack(object):
    """docstring for Stack."""
    def __init__(self):
        self.items = []
        
    # push element on to the stack.
    def push(self, item):
        self.items.append(item)
        
    # pop element from the stack.
    def pop(self):
        return self.items.pop()
        
    # peek element at top of the stack. Will throw error if empty.
    def peek(self):
        return self.items[len(self.items)-1]
    
    # Boolean True if stack is empty.
    def isEmpty(self):
        return len(self.items) == 0
    
    # Numbers of element in the stack.
    def size(self):
        return len(self.items)

class AVLNode:
  def __init__(self, item, balance = 0, left=None, right=None):
    self.item = item
    self.left = left
    self.right = right
    self.balance = balance

  def depth(node):
    if node == None:
      return 0
    return max(node.left.depth() if node.left else 0, node.right.depth() if node.right else 0) + 1
  
  def check(self):
    if node != None:
      if self.balance > 2 or self.balance < -2:
        raise Exception("Wrong balance at node: {}".format(self.item))
      
      AVLNode.depth(self.right) 
      AVLNode.depth(self.left)

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

  def __repr__(self):
    return "AVLNode("+repr(self.item)+", balance="+ \
    repr(self.balance)+", left="+repr(self.left)+ \
    ", right="+repr(self.right)+")"
  
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

  def rotateRight(self):
    '''  Perform a right rotation of the subtree rooted at the
      receiver.  Answer the root node of the new subtree.  
    '''
    child = self.left
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
    self.right = self.right.rotateRight()
    return self.rotateLeft()
    
  def rotateLeftThenRight(self):
    '''Perform a double inside right rotation at the receiver.  We
      assume the receiver has a left child (the bad child) which has a right 
      child. We rotate left at the bad child, then rotate right at 
      the pivot, self.  Answer the root node of the new subtree. We call this 
      case 3, subcase 2.
    '''
    self.left = self.left.rotateLeft()
    return self.rotateRight()
   
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

        if newItem > parent.item:
          parent.right = AVLNode(newItem)
        else:
          parent.left = AVLNode(newItem)
        self.case1(pathStack, pivot, newItem)
      else:

        insertingDirection = "right" if newItem > pivot.item else "left"
        inbalanceDirection = "right" if pivot.balance > 0 else "left"

        if newItem > parent.item:
            parent.right = AVLNode(newItem)
        else:
            parent.left = AVLNode(newItem)

        if insertingDirection != inbalanceDirection:
          self.case2(pathStack, pivot, newItem)
        else:
          self.case3(pathStack, pivot, newItem)

  def adjustBalances(self, theStack, pivot, newItem):
    '''  We adjust the balances of all the nodes in theStack, up to and
        including the pivot node, if any.  Later rotations may cause
        some of the balances to change.
    '''
    pivotAdjusted = False
    while (not theStack.isEmpty()) and (not pivotAdjusted):
      current = theStack.pop()
      if newItem > current.item:
        current.balance += 1
      elif newItem < current.item:
        current.balance -= 1
      if current == pivot:
        pivotAdjusted = True       
    
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
        
  def case3(self, theStack, pivot, newItem):
    '''  The pivot node exists.  We have inserted a new node into the
        larger height subtree of the pivot node.  Hence rebalancing and 
        rotations are needed.
    '''
    self.adjustBalances(theStack, pivot, newItem)

    pivotInbalanceDirection = "right" if pivot.balance > 0 else "left"
    badChild = pivot.right if pivot.balance > 0 else pivot.left
    badGrandChild = badChild.right if badChild.balance > 0 else badChild.left

    if badGrandChild.item == newItem:
      badGrandChild = None

    badChildinsertingDirection = "right" if newItem > badChild.item else "left"
    pivotsParent = theStack.pop() if (not theStack.isEmpty()) else pivot

    if pivotInbalanceDirection == badChildinsertingDirection:
      if badChildinsertingDirection == "left":
        if pivotsParent == pivot:
          self.root = pivot.rotateRight()
        else:
          if newItem > pivotsParent.item:
            pivotsParent.right = pivot.rotateRight()
          else:
            pivotsParent.left = pivot.rotateRight()
      else:
        if pivotsParent == pivot:
          self.root = pivot.rotateLeft()
        else:
          if newItem > pivotsParent.item:
            pivotsParent.right = pivot.rotateLeft()
          else:
            pivotsParent.left = pivot.rotateLeft()
      
      pivot.balance = 0
      badChild.balance = 0
    else:
      # CASE 3b
      if pivotInbalanceDirection == "left":
        self.root = pivot.rotateLeftThenRight()
      else:
        self.root = pivot.rotateRightThenLeft()

      if badGrandChild == None:
        pivot.balance = 0
        badChild.balance = 0
      else:
        badGrandChild.balance = 0
        if badChildinsertingDirection == "right":
          if newItem < badGrandChild.item:
            badChild.balance = 0
            pivot.balance = 1
          else:
            badChild.balance = -1
            pivot.balance = 0
        else:
          if newItem < badGrandChild.item:
            badChild.balance = 1
            pivot.balance = 0
          else:
            badChild.balance = 0
            pivot.balance = -1

        
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
    found, pathStack, parent, pivot = False, Stack(), self.root, None
    if self.count > 0:
      node = self.root

      while node != None and not found:
        if newItem == node.item:
          found = True
        else:
          pathStack.push(node)
          parent = node

          if node.balance != 0:
            pivot = node

          if newItem > node.item:
            node = node.right
          else:
            node = node.left
    return found, pathStack, parent, pivot

  def __pushLefts(root, stck):
      while root != None:
          stck.append(root)
          root = root.left

  def __iter__(self):
      nodeStack = []
      root = self.root
      AVLTree.__pushLefts(root, nodeStack)

      # Depth first search on the current node.
      while len(nodeStack) > 0:
          top = nodeStack.pop()
          yield top.item
          AVLTree.__pushLefts(top.right, nodeStack)
  
  def __repr__(self):
    return repr(self.root)
  

            
            
def main():
  print()
  t = AVLTree()
  # a = AVLNode(20, -1)
  # b = AVLNode( 30, -1)
  # c = AVLNode(-100)
  # d = AVLNode(290)

  # #  print(a)
  # #  print(b)

  # t.root = b
  # b.left = a
  # a.left = c
  # b.right = d
  # t.count = 4
  # print(t)

  # print(t.search(-100))
  vals = [10,3,18,2,13,4,40,39,12,14,38,11]
  # vals = [25,15,40,50,65,33]
  # vals = range(1,5)
  for v in vals:
    t.insert(v)
  print(repr(t))

  # for i in t:
  #   print(i)
              
  # a = AVLNode(50)
  # b = AVLNode(30)
  # c = AVLNode(40)
  # a.left = b
  # b.right = c
  # print("Testing rotateLeftThenRight()")
  # print(a.rotateLeftThenRight())


  # found, pathStack, parent, pivot = t.search(-70)
  # print(pivot.item, parent.item, found)
  # print()
  # print("The items in the nodes of the stack are: ")
  # while not pathStack.isEmpty():
  #   current = pathStack.pop()
  #   print(current.item)
  # print()

  # (pivot, pathStack, parent, found) = t.search(25)
  # print(pivot.item, parent.item, found)
  
  # (pivot, pathStack, parent, found) = t.search(-100)
  # print(pivot.item, parent.item, found)

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
