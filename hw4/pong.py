from __future__ import print_function
import pygame, sys, time
import pdb
from pygame.locals import *
import random

start_time = time.time()

# Number of frames per second
FPS = 60

#Global Variables to be used through the program
width = 800
height = 600
paddle_width = width/40.0
paddle_height1 = 1*height
paddle_height2 = .2*height
PADDLEOFFSET = 20

# Set up the colours
black     = (0,0,0)
white     = (255,255,255)


#Q and R matrix constants
rows = 12
columns = 12
victory_reward = 1
failure_reward = -1
gamma = 5
alpha = 10.0
learning_times = [[[[[0 for v in range(3)] for w in range(2)] for x in range(columns)] for y in range(columns)] for z in range(rows)]
Nc = 3
# to stop the algorithm from processing the a negative on the first state after a failure
firstState = True

#File to store trained list
out_file = "./q_training.txt"

#Enable gui
graphics = True

#Draws the arena the game will be played in.
def drawArena():
    DISPLAYSURF.fill((255,255,255))
#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > height:
        paddle.bottom = height
    #Stops paddle moving too high
    elif paddle.top < 0:
        paddle.top = 0
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, black, paddle)

#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, black, ball)

#moves the ball returns new position
def moveBall(ball, velocity_x, velocity_y):
    ball.x += velocity_x
    ball.y += velocity_y
    return ball

#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, velocity_x, velocity_y):
    if ball.top <= 0 or ball.bottom >= height:
        velocity_y = velocity_y * -1
    if ball.left <= 0 or ball.right >= width:
        velocity_x = 0
    return velocity_x, velocity_y

#Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(ball, paddle1, paddle2, velocity_x, velocity_y):
    if velocity_x < 0 and paddle1.right >= ball.left and paddle1.top < ball.bottom and paddle1.bottom > ball.top:
        return -velocity_x, velocity_y
    # if velocity_x < 0 and paddle1.right >= ball.left and paddle1.top < ball.bottom and paddle1.bottom > ball.top:
    #     velocity_x*=-1
    #     speed_up=(random.randint(-150,150)/10000.0)
    #     velocity_x+=speed_up
    #     velocity_y+=(random.randint(-300,300)/10000.0)
    #     if velocity_x < .03:
    #         velocity_x = .03
    #     # if velocity_x > .1:
    #     #     velocity_x = .1
    #     # if velocity_y > .09:
    #     #     velocity_y = .09
    #     if velocity_y < -.06:
    #         velocity_y = -.06
    #     return velocity_x, velocity_y
    if velocity_x > 0 and paddle2.left <= ball.right and paddle2.top < ball.bottom and paddle2.bottom > ball.top:
        velocity_x*=-1
        speed_up=(random.randint(-150,150)/10000.0)
        velocity_x+=speed_up
        velocity_y+=(random.randint(-300,300)/10000.0)
        if velocity_x > -.03:
            velocity_x = -.03
        # if velocity_x < -.1:
        #     velocity_x = -.1
        # if velocity_y > .06:
        #     velocity_y = .06
        # if velocity_y < -.06:
        #     velocity_y = -.06
        return velocity_x, velocity_y
    else:
        return velocity_x, velocity_y

#Checks to see if a point has been scored returns new score
def checkPointScored(paddle2, ball, score, velocity_x):
    #reset points if left wall is hit
    if ball.right >= width:
        return -1
    #1 point for hitting the ball
    elif velocity_x > 0 and paddle2.left <= ball.right and paddle2.top < ball.bottom and paddle2.bottom > ball.top:
        score += 1
        return score
    #5 points for beating the other paddle
    # elif ball.right == width - length:
      #  score += 5
      #  return score
    #if no points scored, return score unchanged
    else: return score

#Artificial Intelligence of computer player
def hard_coded_paddle(ball, paddle1):
    #if ball moving towards bat, track its movement.
    if paddle1.centery < ball.centery:
        paddle1.y += .02*height
    else:
        paddle1.y -= .02*height
    return paddle1

