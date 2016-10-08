import sys
import time
import pdb

start_time = time.time()

def main():
    if len(sys.argv)==2:
        print("No word bank file or no puzzle. Provide a word bank and a puzzle to solve and rerun.")
        return

    w, h = 9, 9
    puzzle = [[0 for x in range(w)] for y in range(h)] #declare a 2d array to hold the puzzle
    word_bank = []
    frontier = []

    readBank(sys.argv[1], word_bank) #word_bank now holds all the words given
    readPuzzle(sys.argv[2], puzzle, w)

    for curWord in word_bank:
        expandState(puzzle, curWord, frontier)
        break

    print frontier
    # for line in puzzle:
    #     print line
    # word_bank.sort(key=len, reverse=True) #sort word_bank by most constraining to least constraining
    # print word_bank
    return

def readBank(input_file, word_bank):
    with open(input_file) as f:
        for line in f:
            word_bank.append(line[:-2]) #removes the new line characters from file reading

def readPuzzle(input_file, puzzle, w):
    x, y = 0, 0
    with open(input_file) as f:
        for line in f:
            for letter in line:
                if letter != '\r' and letter != '\n': #removes new line cahracters while file reading
                    puzzle[x][y]=letter
                    x+=1
            y+=1
            x=0


def expandState(puzzle, curWord, frontier):
    for x in range(9): #column search
        for y in range(9):
            z = 0 #curWord letter counter
            if len(curWord)+y > 9: #if curword doesn't fit in line, skip to next line
                break
            while curWord[z]==puzzle[x][y+z] or puzzle[x][y+z]=='_':
                z+=1
                if z==len(curWord):
                    stringInsert = str(x)+str(y)
                    frontier.append(stringInsert)
                    break
                if y+z >=9:
                    break

    for y in range(9): #row search
        for x in range(9):
            z = 0 #curWord letter counter
            if len(curWord)+x > 9: #if curword doesn't fit in line, skip to next line
                break
            while curWord[z]==puzzle[x+z][y] or puzzle[x+z][y]=='_':
                z+=1
                if z==len(curWord):
                    stringInsert = str(x)+str(y)
                    frontier.append(stringInsert)
                    break
                if x+z >=9:
                    break
    return

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
