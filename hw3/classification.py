import sys
from copy import deepcopy
import time
import pdb

start_time = time.time()

def main():
    ### Files to train from and save training data ###
    trainingDigitFile = "./digitdata/trainingimages"
    trainingValueFile = "./digitdata/testlabels"
    output_file = "./training.txt"
    ### Size of picture in pixels ###
    M = 28
    trainVal = list()
    ### Initialize the training lists with one gray and one black pixel in each location ###
    ### Initialize to one for laplacian smoothing ###
    ### KEY : [Number][black/gray][row][column] ###
    trainedList = {0: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   1: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   2: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   3: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   4: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   5: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   6: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   7: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   8: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]],
                   9: [[[1 for i in range(M)] for j in range(M)],[[1 for i in range(M)] for j in range(M)]]}
    read_trainingVal(trainingValueFile, trainVal)
    train_network(trainingDigitFile, trainVal, trainedList)
    write_training(output_file, trainedList)
    return

def read_trainingVal(input_file, trainVal):
    with open(input_file) as f:
        for line in f:
            trainVal.append(line[0])

def train_network(input_file, trainVal, trainedList):
    trainValNumber = 0
    i = 0 #line in picture
    j = 0 #pixel in line
    with open(input_file) as f:
        curNumber = int(trainVal[trainValNumber])
        for line in f:
            if i <= 28:
                trainValNumber+=1
                if trainValNumber==len(trainVal):
                    print "Error: More Train Values than Train Digits"
                    sys.exit()
                curNumber = int(trainVal[trainValNumber])
                i = 0
            j = 0
            for letter in line:
                if letter == '\n':
                    continue
                ### If gray, add .5 to black and 1 to gray ###
                elif letter == '+':
                    trainedList[curNumber][0][i][j]+=.5
                    trainedList[curNumber][1][i][j]+=1
                ### If black, add .5 to gray and 1 to black ###
                elif letter == '#':
                    trainedList[curNumber][0][i][j]+=1
                    trainedList[curNumber][1][i][j]+=.5
                j+=1
            i+=1

def write_training(output_file, data):
    with open(output_file, 'w') as outfile:
        outfile.write("Training data\n")
        for x in range(10):
            print str(x) + ":"
            print "Black:"
            for j in range(28):
                print data[x][0][j]
            print "Gray"
            for j in range(28):
                print data[x][0][j]



if __name__ == "__main__":
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
