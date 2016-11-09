from __future__ import print_function
from copy import deepcopy
from collections import defaultdict
import sys
import time
import math
import pdb

start_time = time.time()

def main():
    if len(sys.argv)!=3:
        print("Not enough arguments.")
        return
    ### Files to train from and save training data ###
    trainingFile = "./movie_review/rt-train.txt"
    testFile = "./movie_review/rt-test.txt"
    # trainingFile = "./fisher_2topic/fisher_train_2topic.txt"
    # testFile = "./fisher_2topic/fisher_test_2topic.txt"
    ### LaPlace smoothing value ###
    LP = .1
    ### Word list (needs to be converted into a dictionary) ###
    trainVal = list()
    ### 1 or -1 depending on review ###
    docVals = list()
    ### Dictionary of words and their frequency ###
    trainDicts = list()
    ### Trained value list to test based on ###
    trained_network = list()
    
    read_trainingVal(trainingFile, trainVal)
    for x in trainVal:
        docVals.append(int(x[0]))
        del x[0]
    create_dict(trainVal, trainDicts)
    train_network_b(docVals, trainDicts, trained_network, LP) 
    # write_training(output_file, trainedList)
    # read_testVal(testValueFile, testVal)
    # test_values(testDigitFile, testVal, trainedList, numbers_classified, classCount, M)
    # determine_accuracy(testVal, numbers_classified, confusionMatrix)
    # print_odds_ratios(trainedList)
    return

def read_trainingVal(input_file, trainVal):
    with open(input_file) as f:
        for line in f:
            line = line.replace("\n", "")
            trainVal.append(line.split(" "))

def create_dict(trainVal, trainDicts):
    runs = 0
    for x in trainVal:
        tempDict = dict()
        for y in x:
            temp = y.split(":")
            tempDict[temp[0]] = int(temp[1])
        trainDicts.append(tempDict)

def train_network_b(docVals, trainDicts, trained_network, LP):
    positive = 0.0
    negative = 0.0
    count=-1


    trained_network.append(defaultdict(lambda: 0)) #index 0 is negative
    trained_network.append(defaultdict(lambda: 0)) #index 1 is positive
    for x in range(len(docVals)):
        if docVals[x] < 0:
            negative+=1
            for y in trainDicts[x].keys():
                trained_network[0][y]+=1
        else:
            positive+=1
            for y in trainDicts[x]:
                trained_network[1][y]+=1
        
    for x in trained_network:
        for y in x.values():
            y+=LP

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
    total_numbers = len(numbers_classified)
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
            print("[", end="")
        elif x == 9:
            print(correct_per_class[x],end="%]\n")
        else:
            print(correct_per_class[x],end="%, ")
    print()
    print("The confusion matrix for row true class and column classified as:")
    for i in range(10):
        for j in range(10):
            if j == 0:
                print("[", end="")
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
