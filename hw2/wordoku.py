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
    # word_bank=["AHGGGGGGG"]

    hasAnswer = dfsExpandState(puzzle,word_bank,frontierTree)

    if not hasAnswer:
        print "The maze given has no solution for the given word bank."
        return


    for layer in frontierTree.values():
        for state in frontierTree[word_bank[-1]]:
            for row in state:
                for val in row:
                    print '{:1}'.format(val),
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
    word_bank.sort(key=len, reverse=True)

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

def dfsExpandState(puzzle, word_bank, frontierTree, layer=0, direction=True):
    if layer==len(word_bank):
        return True

    ### Debugging Print Statements ###
    # print word_bank[layer]
    # for row in puzzle:
    #     for val in row:
    #         print '{:1}'.format(val),
    #     print
    # print

    expandState(puzzle, word_bank[layer], frontierTree, direction) #expand the first word into the state

    for frontier in frontierTree[word_bank[layer]]:
        hasAnswer = dfsExpandState(frontier, word_bank, frontierTree, layer+1, not direction)
        if hasAnswer:
            return True
    return False

def expandState(puzzle, curWord, frontier, direction):
    # for row in puzzle:
    #     for val in row:
    #         print '{:1}'.format(val),
    #     print

    ### Debugging Print Statements ###
    # print direction
    # print curWord
    # for row in puzzle:
    #     for val in row:
    #         print '{:1}'.format(val),
    #     print
    # print

    frontier[curWord]=list()
    if direction:
        for x in range(9): #column search
            for y in range(9):
                z = 0 #curWord letter counter
                if len(curWord)+y > 9: #if curword doesn't fit in line, skip to next line
                    break
                while (str(curWord[z])==str(puzzle[y+z][x])) or (puzzle[y+z][x]=="_"):
                    if not regionCheck(puzzle, curWord[z], x, y+z): #check the letter region
                        break
                    z+=1
                    if z==len(curWord):
                        puzzleCpy=deepcopy(puzzle)
                        for a in range(len(curWord)):
                            puzzleCpy[a+y][x]=curWord[a]

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
                while (str(curWord[z])==str(puzzle[y][x+z])) or (puzzle[y][x+z]=="_"):
                    if not regionCheck(puzzle, curWord[z], x+z, y): #check the letter region
                        break
                    z+=1
                    if z==len(curWord):
                        puzzleCpy=deepcopy(puzzle)
                        for a in range(len(curWord)):
                            puzzleCpy[y][x+a]=curWord[a]

                        # for row in puzzleCpy:
                        #     for val in row:
                        #         print '{:1}'.format(val),
                        #     print

                        frontier[curWord].append(puzzleCpy)
                        break
                    if x+z >=9:
                        break
    else:
        for y in range(9): #row search
            for x in range(9):
                z = 0 #curWord letter counter
                if len(curWord)+x > 9: #if curword doesn't fit in line, skip to next line
                    break
                while (str(curWord[z])==str(puzzle[y][x+z])) or (puzzle[y][x+z]=="_"):
                    if not regionCheck(puzzle, curWord[z], x+z, y): #check the letter region
                        break
                    z+=1
                    if z==len(curWord):
                        puzzleCpy=deepcopy(puzzle)
                        for a in range(len(curWord)):
                            puzzleCpy[y][a+x]=curWord[a]

                        # for row in puzzleCpy:
                        #     for val in row:
                        #         print '{:1}'.format(val),
                        #     print

                        frontier[curWord].append(puzzleCpy)
                        break
                    if x+z >=9:
                        break

        for x in range(9): #column search
            for y in range(9):
                z = 0 #curWord letter counter
                if len(curWord)+y > 9: #if curword doesn't fit in line, skip to next line
                    break
                while (str(curWord[z])==str(puzzle[y+z][x])) or (puzzle[y+z][x]=="_"):
                    if not regionCheck(puzzle, curWord[z], x, y+z): #check the letter region
                        break
                    z+=1
                    if z==len(curWord):
                        puzzleCpy=deepcopy(puzzle)
                        for a in range(len(curWord)):
                            puzzleCpy[a+y][x]=curWord[a]

                        # for row in puzzleCpy:
                        #     for val in row:
                        #         print '{:1}'.format(val),
                        #     print

                        frontier[curWord].append(puzzleCpy)
                        break
                    if y+z >=9:
                        break

    return

def regionCheck(puzzle, letter, x, y): #checks to see if the letter is unique in its 3x3 square
    if x < 3:
        if y < 3:
            for w in range(3):
                for h in range(3):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
        elif y < 6:
            for w in range(3):
                for h in range(3,6):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
        else:
            for w in range(3):
                for h in range(6,9):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
    elif x < 6:
        if y < 3:
            for w in range(3,6):
                for h in range(3):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
        elif y < 6:
            for w in range(3,6):
                for h in range(3,6):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
        else:
            for w in range(3,6):
                for h in range(6,9):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
    else:
        if y < 3:
            for w in range(6,9):
                for h in range(3):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
        elif y < 6:
            for w in range(6,9):
                for h in range(3,6):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
        else:
            for w in range(6,9):
                for h in range(6,9):
                    if x == w and y == h:
                        continue
                    if letter == puzzle[h][w]:
                        return False
    return True

if __name__ == "__main__":
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

'''
Ways to improve algorithm:
1. Early failure detection
2. Better most constraining variable detection
3. Arc consistency
-Keep map with possible locations. Using start position, orientation, and length?
'''
