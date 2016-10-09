import sys
from copy import deepcopy
import time
import pdb

start_time = time.time()

def main():
    if len(sys.argv)!=3:
        print("No word bank file or no puzzle. Provide a word bank and a puzzle to solve and rerun.")
        return

    w, h = 9, 9
    puzzle = [[0 for y in range(h)] for x in range(w)] #declare a 2d array to hold the puzzle
    word_bank = []
    frontierTree = {}

    readBank(sys.argv[1], word_bank) #word_bank now holds all the words given
    readPuzzle(sys.argv[2], puzzle, w)

    expandState(puzzle, word_bank[0], frontierTree) #expand the first word into the state

    while len(frontierTree) != 0:
        expandState((frontierTree[word_bank[0]])[0],word_bank[len(frontierTree)],frontierTree)
        break

    for layer in frontierTree.values():
        for state in layer:
            for row in state:
                for val in row:
                    print '{:1}'.format(val),
                print
            print
        print
        print
    # while len(frontier)!=0:
    #     expandState(puzzle, curWord, frontier)

    # print frontier
    # for row in puzzle:
    #     for val in row:
    #         print '{:1}'.format(val),
    #     print
    # word_bank.sort(key=len, reverse=True) #sort word_bank by most constraining to least constraining
    # print word_bank
    return

def readBank(input_file, word_bank):
    with open(input_file) as f:
        for line in f:
            insertString = line[:-2]
            word_bank.append(insertString.upper()) #removes the new line characters from file reading

def readPuzzle(input_file, puzzle, w):
    x, y = 0, 0
    with open(input_file) as f:
        for line in f:
            for letter in line:
                if letter != '\r' and letter != '\n': #removes new line cahracters while file reading
                    puzzle[x][y]=letter
                    y+=1
            x+=1
            y=0


def expandState(puzzle, curWord, frontier):
    for row in puzzle:
        for val in row:
            print '{:1}'.format(val),
        print
    frontier[curWord]=list()
    for x in range(9): #column search
        for y in range(9):
            z = 0 #curWord letter counter
            if len(curWord)+y > 9: #if curword doesn't fit in line, skip to next line
                break
            while curWord[z]==puzzle[x][y+z] or puzzle[x][y+z]=='_':
                if not regionCheck(puzzle, curWord[z], x, y+z): #check the letter region
                    break
                z+=1
                if z==len(curWord):
                    puzzleCpy=deepcopy(puzzle)
                    for a in range(len(curWord)):
                        puzzleCpy[x][a+y]=curWord[a]

                    # for row in puzzleCpy:
                    #     for val in row:
                    #         print '{:1}'.format(val),
                    #     print

                    frontier[curWord].append(puzzleCpy)
                    break
                if y+z >=9:
                    break

    for y in range(9): #row search
        for x in range(9):
            z = 0 #curWord letter counter
            if len(curWord)+x > 9: #if curword doesn't fit in line, skip to next line
                break
            while curWord[z]==puzzle[x+z][y] or puzzle[x+z][y]=='_':
                if not regionCheck(puzzle, curWord[z], x+z, y): #check the letter region
                    break
                z+=1
                if z==len(curWord):
                    puzzleCpy=deepcopy(puzzle)
                    for a in range(len(curWord)):
                        puzzleCpy[a+x][y]=curWord[a]

                    # for row in puzzleCpy:
                    #     for val in row:
                    #         print '{:1}'.format(val),
                    #     print

                    frontier[curWord].append(puzzleCpy)
                    break
                if x+z >=9:
                    break
    return

def regionCheck(puzzle, letter, x, y): #checks to see if the letter is unique in its 3x3 square
    if x < 3:
        for w in range(3):
            for h in range(3):
                if letter == puzzle[x][y]:
                    return False
    elif x < 6:
        for w in range(3,6):
            for h in range(3,6):
                if letter == puzzle[x][y]:
                    return False
    else:
        for w in range(6,9):
            for h in range(6,9):
                if letter == puzzle[x][y]:
                    return False
    return True

if __name__ == "__main__":
    pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

'''
Ways to improve algorithm:
1. Early failure detection
2. Better most constraining variable detection
3. Arc consistency
-Keep map with possible locations. Using start position, orientation, and length?
'''
