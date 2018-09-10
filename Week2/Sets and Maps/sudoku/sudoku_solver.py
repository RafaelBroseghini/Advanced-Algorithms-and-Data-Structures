#! bin/env/usr python

"""
Python script for solving sudoku using sets.

The sudoku matrix must be 9x9.
"""

__author__ = "Rafael Broseghini"


def create_puzzle(filename):
    matrix = []
    with open(filename) as infile:
        for line in infile:
            row = []
            line = line.split()
            for elem in line:
                if elem != "x":
                    elem = int(elem)
                row.append(elem)
            matrix.append(row)
    
    return matrix

def form_puzzle(matrix):

    rows = len(matrix)
    cols = len(matrix[0])

    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == "x":
                matrix[row][col] = set([1,2,3,4,5,6,7,8,9])

    return matrix

def getGroups(matrix):
    # Adding rows to groups. Here we make a new object (list) 
    # via the list method that takes an iterator and returns a new object.
    groups = list(matrix)

    rows = len(groups)
    cols = len(groups[0])

    # Adding columns to groups
    for row in range(rows):
        g = []
        for col in range(cols):
            g.append(matrix[col][row])
        groups.append(g)
    
    # Adding squares to groups.
    # This iterates over rows.
    for i in range(0, 9, 3):
        #This iterates over the columns.
        for j in range(0, 9, 3):
            g = []
            # This iterates in range of row, row+3
            for k in range(i, i+3):
                # This iterates in range of column, column+3
                for m in range(j, j+3):
                    g.append(matrix[k][m])
            groups.append(g)

    return groups

def reduceGroups(groups):
    pass

def reduce_groups(matrix):
    changed = True
    groups = getGroups(matrix)

    while changed:
        changed = reduceGroups(groups)

   
def main():
    x = create_puzzle("sudoku1.txt")
    y = form_puzzle(x)
    z = getGroups(y)

    print(len(z))
    # print(z)
if __name__ == '__main__':
    main()
