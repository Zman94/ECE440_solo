from __future__ import print_function
from copy import deepcopy
import sys
import time
import math
import random
import pdb

start_time = time.time()

# epochs = 100
epochs = 40
# epochs = 1
curEpoch = 0
alpha = 50

def main():
    if len(sys.argv)!=2:
        print("Give argument 'f' for face data and 'n' for number data.")
        return
    ### LaPlace smoothing value ###
    if sys.argv[1] == "n":
        ### Files to train from and save training data ###
        trainingDigitFile = "./digitdata/trainingimages"
        trainingValueFile = "./digitdata/traininglabels"
        ### Files to test against ###
        testDigitFile = "./digitdata/testimages"
        testValueFile = "./digitdata/testlabels"
        ### Size of picture in pixels ###
        M = 28
        W = 28
        ### Used to calculate the prior probability ###
        classCount = list()
        for x in range(10):
            classCount.append(0)
        ### Initialize the training lists with one gray and one black pixel in each location ###
        ### Initialize to one for laplacian smoothing ###
        ### KEY : [Number][row][column] ###
        # Includes bias and random
        # trainedList = {0: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                1: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                2: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                3: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                4: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                5: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                6: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                7: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                8: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)],
        #                9: [[5*(random.random()-.5) for i in range(M+1)] for j in range(W+1)]}
        # Includes bias
        trainedList = {0: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       1: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       2: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       3: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       4: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       5: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       6: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       7: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       8: [[float(0) for i in range(M+1)] for j in range(W+1)],
                       9: [[float(0) for i in range(M+1)] for j in range(W+1)]}
        # # Exclude bias
        # trainedList = {0: [[float(0) for i in range(M)] for j in range(W)],
        #                1: [[float(0) for i in range(M)] for j in range(W)],
        #                2: [[float(0) for i in range(M)] for j in range(W)],
        #                3: [[float(0) for i in range(M)] for j in range(W)],
        #                4: [[float(0) for i in range(M)] for j in range(W)],
        #                5: [[float(0) for i in range(M)] for j in range(W)],
        #                6: [[float(0) for i in range(M)] for j in range(W)],
        #                7: [[float(0) for i in range(M)] for j in range(W)],
        #                8: [[float(0) for i in range(M)] for j in range(W)],
        #                9: [[float(0) for i in range(M)] for j in range(W)]}
        # Exclude bias and random
        # trainedList = {0: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                1: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                2: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                3: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                4: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                5: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                6: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                7: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                8: [[2*(random.random()-.5) for i in range(M)] for j in range(W)],
        #                9: [[2*(random.random()-.5) for i in range(M)] for j in range(W)]}
    elif sys.argv[1] == "f":
        ### Files to train from and save training data ###
        trainingDigitFile = "./facedata/facedatatrain"
        trainingValueFile = "./facedata/facedatatrainlabels"
        ### Files to test against ###
        testDigitFile = "./facedata/facedatatest"
        testValueFile = "./facedata/facedatatestlabels"
        ### Size of picture in pixels ###
        M = 60
        W = 70
        ### Initialize the training lists with one gray and one black pixel in each location ###
        ### Initialize to one for laplacian smoothing ###
        ### KEY : [Number][row][column] ###
        classCount = list()
        for x in range(2):
            classCount.append(0)
    else:
        print("Give either argument 'f' for face data or 'n' for number data.")

    ### List to display numbers generated from AI ###
    numbers_classified = list()
    trainVal = list()
    testVal = list()
    confusionMatrix = [[0 for i in range(10)] for j in range(10)]

    read_trainingVal(trainingValueFile, trainVal)
    if sys.argv[1] == 'n':
        train_network(trainingDigitFile, trainVal, trainedList, classCount, M)
    else:
        train_network_face(trainingDigitFile, trainVal, trainedList, M, W)
        read_testVal(testValueFile, testVal)
        test_values_face(testDigitFile, testVal, trainedList, numbers_classified, classCount, M, W)
        determine_accuracy_face(testVal, numbers_classified)
        return
    # write_training(output_file, trainedList)
    read_testVal(testValueFile, testVal)
    test_values(testDigitFile, trainedList, numbers_classified, classCount, M)
    determine_accuracy(testVal, numbers_classified, confusionMatrix)
    # print_odds_ratios(trainedList)
    return