#Q trained computer player
def q_paddle(q, cur_state, paddle2):
    # print(cur_state)
    curminus1 = cur_state[2]-1
    curplus1 = cur_state[2]+1

    if cur_state[2]-1 < 0:
        curminus1 = 0
    if cur_state[2]+1 >= rows:
        curplus1 = rows-1
    print("Q is")
    print(q[cur_state[0]][cur_state[1]][curminus1][cur_state[3]][cur_state[4]])
    print(q[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]])
    print(q[cur_state[0]][cur_state[1]][curplus1][cur_state[3]][cur_state[4]])

    if learning_times[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]] < Nc:
        max_state = 0
    elif learning_times[cur_state[0]][cur_state[1]][curplus1][cur_state[3]][cur_state[4]] < Nc:
        max_state = 1
    elif learning_times[cur_state[0]][cur_state[1]][curminus1][cur_state[3]][cur_state[4]] < Nc:
        max_state = -1
    else: #only enter the utility function if all explorations are satisfied
        if q[cur_state[0]][cur_state[1]][curminus1][cur_state[3]][cur_state[4]] > q[cur_state[0]][cur_state[1]][curplus1][cur_state[3]][cur_state[4]]:
            if q[cur_state[0]][cur_state[1]][curminus1][cur_state[3]][cur_state[4]] > q[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]]:
                max_state = -1
            else:
                max_state = 0
        else:
            if q[cur_state[0]][cur_state[1]][curplus1][cur_state[3]][cur_state[4]] > q[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]]:
                max_state = 1
            else:
                max_state = 0

    print("This is max state", max_state)
    paddle2.y += (max_state*height*.04)
    return paddle2

#Displays the current score on the screen
def displayScore(score):
    if graphics:
        resultSurf = BASICFONT.render('Score = %s' %(score), True, black)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (width - 150, 25)
        DISPLAYSURF.blit(resultSurf, resultRect)

#Resets game to initial state
def resetGame(game_state_tuple):
    game_state_tuple[0] = .5*width
    game_state_tuple[1] = .5*height
    game_state_tuple[2] = .03
    game_state_tuple[3] = .01
    game_state_tuple[4] = .5*height

#Determine cur_state
def determineState(paddle, ball, velocity_x, velocity_y):
    n = 0
    while (width/1.0/columns)*(n+1) < (ball.left+ball.right)/2.0:
        n+=1

    m = 0
    while (height/1.0/rows)*(m+1) < (ball.top+ball.bottom)/2.0:
        m+=1

    l = 0
    while (height/1.0/rows)*(l+1) < (paddle.top+paddle.bottom)/2.0:
        l+=1

    if velocity_x < 0:
        k = 0
    else:
        k = 1

    if velocity_y < .015:
        if velocity_y > -.015:
            j = 1
        else:
            j = 0
    else:
        j = 2

    if m >= rows:
        m = rows-1
    if m < 0:
        m = 0

    if l >= rows:
        l = rows-1
    if l < 0:
        l = 0

    if n >= columns:
        n = columns-1
    if n < 0:
        n = 0

    return (n,m,l,k,j)

