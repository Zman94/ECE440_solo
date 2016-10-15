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
    if len(sys.argv)!=3:
        print("Not enough players for match. Please call function as stated in file.")
        return

    w = 8 # Standard board size
    h = 8
    players = list()
    players.append(sys.argv[1])
    players.append(sys.argv[2])

    board = [[0 for y in range(h)] for x in range(w)]
    for y in range(8):
        for x in range(8):
            if y < 2:
                board[y][x]="B"
            elif y < 6:
                board[y][x]="."
            else:
                board[y][x]="W"

    print_board(board)

    ##### Playing the Game ######
    game_loop(board, players)

    return

def print_board(board):
    for row in board:
        for val in row:
            print '{:1}'.format(val),
        print

def game_loop(board, players):
    heuristic1 = define_heuristic(players[0])
    heuristic2 = define_heuristic(players[1])

    winner1, winner2 = False, False
    while winner1 == False and winner2 == False:
        winner1 = player_move(board, heuristic1, True)
        print
        print "White Move"
        print_board(board)
        winner2 = player_move(board, heuristic2, False)
        print
        print "Black Move"
        print_board(board)

def define_heuristic(strategy):
    ### Define the heuristic for each strategy
    heuristic = list()
    if strategy[1] == "a":  # Aggressive
        heuristic.append(4) # Your pieces
        heuristic.append(6) # Opponent's pieces
        heuristic.append(3) # Position
        heuristic.append(-2)# Opponent's position
        heuristic.append(3) # Center
        return
    elif strategy[1] == "d":# Defensive
        heuristic.append(6) # Your pieces
        heuristic.append(4) # Opponent's pieces
        heuristic.append(2) # Position
        heuristic.append(-3)# Opponent's position
        heuristic.append(3) # Center
        return
    else:
        print "Make sure that player strategies are correct then rerun."
        sys.exit()
    return heuristic

def player_move(board, strategy, player):

    ### Check for a winner ###
    for x in range(8):
        if board[0][x]=="W" and player==True:
            return True
        if board[7][x]=="B" and player==False:
            return True

    return False

if __name__ == "__main__":
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
