from __future__ import print_function
import sys
from copy import deepcopy
import time
import pdb

start_time = time.time()

def main():
    ### Files to train from and save training data ###
    trainingDigitFile = "./digitdata/trainingimages"
    trainingValueFile = "./digitdata/traininglabels"
    output_file = "./training.txt"
    ### Files to test against ###
    testDigitFile = "./digitdata/testimages"
    testValueFile = "./digitdata/testlabels"
    ### Size of picture in pixels ###
    M = 28
    ### List to display numbers generated from AI ###
    numbers_classified = list()
    trainVal = list()
    testVal = list()
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
    # write_training(output_file, trainedList)
    read_testVal(testValueFile, testVal)
    test_values(testDigitFile, testVal, trainedList, numbers_classified)
    determine_accuracy(testVal, numbers_classified)
    return

def read_trainingVal(input_file, trainVal):
    with open(input_file) as f:
        for line in f:
            trainVal.append(line[0])

def read_testVal(input_file, testVal):
    with open(input_file) as f:
        for line in f:
            testVal.append(line[0])

def train_network(input_file, trainVal, trainedList):
    trainValNumber = 0
    i = 0 #line in picture
    j = 0 #pixel in line
    with open(input_file) as f:
        curNumber = int(trainVal[trainValNumber])
        for line in f:
            if i >= 28:
                trainValNumber+=1
                if trainValNumber==len(trainVal):
                    print("Error: More Train Values than Train Digits")
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
    ### Normalize values ###
    normalize_number = len(trainVal)
    ### Convert to float ###
    normalize_number*=1.0
    for x in range(10):
        for color in range(2):
            for j in range(28):
                for i in range(28):
                    trainedList[x][color][j][i]/=normalize_number

def test_values(input_file, testVal, trainedList, numbers_classified):
    probability_list = [1,1,1,1,1,1,1,1,1,1]
    i = 0
    # debuggingCounter = 0
    with open(input_file) as f:
        for line in f:
            if i >= 28:
                numbers_classified.append(classify_number(probability_list))
                # debuggingCounter+=1
                # if debuggingCounter == 15:
                #     print(numbers_classified)
                #     return
                i = 0
                probability_list = [1,1,1,1,1,1,1,1,1,1]

            for curNumber in range(10):
                j = 0
                for letter in line:
                    if letter == '\n':
                        continue
                    elif letter == '+':
                        probability_list[curNumber]*=(1+trainedList[curNumber][1][i][j])
                    elif letter == '#':
                        probability_list[curNumber]*=(1+trainedList[curNumber][0][i][j])
                    j+=1
            i+=1

def classify_number(probability_list):
    max = 0
    maxNumber = 0
    for number in range(10):
        if probability_list[number] > max:
            maxNumber = number
            max = probability_list[number]
    return maxNumber

def determine_accuracy(testVal, numbers_classified):
    total_numbers = len(numbers_classified)
    correct_number = 0
    for x in range(total_numbers):
        print(numbers_classified[x],testVal[x])
        if numbers_classified[x] == int(testVal[x]):
            correct_number+=1
    print(total_numbers)
    print(correct_number * 1.0 / total_numbers)

def write_training(output_file, data):
    with open(output_file, 'w') as outfile:
        outfile.write("Training data\n")
        for x in range(10):
            outfile.write("\n")
            outfile.write(str(x) + ":\n")
            outfile.write("Black:\n")
            for j in range(28):
                for i in range(28):
                    outfile.write(str(data[x][0][j][i]) + " ")
                outfile.write("\n")
            outfile.write("Gray\n")
            for j in range(28):
                for i in range(28):
                    outfile.write(str(data[x][1][j][i]) + " ")
                outfile.write("\n")




if __name__ == "__main__":
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
