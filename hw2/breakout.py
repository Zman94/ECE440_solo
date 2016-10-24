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

    nodes_expanded = list()
    nodes_expanded.append(0)
    nodes_expanded.append(0)

    white_moves = 0
    black_moves = 0

    whitePieces = 0
    blackPieces = 0

    winner1, winner2 = False, False
    while True:
        winner1 = player_move(board, heuristic1, True, players[0], nodes_expanded)
        white_moves+=1
        print
        print "White's move"
        print
        print_board(board)
        if winner1:
            for x in range(8):
                for y in range(8):
                    if board[y][x]=="B":
                        blackPieces+=1
                    elif board[y][x]=="W":
                        whitePieces+=1
            print "White Wins!"
            print_board(board)
            print "White took", white_moves, "turns and black took", black_moves, "turns."
            print "White captured", 16-blackPieces, "pieces and black captured", 16-whitePieces, "pieces."
            print "White expanded", nodes_expanded[0], "nodes and black expanded", nodes_expanded[1], "nodes."
            print "There were", nodes_expanded[0]+nodes_expanded[1], "nodes expanded total this game."
            print
            print "The average nodes expanded per turn was", nodes_expanded[0]/(black_moves+white_moves+0.0)
            print "The average time per move was", (time.time() - start_time)/(white_moves+black_moves), "s."
            break
        winner2 = player_move(board, heuristic2, False, players[1], nodes_expanded)
        black_moves+=1
        print
        print "Black's move"
        print
        print_board(board)
        if winner2:
            for x in range(8):
                for y in range(8):
                    if board[y][x]=="B":
                        blackPieces+=1
                    elif board[y][x]=="W":
                        whitePieces+=1
            print "Black Wins!"
            print_board(board)
            print "White took", white_moves, "turns and black took", black_moves, "turns."
            print "White captured", 16-blackPieces, "pieces and black captured", 16-whitePieces, "pieces."
            print "White expanded", nodes_expanded[0], "nodes and black expanded", nodes_expanded[1], "nodes."
            print "There were", nodes_expanded[0]+nodes_expanded[1], "nodes expanded total this game."
            print
            print "The average nodes expanded per turn was", nodes_expanded[0]/(black_moves+white_moves+0.0)
            print "The average time per move was", (time.time() - start_time)/(white_moves+black_moves), "s."
            break

def define_heuristic(strategy):
    ### Define the heuristic for each strategy
    heuristic = list()
    if strategy[1] == "a":  # Aggressive
        heuristic.append(20) # Your pieces
        heuristic.append(-40)# Opponent's pieces
        heuristic.append(30) # Position
        heuristic.append(10) # Opponent's position
        heuristic.append(15) # Center
    elif strategy[1] == "d":# Defensive
        heuristic.append(40) # Your pieces
        heuristic.append(-20)# Opponent's pieces
        heuristic.append(10) # Position
        heuristic.append(30) # Opponent's position
        heuristic.append(15) # Center
    else:
        print "Make sure that player strategies are correct then rerun."
        sys.exit()
    return heuristic

def calculate_score(board, heuristic, player):
    points = 0

    # print
    # print "Calculate score of:"
    # print_board(board)

    for x in range(8):
        for y in range(8):
            if board[y][x]=="W" and player:
                points+=heuristic[0]
                points+=heuristic[2]*(8-y)
                if y > 2 and y < 5 and x > 2 and x < 5:
                    points+=heuristic[4]
            elif board[y][x]=="W" and not player:
                points+=heuristic[1]
                points-=heuristic[3]*(8-y)
            elif board[y][x]=="B" and player:
                points+=heuristic[1]
                points-=heuristic[3]*(y+1)
            elif board[y][x]=="B" and not player:
                points+=heuristic[0]
                points+=heuristic[2]*(y+1)
                if y > 2 and y < 5 and x > 2 and x < 5:
                    points+=heuristic[4]

    # print points
    # print

    return points

