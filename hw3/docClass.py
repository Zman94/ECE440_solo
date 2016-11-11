from __future__ import print_function
from copy import deepcopy
from collections import defaultdict
import operator
import sys
import time
import math
import pdb

start_time = time.time()

def main():
    if len(sys.argv)!=3:
        print("Wrong number of arguments. For the first argument, enter 'b' for bernouli or 'm' for multinomial. For the second argument, enter 'm' for movie reviews or 'c' for conversations.")
        return
    ### Files to train from and save training data ###
    if sys.argv[2] == "m":
        trainingFile = "./movie_review/rt-train.txt"
        testFile = "./movie_review/rt-test.txt"
    elif sys.argv[2] == "c":
        trainingFile = "./fisher_2topic/fisher_train_2topic.txt"
        testFile = "./fisher_2topic/fisher_test_2topic.txt"
    else:
        print("For the second argument, enter 'm' for movie reviews or 'c' for conversations.")
        return
    ### File to write training data to if you want to save it ###
    output_file = "./trainingDocClass.txt"
    ### LaPlace smoothing value ###
    LP = 0.1
    ### Word list (needs to be converted into a dictionary) ###
    trainVal = list()
    ### 1 or -1 depending on review ###
    docVals = list()
    ### Dictionary of words and their frequency ###
    trainDicts = list()
    ### Trained value list to test based on ###
    trained_network = list()
    ### Holds the probablility of class1 / class2 ###
    oddsRatio = dict()
    ### Holds the probability of each class ###
    classRatio = 0.0

    read_data(trainingFile, trainVal)
    for x in trainVal:
        docVals.append(int(x[0]))
        del x[0]
    create_dict(trainVal, trainDicts)
    if sys.argv[1] == "b":
        classRatio = train_network_b(docVals, trainDicts, trained_network, LP, classRatio)
    elif sys.argv[1] == "m":
        classRatio = train_network_m(docVals, trainDicts, trained_network, LP, classRatio)
    else:
        print("For the first argument, enter 'b' for bernouli or 'm' for multinomial.")
        return
    # write_training(output_file, trained_network)
    generate_odds(oddsRatio, trained_network)
    ### Get dictionary of values to test on ###
    ### Can reuse variables because our trained_network holds all our data ###
    trainVal = list()
    trainDicts = list()
    docVals = list()
    ### List to hold values generated by system ###
    generated_content = list()
    read_data(testFile, trainVal)
    for x in trainVal:
        docVals.append(int(x[0]))
        del x[0]
    create_dict(trainVal, trainDicts)
    test_values(trainDicts, generated_content, trained_network, oddsRatio, classRatio)
    determine_accuracy(generated_content, docVals)
    print_odds_ratios(trained_network)
    return

def read_data(input_file, trainVal):
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

def train_network_m(docVals, trainDicts, trained_network, LP, classRatio):
    total = [0, 0]

    ### Set default values = to LP smoothing value ###
    trained_network.append(defaultdict(lambda: LP)) #index 0 is negative reviews
    trained_network.append(defaultdict(lambda: LP)) #index 1 is positive reviews
    for x in range(len(docVals)):
        if docVals[x] < 0:
            for key, value in trainDicts[x].iteritems():
                total[0]+=value
                trained_network[0][key]+=value
        else:
            for key, value in trainDicts[x].iteritems():
                total[1]+=value
                trained_network[1][key]+=value

    for i in range(2):
        for y in trained_network[i].iterkeys():
            trained_network[i][y]/=(1.0*(total[1]+total[0]+LP*(total[0]+total[1])))
    ### set the default value = to ()1/number of choices per feature)/# of features ###
    trained_network[0] = defaultdict(lambda: .5/(total[0]), trained_network[0])
    trained_network[1] = defaultdict(lambda: .5/(total[1]), trained_network[1])

    classRatio = 1.0*total[0]/total[1]
    return classRatio

def train_network_b(docVals, trainDicts, trained_network, LP, classRatio):
    total = [0, 0]

    ### Set default values = to LP smoothing value ###
    trained_network.append(defaultdict(lambda: LP)) #index 0 is negative reviews
    trained_network.append(defaultdict(lambda: LP)) #index 1 is positive reviews
    for x in range(len(docVals)):
        if docVals[x] < 0:
            total[0]+=1
            for y in trainDicts[x].keys():
                trained_network[0][y]+=1
        else:
            total[1]+=1
            for y in trainDicts[x]:
                trained_network[1][y]+=1

    for i in range(2):
        for y in trained_network[i].iterkeys():
            trained_network[i][y]/=(1.0*(total[0]+total[1]+LP*2))

    ### set the default value = to ()1/number of choices per feature)/# of features ###
    trained_network[0] = defaultdict(lambda: .5/(total[0]), trained_network[0])
    trained_network[1] = defaultdict(lambda: .5/(total[1]), trained_network[1])

    classRatio = 1.0*total[0]/total[1]
    return classRatio

