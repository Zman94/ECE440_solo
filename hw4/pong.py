import pygame, sys
import pdb
from pygame.locals import *

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 144

#Global Variables to be used through our program

width = 800
height = 600
paddle_width = width/40.0
paddle_height1 = 1*height
paddle_height2 = .2*height
PADDLEOFFSET = 20

# Set up the colours
black     = (0,0,0)
white     = (255,255,255)

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
        velocity_x = velocity_x * -1
    return velocity_x, velocity_y

#Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(ball, paddle1, paddle2, velocity_x):
    if velocity_x < 0 and paddle1.right >= ball.left and paddle1.top < ball.bottom and paddle1.bottom > ball.top:
        return -1
    elif velocity_x > 0 and paddle2.left <= ball.right and paddle2.top < ball.bottom and paddle2.bottom > ball.top:
        return -1
    else:
        return 1

#Checks to see if a point has been scored returns new score
def checkPointScored(paddle2, ball, score, velocity_x):
    #reset points if left wall is hit
    if ball.right >= width:
        return 0
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

#Displays the current score on the screen
def displayScore(score):
    resultSurf = BASICFONT.render('Score = %s' %(score), True, black)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (width - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

def resetGame(game_state_tuple):
    game_state_tuple = [.5*height, .5*width, .03*width, .01*height, .5*height]

#Main function
def main():
    pygame.init()
    global DISPLAYSURF
    ##Font information
    global BASICFONT, BASICFONTSIZE
    ### [ball_x, ball_y, velocity_x, velocity_y, paddle_y] ###
    game_state_tuple = [.5*height, .5*width, .03*width, .01*height, .5*height]

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

    print(game_state_tuple[4]-paddle_height2)
    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET, 0, paddle_width, paddle_height1)
    paddle2 = pygame.Rect(width - PADDLEOFFSET - paddle_width, game_state_tuple[4]-paddle_height2/2, paddle_width, paddle_height2)
    ball = pygame.Rect(game_state_tuple[0], game_state_tuple[1], paddle_width, paddle_width)

    print(paddle_height2)
    #Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(False) # make cursor invisible

    while True: #main game loop
        # if ball.left > width or ball.right < 0:
            # ressetGame(game_state_tuple, score)
            # score = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, game_state_tuple[2], game_state_tuple[3])
        game_state_tuple[2], game_state_tuple[3] = checkEdgeCollision(ball, game_state_tuple[2], game_state_tuple[3])
        score = checkPointScored(paddle2, ball, score, game_state_tuple[2])
        game_state_tuple[2] *= checkHitBall(ball, paddle1, paddle2, game_state_tuple[2])
        paddle1 = hard_coded_paddle (ball, paddle1)

        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    # pdb.set_trace()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
