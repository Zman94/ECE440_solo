from __future__ import print_function
from copy import deepcopy
import sys
import time
import math
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
    ### LaPlace smoothing value ###
    LP = .1
    ### Used to calculate the prior probability ###
    classCount = list()
    for x in range(10):
        classCount.append(0)
    ### List to display numbers generated from AI ###
    numbers_classified = list()
    trainVal = list()
    testVal = list()
    confusionMatrix = [[0 for i in range(10)] for j in range(10)]
    ### Initialize the training lists with one gray and one black pixel in each location ###
    ### Initialize to one for laplacian smoothing ###
    ### KEY : [Number][row][column] ###
    trainedList = {0: [[LP for i in range(M)] for j in range(M)],
                   1: [[LP for i in range(M)] for j in range(M)],
                   2: [[LP for i in range(M)] for j in range(M)],
                   3: [[LP for i in range(M)] for j in range(M)],
                   4: [[LP for i in range(M)] for j in range(M)],
                   5: [[LP for i in range(M)] for j in range(M)],
                   6: [[LP for i in range(M)] for j in range(M)],
                   7: [[LP for i in range(M)] for j in range(M)],
                   8: [[LP for i in range(M)] for j in range(M)],
                   9: [[LP for i in range(M)] for j in range(M)]}
    read_trainingVal(trainingValueFile, trainVal)
    train_network(trainingDigitFile, trainVal, trainedList, classCount, LP, M)
    # write_training(output_file, trainedList)
    read_testVal(testValueFile, testVal)
    test_values(testDigitFile, testVal, trainedList, numbers_classified, classCount, M)
    determine_accuracy(testVal, numbers_classified, confusionMatrix)
    print_odds_ratios(trainedList)
    return

def read_trainingVal(input_file, trainVal):
    with open(input_file) as f:
        for line in f:
            trainVal.append(line[0])

def read_testVal(input_file, testVal):
    with open(input_file) as f:
        for line in f:
            testVal.append(line[0])

def train_network(input_file, trainVal, trainedList, classCount, LP, M):
    trainValNumber = 0
    firstTime = True
    i = 0 # line in picture
    j = 0 # pixel in line
    with open(input_file) as f:
        curNumber = int(trainVal[trainValNumber])
        classCount[curNumber]+=1
        for line in f:
            # if firstTime == True:
            #     firstTime = False
            #     continue
            if i >= M:
                trainValNumber+=1
                if trainValNumber==len(trainVal):
                    print("Error: More Train Values than Train Digits")
                    sys.exit()
                curNumber = int(trainVal[trainValNumber])
                classCount[curNumber]+=1
                i = 0
            j = 0
            for letter in line:
                if letter == '\n':
                    continue
                ### If gray or black, add 1 point to colored ###
                elif letter == '+' or letter == '#':
                    trainedList[curNumber][i][j]+=1
                j+=1
            i+=1
    # for x in range(10):
    #     for j in range(10):
    #         print(trainedList[x][j])
    #     print()
    for x in range(10):
        for j in range(28):
            for i in range(28):
                trainedList[x][j][i]/=(classCount[x]*1.0+LP*2.0)
        # print(trainedList[x])
    ### Normalize classCount ###
    normalize_count_number = len(trainVal)
    normalize_count_number*=1.0
    for x in range(10):
        classCount[x]/=normalize_count_number
        classCount[x] = math.log(classCount[x])

def test_values(input_file, testVal, trainedList, numbers_classified, classCount, M):
    ### Start the probabilities at those of probability for a class ###
    probability_list = list()
    for x in range(10):
        # probability_list.append(1)
        probability_list.append(classCount[x])
    # probability_list[8]-=15
    i = 0
    # debuggingCounter = 0
    with open(input_file) as f:
        for line in f:
            if i >= M:
                probability_list[8]+=7
                probability_list[5]+=4
                numbers_classified.append(classify_number(probability_list))
                # debuggingCounter+=1
                # if debuggingCounter == 15:
                #     print(numbers_classified)
                #     return
                i = 0
                for x in range(10):
                    # probability_list[x]=1
                    probability_list[x]=classCount[x]
                # probability_list[8]-=15

            for curNumber in range(10):
                j = 0
                for letter in line:
                    if letter == '\n':
                        continue
                    elif letter == '+' or letter == '#':
                        probability_list[curNumber]+=math.log(trainedList[curNumber][i][j])
                    elif letter == ' ':
                        probability_list[curNumber]+=math.log(1-trainedList[curNumber][i][j])
                    j+=1
            i+=1
        probability_list[8]+=7
        probability_list[5]+=4
        numbers_classified.append(classify_number(probability_list))
        # debuggingCounter+=1
        # if debuggingCounter == 15:
        #     print(numbers_classified)
        #     return
        i = 0
        for x in range(10):
            # probability_list[x]=1
            probability_list[x]=classCount[x]
        # probability_list[8]-=15

def classify_number(probability_list):
    # print(probability_list)
    max = 0
    maxNumber = -1
    for number in range(10):
        if probability_list[number] > max or maxNumber < 0:
            maxNumber = number
            max = probability_list[number]
    return maxNumber

def determine_accuracy(testVal, numbers_classified, confusionMatrix):
    total_numbers = len(testVal)
    total_per_class = [0.0 for x in range(10)]
    correct_number = 0
    correct_per_class = [0 for x in range(10)]
    classCountTest = [0 for x in range(10)]
    for x in range(total_numbers):
        # print(numbers_classified[x],testVal[x])
        total_per_class[int(testVal[x])]+=1
        if numbers_classified[x] == int(testVal[x]):
            correct_number+=1
            correct_per_class[numbers_classified[x]]+=1

        else:
            int1 = numbers_classified[x]
            int2 = int(testVal[x])
            confusionMatrix[int2][int1]+=1
    ### Percentage of numbers from class row classified as class column ###
    for j in range(10):
        for i in range(10):
            confusionMatrix[j][i]/=total_per_class[j]
            confusionMatrix[j][i]*=1000
            confusionMatrix[j][i]=int(confusionMatrix[j][i])
            confusionMatrix[j][i]/=10.0
    for x in range(10):
        correct_per_class[x]/=total_per_class[x]
        correct_per_class[x]*=1000
        correct_per_class[x]=int(correct_per_class[x])
        correct_per_class[x]/=10.0
    print("Each number's accuracy from 0-9 is:")
    for x in range(10):
        if x == 0:
            print("["+str(correct_per_class[x]), end="%, ")
        elif x == 9:
            print(correct_per_class[x],end="%]\n")
        else:
            print(correct_per_class[x],end="%, ")
    print()
    print("The confusion matrix for row true class and column classified as:")
    for i in range(10):
        for j in range(10):
            if j == 0:
                print("["+str(confusionMatrix[i][j]),end="%, ")
            elif j == 9:
                print(confusionMatrix[i][j],end="%]")
            else:
                print(confusionMatrix[i][j],end="%, ")
        print()
    print("Out of " + str(total_numbers) + " total numbers, " + str(correct_number) + " numbers were correctly classified with an accuracy of ", str(correct_number * 1.0 / total_numbers))

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
