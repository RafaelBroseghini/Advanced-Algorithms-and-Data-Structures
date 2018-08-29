import datetime 
import random
import time
        

"""
Steps:
build list with integers from one to 100.

perform 20 multiplications on integers of same size and time it.
"""

def main():
    
    # Write an XML file with the results
    file = open("ListAccessTiming.xml","w")
    
    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
    
    file.write('<Plot title="Constant Time Multiplication of Two Numbers">\n')
    
    # Start with integer of size one. 
    num = 5
    
    # # Record the list sizes in xList and the average access time within
    # # a list that size in yList for 1000 retrievals. 
    xList = []
    yList = []
    
    for x in range(100):

        xList.append(num)
        num *= 10
        
        # prod = 0
        
        # Creates a list of size x with all 0's
        # lst = [0] * x
        
        # let any garbage collection/memory allocation complete or at least
        # settle down
        # time.sleep(1)
        
        # Time before the 1000 test retrievals
        
    for v in range(100):
        # Iterate over the list in ascending order
        # and perform 100 multiplications for each
        # integer size.
        index = v
        val = xList[index]

        starttime = datetime.datetime.now()

        #  Performing 100 multiplications on each integer size.
        #  Better benchmark as multiplications are done really 
        # fast in a computer.
        for m in range(100):
            prod = val * val

        endtime = datetime.datetime.now()
        # Time after the 1000 test retrievals  
    
        # The difference in time between start and end.
        deltaT = endtime - starttime
    
        # Divide by 1000 for the average access time
        # But also multiply by 1000000 for microseconds.
        accessTime = deltaT.total_seconds() * 1000
    
        yList.append(accessTime)
     
    file.write('  <Axes>\n')
    file.write('    <XAxis min="'+str(1)+'" max="'+str(100)+'">Integer Size</XAxis>\n')
    
    # NOTE
    # Discuss microseconds and seconds metric.

    file.write('    <YAxis min="'+str(min(yList))+'" max="'+str(1)+'">Seconds</YAxis>\n')
    file.write('  </Axes>\n')
    
    file.write('  <Sequence title="Multiplication Time vs Integer Size" color="red">\n')   
    
    for i in range(len(xList)):   
        file.write('    <DataPoint x="'+str(len(str(xList[i])))+'" y="'+str(yList[i])+'"/>\n')    
        
    file.write('  </Sequence>\n')
    file.write('</Plot>\n')
    file.close()  
    
if __name__ == "__main__":
    main()