def generate_odds(oddsRatio, trained_network):
    for x in trained_network[0].keys():
        oddsRatio[x] = trained_network[0][x]/trained_network[1][x]
    ### It's ok to overwrite. Value will be the same ###
    for x in trained_network[1].keys():
        oddsRatio[x] = trained_network[0][x]/trained_network[1][x]

def write_training(output_file, data):
    with open(output_file, 'w') as outfile:
        outfile.write("Training data\n")
        for i in range(2):
            for x in data[i].keys():
                outfile.write(str(x))
            for x in data[i].values():
                outfile.write(str(x))
            outfile.write("\n")

def test_values(trainDicts, generated_content, trained_network, oddsRatio, classRatio):
    probabilities = [0,0] #0 is negative, 1 is positive
    # for x in trainDicts:
    #     print(x)
    # return
    for x in trainDicts:
        # for y in x.keys():
        #     print(y)
        #     print(trained_network[0][y])
        #     print(trained_network[1][y])
        # return
        for i in range(2):
            for y in trained_network[i].keys():
                if y in x.keys():
                    probabilities[i]+=math.log(trained_network[i][y])
                else:
                    probabilities[i]+=math.log(1-trained_network[i][y])
        ### Classify Document ###
        for y in x.keys():
            if y in oddsRatio:
                probabilities[0]+=(5*math.log(oddsRatio[y]))
                probabilities[1]-=(5*math.log(oddsRatio[y]))
        ### Add probability of class y ###
        probabilities[0]+=math.log(classRatio)
        probabilities[1]+=math.log(1/classRatio)
        # print(probabilities)
        if probabilities[0] > probabilities[1]:
            generated_content.append(-1)
        else:
            generated_content.append(1)
        probabilities = [0,0]

def determine_accuracy(generated_content, docVals):
    correct = 0
    confusionMatrix = [[0 for i in range(2)] for j in range(2)]
    total = len(generated_content)
    for i in range(total):
        if generated_content[i] == docVals[i]:
            correct+=1
        else:
            if docVals[i] == -1:
                confusionMatrix[0][1]+=1
            else:
                confusionMatrix[1][0]+=1
    for i in range(2):
        for j in range(2):
            confusionMatrix[i][j]/=(1.0*total)
    for i in range(2):
        for j in range(2):
            confusionMatrix[i][j]*=1000
            confusionMatrix[i][j]=int(confusionMatrix[i][j])
            confusionMatrix[i][j]/=(10.0)
    correct/=(1.0*total)
    correct=int(correct*1000)
    correct/=(10.0)
    if sys.argv[2] == "c":
        print(str(correct)+"% of the conversations were correctly classified.\n")
    else:
        print(str(correct)+"% of the movie reviews were correctly classified.\n")
    print("The confusion matrix for row true class and column classified as:")
    for i in range(2):
        for j in range(2):
            if j == 0:
                print("["+str(confusionMatrix[i][j]), end="%, ")
            else:
                print(confusionMatrix[i][j],end="%]\n")

def print_odds_ratios(trained_network):
    most_likely_keys_0 = sorted(trained_network[0].items(), key=operator.itemgetter(1), reverse=True)
    most_likely_keys_1 = sorted(trained_network[1].items(), key=operator.itemgetter(1), reverse=True)

    top_ten_0 = most_likely_keys_0[:10]
    top_ten_1 = most_likely_keys_1[:10]

    for x in range(len(top_ten_0)):
        top_ten_0[x]=(top_ten_0[x][0],int(top_ten_0[x][1]*10000))
        top_ten_0[x]=(top_ten_0[x][0],top_ten_0[x][1]/100.0)
    for x in range(len(top_ten_1)):
        top_ten_1[x]=(top_ten_1[x][0],int(top_ten_1[x][1]*10000))
        top_ten_1[x]=(top_ten_1[x][0],top_ten_1[x][1]/100.0)

    print()
    print("The top ten words in the category classified as -1 are as follows with percent of documents they appear in:")
    for x in top_ten_0:
        print(x[0]+": "+str(x[1])+"%")
    print()
    print("The top ten words in the category classified as +1 are as follows with percent of documents they appear in:")
    for x in top_ten_1:
        print(x[0]+": "+str(x[1])+"%")

    print()
    print("The words with the highest odds ratio are as follows:")
    oddsRatio = [(1, "ipsum") for x in range(10)]
    for key,value in trained_network[0].iteritems():
        odds_ratio_cur = value/trained_network[1][key]
        for x in range(10):
            if odds_ratio_cur > 1:
                if odds_ratio_cur > oddsRatio[x][0] and odds_ratio_cur > 1/oddsRatio[x][0]:
                    oddsRatio[x] = (odds_ratio_cur,key)
                    break
            elif odds_ratio_cur < 1:
                if odds_ratio_cur < oddsRatio[x][0] and odds_ratio_cur < 1/oddsRatio[x][0]:
                    oddsRatio[x] = (odds_ratio_cur,key)
                    break

    print("These words appeared in category -1 more often.")
    for x in oddsRatio:
        if x[0] > 1:
            print(x)

    print("These words appeared in category +1 more often.")
    for x in oddsRatio:
        if x[0] < 1:
            print(x)

    return

if __name__ == "__main__":
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