def read_trainingVal(input_file, trainVal):
    with open(input_file) as f:
        for line in f:
            trainVal.append(line[0])

def read_testVal(input_file, testVal):
    with open(input_file) as f:
        for line in f:
            testVal.append(line[0])

def train_network(input_file, trainVal, trainedList, classCount, M):
    global curEpoch
    curEpoch = 0
    curNumberImage = [[1 for x in range(M+1)] for y in range(M+1)]
    p = 0
    for curEpoch in range(0,epochs):
        print(curEpoch)
        correctNum = 0
        trainValNumber = 0
        i = 0 # line in picture
        j = 0 # pixel in line
        with open(input_file) as f:
            # Starts at 1 for Bias
            tempWeights = [1 for x in range(10)]
            curNumber = int(trainVal[trainValNumber])
            # classCount[curNumber]+=1
            for line in f:

                if i >= M:
                    trainValNumber+=1
                    if trainValNumber==len(trainVal):
                        print("Error: More Train Values than Train Digits")
                        sys.exit()
                    classified = classifyAs(tempWeights)
                    if classified != curNumber:
                        # if curEpoch != 0:
                        #     print(classified, curNumber)
                        # if classified == 0:
                        #     print(trainedList[0][10][10], end = " ")
                        updateClassWeight(curNumber, classified, trainedList, curNumberImage)
                        # if classified == 0:
                        #     print(trainedList[0][10][10])

                    else:
                        correctNum +=1
                    # print("Classified as", classified, "Real Val", curNumber)
                    tempWeights = [1 for x in range(10)]
                    curNumberImage = [[1 for x in range(M+1)] for y in range(M+1)]
                    curNumber = int(trainVal[trainValNumber])
                    classCount[curNumber]+=1
                    i = 0
                j = 0
                for letter in line:
                    if letter == '\n':
                        continue
                    ### If gray or black, add 1 point to colored ###
                    elif letter == '+' or letter == '#':
                        for x in range(10):
                            tempWeights[x] += trainedList[x][i][j]
                    else:
                        curNumberImage[i][j] = 0
                    j+=1
                i+=1
        print(correctNum/1.0/(len(trainVal)))

    # for x in range(10):
    #     for j in range(28):
    #         for i in range(28):
    #             trainedList[x][j][i]/=(classCount[x]*1.0+LP*2.0)
    #     # print(trainedList[x])
    # ### Normalize classCount ###
    # normalize_count_number = len(trainVal)
    # normalize_count_number*=1.0
    # for x in range(10):
        # classCount[x]/=normalize_count_number
        # classCount[x] = math.log(classCount[x])

def classifyAs(tempWeights):
    argMax = 0
    maxClass = -1
    for x in range(10):
        if tempWeights[x] > argMax or maxClass < 0:
            argMax = tempWeights[x]
            maxClass = x
    return maxClass

def updateClassWeight(real, wrong, trainedList, tempWeights):
    for y in range(len(trainedList[real])):
        for x in range(len(trainedList[real][y])):
            trainedList[real][y][x]+=(alpha/1.0/(alpha+curEpoch)*tempWeights[y][x])
            trainedList[wrong][y][x]-=(alpha/1.0/(alpha+curEpoch)*tempWeights[y][x])

