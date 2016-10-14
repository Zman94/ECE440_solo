import sys
from copy import deepcopy
import time
import pdb

start_time = time.time()

def main():
    if len(sys.argv)!=3:
        print("No word bank file or no puzzle. Provide a word bank and a puzzle to solve and rerun.")
        return

    nodes_expanded = [0]
    w, h = 9, 9
    puzzle = [[0 for y in range(h)] for x in range(w)] #declare a 2d array to hold the puzzle
    word_bank = []
    frontierTree = {}
    word_location = []

    readBank(sys.argv[1], word_bank) #word_bank now holds all the words given
    readPuzzle(sys.argv[2], puzzle, w)
    # word_bank=["AHGGGGGGG"]

    hasAnswer = dfsExpandState(word_location, puzzle,word_bank,frontierTree, nodes_expanded)

    if not hasAnswer:
        print "The maze given has no solution for the given word bank."
        return

    ### Print execution information ###
    print str(nodes_expanded[0])+" nodes were expanded."
    print
    for word in word_location:
        print word[1][2]+","+word[1][1]+","+word[1][0]+": "+word[0]
    print
    for state in frontierTree[word_bank[-1]]:
        if len(state) < 4:
            continue
        for row in state:
            for val in row:
                print '{:1}'.format(val),
            print
        break
    print

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

def dfsExpandState(word_location, puzzle, word_bank, frontierTree, nodes_expanded, layer=0, direction=True):
    if layer==len(word_bank):
        return True

    nodes_expanded[0]+=1
    expandState(puzzle, word_bank[layer], frontierTree, direction) #expand the first word into the state

    for frontier in frontierTree[word_bank[layer]]:
        if len(frontier) < 4: #skip any states that contain the coordinates of the words assignment and update the last used coordinates
            coordinates=frontier
            continue
        hasAnswer = dfsExpandState(word_location, frontier, word_bank, frontierTree, nodes_expanded, layer+1, not direction)
        if hasAnswer:
            word_location.insert(0,[word_bank[layer],coordinates])
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

                        frontier[curWord].append(str(x)+str(y)+"V")
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

                        frontier[curWord].append(str(x)+str(y)+"H")
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

                        frontier[curWord].append(str(x)+str(y)+"H")
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

                        frontier[curWord].append(str(x)+str(y)+"V")
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
