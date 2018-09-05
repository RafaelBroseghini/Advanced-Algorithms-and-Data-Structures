import datetime 
import random
import time
        

"""
Steps:
build list with integers increasing by order of 10.

perform 20 multiplications on integers of same size and time it.
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
    

    for x in range(100):

        xList.append(num)
        num *= 10
    
        
    for v in range(100):
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

    print(yList)
     
    file.write('  <Axes>\n')
    file.write('    <XAxis min="'+str(1)+'" max="'+str(len(str(xList[-1])))+'">Integer Size</XAxis>\n')
    
    # NOTE
    # Discuss microseconds and seconds metric.
    file.write('    <YAxis min="'+str(min(yList))+'" max="'+str(0.009)+'">Miliseconds</YAxis>\n')
    file.write('  </Axes>\n')
    
    file.write('  <Sequence title="Multiplication Time vs Integer Size" color="red">\n')   
    
    for i in range(len(xList)):   
        file.write('    <DataPoint x="'+ str(len(str(xList[i])))+'" y="'+str(yList[i])+'"/>\n')    
        
    file.write('  </Sequence>\n')
    file.write('</Plot>\n')
    file.close()  
    
if __name__ == "__main__":
    main()