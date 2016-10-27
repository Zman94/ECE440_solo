'''
To run file, run "python breakout.py player1 player2" where players can be ma (minimax aggressive), md (minimax defensive), aa (alpha-beta aggressive), or ad (alpha-beta defensive).
The first argument goes first.
'''

import sys
from copy import deepcopy
import time
import pdb

start_time = time.time()

def main():
    trainVal = list()
    trainingValueFile = "./digitdata/testlabels"
    output_file = "./training.txt"
    read_trainingVal(trainingValueFile, trainVal)
    write_training(output_file, trainVal)
    return

def read_trainingVal(input_file, trainVal):
    with open(input_file) as f:
        for line in f:
            trainVal.append(line[0])

def write_training(output_file, data):
    with open(output_file, 'w') as outfile:
        outfile.write("Training data\n")
        for x in data:
            outfile.write(x+"\n")

if __name__ == "__main__":
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
