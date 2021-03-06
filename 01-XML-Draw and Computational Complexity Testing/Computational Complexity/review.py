"""
Author: Rafael Broseghini
Prof: Dr. Kent Lee

Date: 08/27/2018
"""

#1
"""
A Python list behaves like a bunch of post office boxes
as each index in the list has an unique address like a post office and can hold/store value to it.
"""
#2
"""
Accessing an element in a Python list is not like accessing the contents
of a post office box as the number of boxes grow larger there would be 
more time spent on searching for a specific box. Although for an index in
a Python list the access/retrieval time is constant as this action behaves more
like calling a person's name in a group as everyone is listening and takes little
time to respond to the call.
"""
#3
# In Python a useful way to calculate runtime in seconds is to use the module time. See example below.
import time
start = time.time()
lst = list(range(10000000))
end = time.time()
print(end-start,"seconds.")

#4
"""
In terms of algorithmic complexity an algorithm with a quadratic order of growth
is better than a exponential (2^n) order of growth algorithm. For small input sizes these
algorithms may perform similarly but as input size grows larger the exponential algorithm would
take much longer to finish.
"""

#5
"""
An O(n^2) algorithm means that its order of growth is quadratic. In other words, as the input size
grows, runtime increases in a quadratic manner. If for 10 elements input size the algorithm takes 10 seconds, the
same algorithm with 20 elements as input size would take 100 seconds to finish.
"""

#6
"""
When proving by induction the two parts there are there are the base case (initial step), often proved
by subtistuting n with 1. The second step is the inductive hypothesis to be satisfied.
"""

#7
"""
This algorithm would run in a O(n^2) fashion. Even though the number of operations decreases by 2
each time through the loop the dominant term in the final equation would be n^2 (n^2/4 + n/2), and dropping the non
dominant terms would result in a O(n^2) time complexity.
"""

#8
"""
It is hard to state the algorithmic complexity of both algorithms if we only know
it's number of steps for one input size n.

It can be the case where they have the same time complexity of O(n), O(n^2) or even O(1) despite algorithm 'B'
taking more steps. These steps could be addition, multiplication, nested loops etc. It is difficult to conclude with
only one input size. I would be able to better evaluate their asympotic notations if other runtimes given the respective
input sizes were provided.
"""

#9
"""
The built in append operation of a Python list is more efficient than the []+[] operation because
it does not require to realocate extra memory for a new copy of the original list and to copy every element from the
original list to the newly created list plus one element. Freeing memory and performing less nested loops 
are often good tradeoffs we should be aware of as these may increase significantly our algorithm's efficiency.
The only drawback with the append method is the amortized case of resizing the list, that may seem like a O(n) amortized case.
Although as we will learn this amortized computational complexity is of O(1) order of growth. Not so bad.
"""

#10
"""
I can think of two different searching algorithms: sequential search and binary search.

Although it is important to be aware of potential constraints. For example, a sequential search on a
ordered list is a different algorithm than a sequential search on an unordered list.

A binary search algorithm must search on a sorted list since binary search cannot traverse an unordered list.
Binary search is also very efficient as it is a O(log n) when speaking of asymptotic notation.

I will further describe a sequential search on a sorted list of only integers.

Pseudo code:
1. Start at the first element.
2. check if it is equal to the element we are searching.
3. if true return True
4. if it is less keep repeating step 2 until we find the element or reach an element higher than the target.
5. Return False
"""