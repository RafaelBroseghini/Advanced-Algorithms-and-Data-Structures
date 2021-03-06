"""
Author: Rafael Broseghini
Prof: Dr. Kent Lee

Date: 08/25/2018
"""

def main():
    #7
    hashTable = dict()
    hashTable["Kent"]  = "Denise"
    hashTable["Steve"] = "Lindy"

    #8
    # The method __lt__ is called when comparing objects via the < operator.
    # In the example from the textbook we would have to examine the 'x' class
    # to understand exactly the underlying implementation of 'x' < 'y' since 'x' is on the left side
    # of the operation.

    #9
    # The method __lshift__ is called when comparing objects through the << operator.
    # This is a bitwise operation that returns 'a' shifted left by 'b' amount.

    #10
    # The loop and a half problem relates to trying to read records from a file when
    # these may cross multiple lines. The key here is that each line is 
    # part of a set of steps. To perform a certain action we must try to read 
    # a little bit of the record and perform a step by step approach accordingly. 
    # Reading a record allows the algorithm to know how many more lines to check and so forth.
    # The program stops execution once we reach an empty line/EOF.

    #11
    # No. Using the loop and a half solution to read an XML file would be extremely
    # difficult since XML files are not line oriented and XML commands have attributes
    # within themselves. Furthermore, any changes that we wish to make to the input file,
    # would result in changing the program that reads such file, which ultimately
    # would be time consuming and confusing as programs grow larger.
    # In this case it is easier to use a parser that allows us to 
    # access each XML commands' attributes and child data. Lastly, XML is extensively supported.

    #12 
    # Polymorphism refers to the ability to implement the same method differently on different
    # objects. Each method will depend on how it is implemented within each specific object.
    # These methods are often not built in to the Python language and only defined by the
    # programmer. Python is a dynamically typed language, so we can call any method and if 
    # it is defined at run-time, the interpreter understands which object it encapsulates the method
    # and calls it accordingly.

    # Operator Overloading lets you redefine the meaning of an operator respective to your class.
    # For example a developer may choose to give a new implementation to the __add__, __eq__, __iter__ 
    # methods (previously defined in the Python language) that may be slightly different than previous 
    # implementations and suit their program in a desired way.

    #13
    # Are the numbers only positive?
    # Are the numbers always bigger than 2?
    # These are edge cases that may change a more thorough implementation.
    
    inp = int(input("Enter an integer: "))
    total = 2
    for number in range(4, inp+1, 2):
        total += number
        
    print(total)

    # We may also use the while loop.
    inp = int(input("Enter an integer: "))
    total = 0
    runner = 2

    while runner <= inp:
        total += runner
        runner += 2

    print(total)
    

if __name__ == '__main__':
    main()
