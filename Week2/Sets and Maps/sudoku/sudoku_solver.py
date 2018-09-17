#! bin/env/usr python

"""
Python script for solving sudoku using sets.

The algorithm below only solves sudoku puzzles
of 9x9 'cells'.

Steps:
    - Read puzzle from file.
    - Populate empty cells with values from {1...9}
    - Get rows, columns and squares as individual groups.
    - Iterate over groups applying rules 1 and 2. (described below)
        - Implement own HashSet data structure.
    - Print puzzle to console.
    - Write solved puzzle to a file.
"""

__author__ = "Rafael Broseghini"

from hashset import HashSet

def create_puzzle(filename):
    matrix = []
    # Change this to where your puzzles are located the file system.
    with open("sudoku_puzzles/{}".format(filename), "r+") as infile:
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
                matrix[row][col] = HashSet([1,2,3,4,5,6,7,8,9])
            else:
                matrix[row][col] = HashSet([matrix[row][col]])

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
    # Rule 1: HashSet cardinality and number of dups.
    for group in groups:
        for current_cell in group:
            dups = 0
            for other_cell in group:
                if other_cell == current_cell:
                    dups += 1

            if (dups == len(current_cell)) and (dups < 9):
                for other_cell in group:
                    if other_cell != current_cell and current_cell <= other_cell:
                        other_cell.difference_update(current_cell)
                        return True
    
    # Rule 2: HashSet difference when size = 1. Make a new copy of the item we are currently at.
    for group in groups:
        for i in range(0, len(group)):
            set_copy = HashSet(group[i])
            current_index = i
            for j in range(0, len(group)):
                if j != current_index:
                    set_copy.difference_update(group[j])

            if len(set_copy) == 1 and set_copy != group[i]:
                group[i].clear()
                group[i].update(set_copy)
                return True
                
    return False


def _reduce(matrix):
    changed = True
    groups = getGroups(matrix)

    while changed:
        changed = reduceGroups(groups)

    return matrix

def print_to_console(matrix):
    for group in matrix:
        for cell in group:
            cell = list(cell)
            print(("{} ".format(cell[0])), end="")
        print()

def save_to_file(groups, filename):
    with open("sudoku_solved_puzzles/{}".format(filename),"w+") as outfile:
        for group in groups:
            for cell in group:
                cell = list(cell)
                outfile.write("{} ".format(cell[0]))
            outfile.write("\n")

def main():
    # Change the range if you have more than 6 sudoku files.
    # for i in range(1,7):
    #     infile = "sudoku"+str(i)+".txt"
    #     outfile = "sudoku"+str(i)+"_solved.txt"

    print("Which sudoku puzzle would you like to solve? ")
    print("\n+ =========== +")
    for i in range(1,7):
        print("+ \033[1;32msudoku{}.txt\033[0m +".format(str(i)))
    print("+ =========== +\n")
    infile = input("Your choice: ")

    original_puzzle = create_puzzle(infile)
    populated_set_puzzle = form_puzzle(original_puzzle)
    solved_puzzle = _reduce(populated_set_puzzle)

    print_to_console(solved_puzzle)

    # save_to_file(solved_puzzle, outfile)
if __name__ == '__main__':
    main()