def generate_movetree_mm(board, strategy, player, layer, min_max, nodes_expanded):
    if layer >= 3: # if this is odd, must return negative value below and 'if player
        if player:
            nodes_expanded[1]+=1
        else:
            nodes_expanded[0]+=1
        return -calculate_score(board, strategy, player)
    if min_max:
        maxVal=-5000
    else:
        maxVal=5000
    # Find each move for first layer of minimax
    for x in range(8):
        for y in range(8):
            if player:
                if board[y][x]=="W":
                    if y-1 >= 0 and x-1 >= 0 and (board[y-1][x-1]=="." or board[y-1][x-1]=="B"):
                        boardCopy=deepcopy(board)
                        boardCopy[y-1][x-1]="W"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_mm(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded)
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

                    if y-1 >= 0 and board[y-1][x]==".":
                        boardCopy=deepcopy(board)
                        boardCopy[y-1][x]="W"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_mm(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded)
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
                        tempMax = generate_movetree_mm(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded)
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
                        tempMax = generate_movetree_mm(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded)
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

                    if y+1 <= 7 and board[y+1][x]==".":
                        boardCopy=deepcopy(board)
                        boardCopy[y+1][x]="B"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_mm(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded)
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
                        tempMax = generate_movetree_mm(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded)
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

def generate_movetree_ab(board, strategy, player, layer, min_max, nodes_expanded, ab_prune=list()):
    if layer >= 4: # if this is odd, must return negative value below and 'if player'
        if not player:
            nodes_expanded[1]+=1
        else:
            nodes_expanded[0]+=1
        l=calculate_score(board, strategy, player)
        return l
    if min_max:
        maxVal=-7000
        ab_prune.insert(layer,maxVal)
        tempMax=maxVal
    else:
        maxVal=7000
        ab_prune.insert(layer,maxVal)
        tempMax=maxVal
    # Find each move for first layer of minimax
    # If statement speeds up
    for x in range(8):
        if not player:
            y = 7
        else:
            y = 0
        while (y < 8 and player) or (y >=0 and not player):
            if player:
                if board[y][x]=="W":
                    if y-1 >= 0 and x-1 >= 0 and (board[y-1][x-1]=="." or board[y-1][x-1]=="B"):
                        boardCopy=deepcopy(board)
                        boardCopy[y-1][x-1]="W"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_ab(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded, ab_prune)
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax > ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax < ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

                    if y-1 >= 0 and board[y-1][x]==".":
                        boardCopy=deepcopy(board)
                        boardCopy[y-1][x]="W"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_ab(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded, ab_prune)
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax > ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax < ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

                    if y-1 >= 0 and x+1 <= 7 and (board[y-1][x+1]=="." or board[y-1][x+1]=="B"):
                        boardCopy=deepcopy(board)
                        boardCopy[y-1][x+1]="W"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_ab(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded, ab_prune)
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax > ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax < ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

            else:
                if board[y][x]=="B":
                    if y+1 <= 7 and x-1 >= 0 and (board[y+1][x-1]=="." or board[y+1][x-1]=="W"):
                        boardCopy=deepcopy(board)
                        boardCopy[y+1][x-1]="B"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_ab(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded, ab_prune)
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax > ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax < ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

                    if y+1 <= 7 and board[y+1][x]==".":
                        boardCopy=deepcopy(board)
                        boardCopy[y+1][x]="B"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_ab(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded, ab_prune)
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax > ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax < ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)

                    if y+1 <= 7 and x+1 <= 7 and (board[y+1][x+1]=="." or board[y+1][x+1]=="W"):
                        boardCopy=deepcopy(board)
                        boardCopy[y+1][x+1]="B"
                        boardCopy[y][x]="."
                        tempMax = generate_movetree_ab(boardCopy, strategy, not player, layer+1, not min_max, nodes_expanded, ab_prune)
                        if min_max:
                            if tempMax > maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax > ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
                        else:
                            if tempMax < maxVal:
                                maxVal = tempMax
                                if layer!=0 and tempMax < ab_prune[layer-1]:
                                    return maxVal
                                if layer==0:
                                    boardFinal = deepcopy(boardCopy)
            if player:
                y+=1
            else:
                y-=1

    if layer==0 and (tempMax!=7000 or tempMax!=-7000):
        for x in range(8):
            for y in range(8):
                board[y][x]=boardFinal[y][x]

    ab_prune[layer-1]=tempMax
    return maxVal

def player_move(board, heuristic, player, strategy, nodes_expanded):

    moveTree = {}
    ### Check minimax trees ###
    if strategy[0]=="m":
        generate_movetree_mm(board, heuristic, player, 0, True, nodes_expanded)
    else:
        generate_movetree_ab(board, heuristic, player, 0, True, nodes_expanded)

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