#Evaluate Q matrix
def eval_q(q, r, prev_state, cur_state):
    if prev_state[2] >= rows-1:
        rowNumplus1 = rows-1
    else:
        rowNumplus1 = cur_state[2]+1
    if prev_state[2] <= 0:
        rowNumminus1 = 0
    else:
        rowNumminus1 = prev_state[2]-1
    max_next_state = max(q[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]],
                         q[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]],
                         q[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]])
    # max_next_state = max(q[prev_state[0]][prev_state[1]][rowNumplus1][prev_state[3]][prev_state[4]],
    #                      q[prev_state[0]][prev_state[1]][prev_state[2]][prev_state[3]][prev_state[4]],
    #                      q[prev_state[0]][prev_state[1]][rowNumminus1][prev_state[3]][prev_state[4]])


    ### This mess of a line determines the Q value for the last state as based on the lecture algorithm ###
    if not firstState and prev_state != cur_state:
        print(prev_state)
        print(cur_state)
        print((alpha/(learning_times[prev_state[0]][prev_state[1]][prev_state[2]][prev_state[3]][prev_state[4]]+alpha)))
        print(gamma*max_next_state)
        print()
        q[prev_state[0]][prev_state[1]][prev_state[2]][prev_state[3]][prev_state[4]] = q[prev_state[0]][prev_state[1]][prev_state[2]][prev_state[3]][prev_state[4]]+(alpha/(learning_times[prev_state[0]][prev_state[1]][prev_state[2]][prev_state[3]][prev_state[4]]+alpha))*(r[prev_state[0]][prev_state[1]][prev_state[2]][prev_state[3]][prev_state[4]]+gamma*max_next_state-q[prev_state[0]][prev_state[1]][prev_state[2]][prev_state[3]][prev_state[4]])

#Save the list in a file
def save_q_learning(q):
    with open(out_file, 'w') as outfile:
        outfile.write(str(columns)+"\n")
        outfile.write(str(rows)+"\n")
        outfile.write(str(rows)+"\n")
        outfile.write(str(2)+"\n")
        outfile.write(str(3)+"\n")

        for v in q:
            for w in v:
                for x in w:
                    for y in x:
                        for z in y:
                            outfile.write(str(z)+"\n")

#Load list from a file
def load_q_learning():
    with open(out_file, 'r') as outfile:
        list_entries = [0 for x in range(5)]
        for x in range(5):
            list_entries[x] = outfile.readline().strip()

        q = [[[[[0 for v in range(int(list_entries[4]))] for w in range(int(list_entries[3]))]for x in range(int(list_entries[2]))]for y in range(int(list_entries[1]))]for z in range(int(list_entries[0]))]

        for v in range(int(list_entries[0])):
            for w in range(int(list_entries[1])):
                for x in range(int(list_entries[2])):
                    for y in range(int(list_entries[3])):
                        for z in range(int(list_entries[4])):
                            q[v][w][x][y][z] = float(outfile.readline().strip())
    return q