def test_values(input_file, trainedList, numbers_classified, classCount, M):
    probability_list = list()
    for x in range(10):
        probability_list.append(0)
    i = 0
    curNumberlist = 0
    with open(input_file) as f:
        for line in f:
            if i >= M:
                numbers_classified.append(classifyAs(probability_list))
                i = 0
                for x in range(10):
                    probability_list[x]=0
                    # probability_list[x]=classCount[x]
                curNumberlist+=1

            for curNumber in range(10):
                j = 0
                for letter in line:
                    if letter == '\n':
                        continue
                    elif letter == '+' or letter == '#':
                        probability_list[curNumber]+=trainedList[curNumber][i][j]
                        # curPic[i][j] = letter
                    j+=1
            i+=1
        numbers_classified.append(classifyAs(probability_list))

def determine_accuracy(testVal, numbers_classified, confusionMatrix):
    confusion_matrix = [[0 for x in range(10)] for y in range(10)]
    total_of_each_number = [0 for x in range(10)]
    total_numbers = len(testVal)
    correct_number = 0
    for x in range(total_numbers):
        if numbers_classified[x] == int(testVal[x]):
            correct_number+=1
        total_of_each_number[int(testVal[x])]+=1
        confusion_matrix[int(testVal[x])][numbers_classified[x]]+=1

    print("Out of " + str(total_numbers) + " total numbers, " + str(correct_number) + " numbers were correctly classified with an accuracy of ", str(correct_number * 1.0 / total_numbers))

    for y in range(10):
        for x in range(10):
            confusion_matrix[y][x]/=(total_of_each_number[x]/1.0)
            confusion_matrix[y][x]=int(confusion_matrix[y][x]*1000)
            confusion_matrix[y][x]=confusion_matrix[y][x]/10.0

    print("Confusion matrix for row true class and column classified as:")
    for y in range(10):
        for x in range(10):
            if x == 0:
                print("[" + str(confusion_matrix[y][x]) + "%", end=", ")
            elif x == 9:
                print(confusion_matrix[y][x], end="%]\n")
            else:
                print(confusion_matrix[y][x], end="%,")

def write_training(output_file, data):
    with open(output_file, 'w') as outfile:
        outfile.write("Training data\n")
        for x in range(10):
            outfile.write("\n")
            outfile.write(str(x) + ":\n")
            for j in range(28):
                for i in range(28):
                    outfile.write(str(data[x][j][i]) + " ")
                outfile.write("\n")

def print_odds_ratios(trainedList):
    ### Add value pairs to compare here ###
    list1 = [5,8,4,7]
    list2 = [3,3,9,9]

    print("\nKey:\nFor log likelihood maps:\n#: log<-6\n%: -6<log<-3\nX: -3<log<-1\n/: -1<log\n")
    print("For log odds ratio:\n#: logs of 1 and 2 are approx. equal\n+: Graph 1 is more likely\n-: Graph 2 is more likely")
    for x in range(4):
        ### Log Likelihood for list1 number ###
        for i in range(28):
            for j in range(28):
                determineColor = math.log(trainedList[list1[x]][i][j])
                # print(determineColor)
                # continue
                if determineColor < -6:
                    print("#", end="")
                elif determineColor < -3:
                    print("%", end="")
                elif determineColor < -1:
                    print("X", end="")
                else:
                    print("/", end="")
            print(" ", end="")
            for j in range(28):
                determineColor = math.log(trainedList[list2[x]][i][j])
                # print(determineColor)
                # continue
                if determineColor < -6:
                    print("#", end="")
                elif determineColor < -3:
                    print("%", end="")
                elif determineColor < -1:
                    print("X", end="")
                else:
                    print("/", end="")
            print(" ", end="")
            for j in range(28):
                determineColor = math.log(trainedList[list1[x]][i][j])/math.log(trainedList[list2[x]][i][j])
                if determineColor < 1.4 and determineColor > .6:
                    print("#", end="")
                elif determineColor > 1.4:
                    print("-", end="")
                elif determineColor < .6:
                    print("+", end="")
            print()
        print ()



if __name__ == "__main__":
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
