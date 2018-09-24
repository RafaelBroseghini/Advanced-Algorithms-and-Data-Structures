import datetime 
import random
import time
        

"""
Step by step approach:
    - Build one list with integers of size 1 to 200, starting at 5.
    - Multiply each integer by itself 1000 times and record the time elapsed.
    - Build XML file to later display data via turtle graphics.

Findings:
    - For small integer sizes (0-10...15), the multiplication times
    presented a consistent constant (O(1)) algorithmic complexity.
    As numbers grew larger I have noticed a trend of a O(log(n)) nature.
    Every time I have ran the program it has never displayed any anomalies rather than
    what I believe to be some sort of garbage collect. Overall, it 
    has remained within a log algorithmic complexity with no anomalies. 

    There is a cutoff from O(1) to O(log n) due to Python's support for large integers in which
    numbers that are greater than 64bits/32bits carry their overflow over to 
    a new calculation which ultimately takes more time than multiplication between numbers that 
    are less than what the computer's architecture supports. The product of two large number needs more space in memory than previously allocated.
    Python also uses arbitrary precision arithmetic
    to prevent overflow and ensure correct results although it decreases performance. 

    I have found this explanation quite helpful : 'One of the solutions is to represent the integer as an array of digits. 
    To do it in an efficient way we need to convert our number from base 10 to base 2^30
    numeral system, where each element represents a single 'digit' in a range from 0 to 2^30 −1.
    Depending on the platform, Python uses either 32-bit unsigned integer arrays with 30-bit digits or
    16-bit unsigned integer arrays with 15-bit digits. Such integers are stored as an array of one element 
    and if it's possible treated as fixed 32-bit integers.'

    We may argue that a decrease in performance from constant to logarithmic is not that bad.

"""

def main():
    
    # Write an XML file with the results
    file = open("MultiplicationTiming.xml","w")
    
    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
    
    file.write('<Plot title="Constant Time Multiplication of Two Numbers">\n')
    
    # Start with integer of size one. 
    num = 5
     
    xList = []
    yList = []
    

    for x in range(200):

        xList.append(num)
        num *= 10
    
        
    for v in range(200):
        # Iterate over the list in ascending order
        # and perform 100 multiplications for each
        # integer size.
        index = v
        val = xList[index]

        starttime = datetime.datetime.now()

        #  Performing 100 multiplications on each integer size.
        #  Better benchmark, as multiplications are done really 
        # fast in a computer.
        for m in range(1000):
            prod = val * val

        endtime = datetime.datetime.now()
        # Time after the 100 test multiplications  
    
        # The difference in time between start and end.
        deltaT = endtime - starttime
    
        # Divide by 100 for the average multiplication time
        # But also multiply by 1000000 for microseconds.
        accessTime = (deltaT.total_seconds() / 100) * 1000
    
        yList.append(accessTime)
     
    file.write('  <Axes>\n')
    file.write('    <XAxis min="'+str(1)+'" max="'+str(len(str(xList[-1])))+'">Integer Size</XAxis>\n')
    
    # NOTE
    # Discuss microseconds and seconds metric.
    file.write('    <YAxis min="'+str(min(yList))+'" max="'+str(0.05)+'">Miliseconds</YAxis>\n')
    file.write('  </Axes>\n')
    
    file.write('  <Sequence title="Multiplication Time vs Integer Size" color="red">\n')   
    
    for i in range(len(xList)):   
        file.write('    <DataPoint x="'+ str(len(str(xList[i])))+'" y="'+str(yList[i])+'"/>\n')    
        
    file.write('  </Sequence>\n')
    file.write('</Plot>\n')
    file.close()  
    
if __name__ == "__main__":
    main()