#Main function
def main():
    global graphics
    global Nc, gamma, alpha
    global firstState
    if len(sys.argv)!=3:
        print("Give argument 'g' for a gui and any other letter for no gui.")
        print("Give second argument 't' for test and 'l' for learn.")
        print("Note that test still trains the network; values are tweaked to make training less prominant.")
        return

    if sys.argv[1] == 'g':
        graphics = True
    else:
        graphics = False

    if sys.argv[2] == 't':
        q = load_q_learning()
        Nc = 0
        gamma = 2.0
        maxGames = 5000
        alpha = 1.0
    elif sys.argv[2] == 'l':
        ### q matrix [column][row_ball][row_paddle][x_speed][y_speed]###
        q = [[[[[0 for v in range(3)] for w in range(2)] for x in range(columns)] for y in range(columns)] for z in range(rows)]
        maxGames = 500000
    else:
        print("Please give argument 't' for test or 'l' for learn.")
        return

    if graphics:
        pygame.init()
    global DISPLAYSURF
    ##Font information
    global BASICFONT, BASICFONTSIZE, learning_times
    ### [ball_x, ball_y, velocity_x, velocity_y, paddle_y] ###
    game_state_tuple = [.5*width, .5*height, .03, .01, .5*height]

    ### r matrix [column][row_ball][row_paddle][x_speed][y_speed]###
    r = [[[[[0 for v in range(3)] for w in range(2)] for x in range(columns)] for y in range(columns)] for z in range(rows)]
    ### state machines for prev and cur state [column][row_ball][row_paddle][x_speed][y_speed]###
    prev_state = (0,0,0,0,0)
    cur_state = (0,0,0,0,0)

    ### initialize reward matrix ###
    for x in range(rows):
        for y in range(rows):
            if y == x:
                r[columns-1][x][y][1][0] = 1
                r[columns-1][x][y][1][1] = 1
                r[columns-1][x][y][1][2] = 1
            else:
                r[columns-1][x][y][1][0] = -1
                r[columns-1][x][y][1][1] = -1
                r[columns-1][x][y][1][2] = -1

    if graphics:
        BASICFONTSIZE = 20
        BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Pong HW4')

    #Initiate variable and set starting positions
    #any future changes made within rectangles
    game_state_tuple[0] = width/2 - paddle_width/2
    game_state_tuple[1] = height/2 - paddle_width/2
    score = 0

    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET, 0, paddle_width, paddle_height1)
    paddle2 = pygame.Rect(width - PADDLEOFFSET - paddle_width, game_state_tuple[4]-paddle_height2/2, paddle_width, paddle_height2)
    ball = pygame.Rect(game_state_tuple[0], game_state_tuple[1], paddle_width, paddle_width)

    #Draws the starting position of the Arena
    if graphics:
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        pygame.mouse.set_visible(False) # make cursor invisible

    determineState(paddle2, ball, game_state_tuple[2], game_state_tuple[3])
    firstState = False
    gamesNum = 1
    maxHits = 0
    avgHits = 0

    while True: #main game loop
        if graphics:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    break

        if score < 0:
            score = 0
            q[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]] = r[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]]
            firstState = True
            # play_again = raw_input("Press 'p' to play again")
            # if play_again != 'p':
            #     break
            print("Game Number",gamesNum)
            if gamesNum == maxGames:
                save_q_learning(q)
                print("The average number of hits was", avgHits/1.0/gamesNum)
                print("The max number of hits was", maxHits)
                return
            gamesNum += 1
            resetGame(game_state_tuple)
            paddle1 = pygame.Rect(PADDLEOFFSET, 0, paddle_width, paddle_height1)
            paddle2 = pygame.Rect(width - PADDLEOFFSET - paddle_width, game_state_tuple[4]-paddle_height2/2, paddle_width, paddle_height2)
            ball = pygame.Rect(game_state_tuple[0], game_state_tuple[1], paddle_width, paddle_width)

        if graphics:
            drawArena()
            drawPaddle(paddle1)
            drawPaddle(paddle2)
            drawBall(ball)

        ball = moveBall(ball, game_state_tuple[2]*width, game_state_tuple[3]*height)
        game_state_tuple[2], game_state_tuple[3] = checkEdgeCollision(ball, game_state_tuple[2], game_state_tuple[3])
        lastScore = score
        score = checkPointScored(paddle2, ball, score, game_state_tuple[2])

        if score < 0:
            # print(lastScore)
            if lastScore > maxHits:
                maxHits = lastScore
            avgHits+=lastScore

        else:
            prev_state = cur_state
            cur_state = determineState(paddle2, ball, game_state_tuple[2], game_state_tuple[3])
            game_state_tuple[2], game_state_tuple[3] = checkHitBall(ball, paddle1, paddle2, game_state_tuple[2], game_state_tuple[3])
            # print(cur_state)
            paddle1 = hard_coded_paddle (ball, paddle1)
            paddle2 = q_paddle(q, cur_state, paddle2)

            displayScore(score)

            if graphics:
                pygame.display.update()
                FPSCLOCK.tick(FPS)

            # print(cur_state)
            learning_times[cur_state[0]][cur_state[1]][cur_state[2]][cur_state[3]][cur_state[4]]+=1
            # print(q[cur_state[0]][cur_state[1]][cur_state[2]])
            # print()
            # for v in learning_times:
            #     for w in v:
            #         for x in w:
            #             for y in x:
            #                 for z in y:
            #                     IF Z >0:
            #                         print(z)
            eval_q(q, r, prev_state, cur_state)
            firstState = False

if __name__=='__main__':
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
