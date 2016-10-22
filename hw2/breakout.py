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
    while True:
        winner1 = player_move(board, heuristic1, True)
        print
        print "White Move"
        print
        print_board(board)
        if winner1:
            break
        winner2 = player_move(board, heuristic2, False)
        print
        print "Black Move"
        print_board(board)
        if winner2:
            break

def define_heuristic(strategy):
    ### Define the heuristic for each strategy
    heuristic = list()
    if strategy[1] == "a":  # Aggressive
        heuristic.append(4) # Your pieces
        heuristic.append(-6) # Opponent's pieces
        heuristic.append(3) # Position
        heuristic.append(-2)# Opponent's position
        heuristic.append(3) # Center
    elif strategy[1] == "d":# Defensive
        heuristic.append(6) # Your pieces
        heuristic.append(-4) # Opponent's pieces
        heuristic.append(2) # Position
        heuristic.append(-3)# Opponent's position
        heuristic.append(3) # Center
    else:
        print "Make sure that player strategies are correct then rerun."
        sys.exit()
    return heuristic

def calculate_score(board, heuristic, player):
    points = 0

    for x in range(8):
        for y in range(8):
            if board[y][x]=="W" and player:
                points+=heuristic[0]
                points+=(7-y)*heuristic[2]
                if y > 2 and y < 5 and x > 2 and x < 5:
                    points+=heuristic[4]
            elif board[y][x]=="W" and not player:
                points+=heuristic[1]
                points+=(7-y)*heuristic[3]
            elif board[y][x]=="B" and player:
                points+=heuristic[1]
                points+=y*heuristic[3]
            elif board[y][x]=="B" and not player:
                points+=heuristic[0]
                points+=y*heuristic[2]
                if y > 2 and y < 5 and x > 2 and x < 5:
                    points+=heuristic[4]

    return points

def generate_movetree(board, strategy, player, layer, min_max):
    if layer > 2:
        return calculate_score(board, strategy, player)
    if min_max:
        maxVal=-50
    else:
        maxVal=50
    # Find each move for first layer of minimax
    for x in range(8):
        for y in range(8):
            if player:
                if board[y][x]=="W":
                    if y-1 >= 0 and x-1 >= 0 and (board[y-1][x-1]=="." or board[y-1][x-1]=="B"):
                        boardCopy=deepcopy(board)
                        boardCopy[y-1][x-1]="W"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree(boardCopy, strategy, not player, layer+1, not min_max)
                        if min_max:
                            if tempMax > maxVal:
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                                maxVal = tempMax
                        else:
                            if tempMax < maxVal:
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                                maxVal = tempMax

                    if y-1 >= 0 and (board[y-1][x]=="." or board[y-1][x]=="B"):
                        boardCopy=deepcopy(board)
                        boardCopy[y-1][x]="W"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree(boardCopy, strategy, not player, layer+1, not min_max)
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

                    if y-1 >= 0 and x+1 <= 7 and (board[y-1][x+1]=="." or board[y-1][x+1]=="B"):
                        boardCopy=deepcopy(board)
                        boardCopy[y-1][x+1]="W"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree(boardCopy, strategy, not player, layer+1, not min_max)
                        if maxVal is None:
                            maxVal=tempMax
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

            else:
                if board[y][x]=="B":
                    if y+1 <= 7 and x-1 >= 0 and (board[y+1][x-1]=="." or board[y+1][x-1]=="W"):
                        boardCopy=deepcopy(board)
                        boardCopy[y+1][x-1]="B"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree(boardCopy, strategy, not player, layer+1, not min_max)
                        if maxVal is None:
                            maxVal=tempMax
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

                    if y+1 <= 7 and (board[y+1][x]=="." or board[y+1][x]=="W"):
                        boardCopy=deepcopy(board)
                        boardCopy[y+1][x]="B"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree(boardCopy, strategy, not player, layer+1, not min_max)
                        if maxVal is None:
                            maxVal=tempMax
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

                    if y+1 <= 7 and x+1 <= 7 and (board[y+1][x+1]=="." or board[y+1][x+1]=="W"):
                        boardCopy=deepcopy(board)
                        boardCopy[y+1][x+1]="B"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree(boardCopy, strategy, not player, layer+1, not min_max)
                        if maxVal is None:
                            maxVal=tempMax
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

    if layer==0:
        for x in range(8):
            for y in range(8):
                board[y][x]=boardFinal[y][x]

    return maxVal

def player_move(board, heuristic, player):

    moveTree = {}
    ### Check minimax trees ###
    generate_movetree(board, heuristic, player, 0, True)

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
