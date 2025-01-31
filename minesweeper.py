import gymnasium as gym
import math
import pygame
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count

import numpy
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import minesweeper_env
window_size = 500
screen = None
clock = None
running = None
gameStarted = None
gameEnded = False
RIGHT_MOUSE_UP = None

clickSpot = None

arr = None
clickedArr = None
flaggedArr = None

screen = None
clock = None
posX = None
posY = None

MinesweeperOneTile = None
MinesweeperTwoTile = None
MinesweeperThreeTile = None
MinesweeperFourTile = None
MinesweeperFiveTile = None
MinesweeperSixTile = None
MinesweeperBlankTile = None
MinesweeperUnexploredTile = None
MinesweeperMineTile = None
MinesweeperMineTileClicked = None
MinesweeperFlagTile = None

def render():
   running = True
   global screen
   global clock
   global posX
   global posY
   
   while running:
    
    
    
    # psychic reading for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    posX = int(pygame.mouse.get_pos()[0] / 50)
    posY = int(pygame.mouse.get_pos()[1] / 50)
    
    # print(posX, posY)
    
    renderStep()
    # print("renedering")
    # RENDER YOUR GAME HERE
    # print(pygame.mouse.get_pressed(num_buttons = 3))
    # print(pygame.mouse.get_pos())
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60) 
def renderAuto(model):
   running = True
   stepsNum = 0
   global screen
   global clock
   global posX
   global posY
   gameWon = False
#    board = getObs()
#    board = numpy.array(board, dtype="float32")
#    board = torch.tensor(board)
#    board = board.reshape(1, 10, 10)
#    coordX = 0
#    coordY = 0
# # print(board)
#    temp = model(board)
#    temp = temp.flatten()
#    for i in range(100):
    
#         if temp[i].item() == temp.max(0).values:
#             coordX = i % 10
#             coordY = int(i / 10)
   
   while running:
    board = getObs()
    # print(board)
    board = numpy.array(board, dtype="float32")
    board = torch.tensor(board)
    board = board.reshape(1, 10, 10)
    coordX = 0
    coordY = 0
    
# print(board)
    temp = model(board)
    temp = temp.flatten()
    max = -10000
    for i in range(100):
        tempY = i % 10
        tempX = int(i / 10)
        val = temp[i].item()
        if(clickedArr[tempX][tempY] == 0):
            val = -1000
        if val >= max:
            coordY = i % 10
            coordX = int(i / 10)
            max = val
    # print(coordX, coordY)
    
    # psychic reading for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    
    # print(posX, posY)
    if not (gameEnded or endConditionsSatisfied()):
        renderStepAuto(coordX, coordY)
        
    if gameEnded and endConditionsSatisfied():
        for i in range(10):
            for j in range(10):
                if arr[i][j] == -10:
                    screen.blit(MinesweeperMineTile, (i * 50, j * 50))
                if arr[i][j] == 0:
                        screen.blit(MinesweeperBlankTile, (i * 50, j * 50))
                if arr[i][j] == 1:
                        screen.blit(MinesweeperOneTile, (i * 50, j * 50))
                if arr[i][j] == 2:
                        screen.blit(MinesweeperTwoTile, (i * 50, j * 50))
                if arr[i][j] == 3:
                        screen.blit(MinesweeperThreeTile, (i * 50, j * 50))
                if arr[i][j] == 4:
                        screen.blit(MinesweeperFourTile, (i * 50, j * 50))
                if arr[i][j] == 5:
                        screen.blit(MinesweeperFiveTile, (i * 50, j * 50))
                if arr[i][j] == 6:
                        screen.blit(MinesweeperSixTile, (i * 50, j * 50))
                if arr[i][j] == -10:
                        screen.blit(MinesweeperFlagTile, (i * 50, j * 50))
        gameWon = True
        return gameWon
    elif gameEnded or stepsNum == 50:
        for i in range(10):
            for j in range(10):
                if arr[i][j] == -10:
                    screen.blit(MinesweeperMineTile, (i * 50, j * 50))
                if arr[i][j] == 0:
                        screen.blit(MinesweeperBlankTile, (i * 50, j * 50))
                if arr[i][j] == 1:
                        screen.blit(MinesweeperOneTile, (i * 50, j * 50))
                if arr[i][j] == 2:
                        screen.blit(MinesweeperTwoTile, (i * 50, j * 50))
                if arr[i][j] == 3:
                        screen.blit(MinesweeperThreeTile, (i * 50, j * 50))
                if arr[i][j] == 4:
                        screen.blit(MinesweeperFourTile, (i * 50, j * 50))
                if arr[i][j] == 5:
                        screen.blit(MinesweeperFiveTile, (i * 50, j * 50))
                if arr[i][j] == 6:
                        screen.blit(MinesweeperSixTile, (i * 50, j * 50))
                if arr[i][j] == -10:
                        screen.blit(MinesweeperMineTileClicked, (i * 50, j * 50))
        gameWon = False
        return gameWon
    
    
                                
        
    # print("renedering")
    # RENDER YOUR GAME HERE
    # print(pygame.mouse.get_pressed(num_buttons = 3))
    # print(pygame.mouse.get_pos())
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)      
    stepsNum += 1
def renderStepAuto(x, y):
    global clickedArr
    global arr
    global flaggedArr
    global clickSpot
    global screen
    global clock
    global running
    global gameStarted
    global gameEnded
    
    
       
    if gameEnded == False:
        evalAction(x, y, 0)
        # print("evaluating")
        for i in range(10):
            for j in range(10):
                screen.blit(MinesweeperUnexploredTile, (i * 50, j * 50))
                
        # if(pygame.mouse.get_pressed(num_buttons = 3)[0]):
            
        #     evalAction(posX, posY, 0)
            # clickedArr[posX][posY] = 0
            # if arr[posX][posY] < 0:
            #     gameEnded = True
            #     clickSpot[0] = posX
            #     clickSpot[1] = posY
            
        
    
        for i in range(10):
            for j in range(10):
                if(clickedArr[i][j] == 0):
                    if arr[i][j] == -10:
                        screen.blit(MinesweeperMineTile, (i * 50, j * 50))
                    if arr[i][j] == 0:
                        screen.blit(MinesweeperBlankTile, (i * 50, j * 50))
                    if arr[i][j] == 1:
                        screen.blit(MinesweeperOneTile, (i * 50, j * 50))
                    if arr[i][j] == 2:
                        screen.blit(MinesweeperTwoTile, (i * 50, j * 50))
                    if arr[i][j] == 3:
                        screen.blit(MinesweeperThreeTile, (i * 50, j * 50))
                    if arr[i][j] == 4:
                        screen.blit(MinesweeperFourTile, (i * 50, j * 50))
                    if arr[i][j] == 5:
                        screen.blit(MinesweeperFiveTile, (i * 50, j * 50))
                    if arr[i][j] == 6:
                        screen.blit(MinesweeperSixTile, (i * 50, j * 50))
                else:
                    if flaggedArr[i][j]:
                        screen.blit(MinesweeperFlagTile, (i * 50, j * 50))
                    else:
                        screen.blit(MinesweeperUnexploredTile, (i * 50, j * 50))
        #  if(pygame.mouse.get_pressed(num_buttons = 3)[0]):
        #      evalAction(posX, posY, 0)
            # if clickedArr[posX][posY] == 0:
            #     numAdjacentFlags = 0
            #     if posX-1 >= 0 and posY-1 >= 0 and flaggedArr[posX-1][posY-1] == True:
            #         numAdjacentFlags += 1
            #     if posX-1 >= 0 and posY >= 0 and flaggedArr[posX-1][posY] == True:
            #         numAdjacentFlags += 1
            #     if posX-1 >= 0 and posY+1 < 10 and flaggedArr[posX-1][posY+1] == True:
            #         numAdjacentFlags += 1   
            #     if posX >= 0 and posY-1 >= 0 and flaggedArr[posX][posY-1] == True:
            #         numAdjacentFlags += 1 
            #     if posX >= 0 and posY+1 < 10 and flaggedArr[posX][posY+1] == True:
            #         numAdjacentFlags += 1 
            #     if posX+1 < 10 and posY-1 >= 0 and flaggedArr[posX+1][posY-1] == True:
            #         numAdjacentFlags += 1 
            #     if posX+1 < 10 and posY < 10 and flaggedArr[posX+1][posY] == True:
            #         numAdjacentFlags += 1 
            #     if posX+1 < 10 and posY+1 < 10 and flaggedArr[posX+1][posY+1] == True:
            #         numAdjacentFlags += 1 
            #     # print(numAdjacentFlags)
            #     if numAdjacentFlags == arr[posX][posY]:
            #         clear(posX, posY)
            #     clickedArr[posX][posY] = 0
            # if arr[posX][posY] >= 0 and flaggedArr[posX][posY] == False:
            #     clearAdjacent(posX, posY)
            #     clickedArr[posX][posY] = 0
            # if arr[posX][posY] < 0 and flaggedArr[posX][posY] == False:
            #     gameEnded = True
            #     clickSpot[0] = posX
            #     clickSpot[1] = posY
            #     clickedArr[posX][posY] = 0
        #  if(pygame.mouse.get_pressed(num_buttons = 3)[1]):
        #      print(getObs())
            
        #  if(pygame.mouse.get_pressed(num_buttons = 3)[2]):
        #     evalAction(posX, posY, 2)
            # if clickedArr[posX][posY] == -1 and RIGHT_MOUSE_UP == True:
            #     flaggedArr[posX][posY] = not flaggedArr[posX][posY]
            # RIGHT_MOUSE_UP = False
        #  else:
        #     RIGHT_MOUSE_UP = True
    else:
        for i in range(10):
            for j in range(10):
                if(clickedArr[i][j] == 0):
                    if i == clickSpot[0] and j == clickSpot[1]:
                        screen.blit(MinesweeperMineTileClicked, (i * 50, j * 50))
                    elif arr[i][j] == -10:
                        screen.blit(MinesweeperMineTile, (i * 50, j * 50))
                    elif arr[i][j] == 0:
                        screen.blit(MinesweeperBlankTile, (i * 50, j * 50))
                    elif arr[i][j] == 1:
                        screen.blit(MinesweeperOneTile, (i * 50, j * 50))
                    elif arr[i][j] == 2:
                        screen.blit(MinesweeperTwoTile, (i * 50, j * 50))
                    elif arr[i][j] == 3:
                        screen.blit(MinesweeperThreeTile, (i * 50, j * 50))
                    elif arr[i][j] == 4:
                        screen.blit(MinesweeperFourTile, (i * 50, j * 50))
                    elif arr[i][j] == 5:
                        screen.blit(MinesweeperFiveTile, (i * 50, j * 50))
                    elif arr[i][j] == 6:
                        screen.blit(MinesweeperSixTile, (i * 50, j * 50))
                else:
                    if i == clickSpot[0] and j == clickSpot[1]:
                        screen.blit(MinesweeperMineTileClicked, (i * 50, j * 50))
                    elif flaggedArr[i][j]:
                        screen.blit(MinesweeperFlagTile, (i * 50, j * 50))
                    elif arr[i][j] == -10:
                        screen.blit(MinesweeperMineTile, (i * 50, j * 50))
                    else:
                        screen.blit(MinesweeperUnexploredTile, (i * 50, j * 50))


def renderStep():
    global clickedArr
    global arr
    global flaggedArr
    global clickSpot
    global screen
    global clock
    global running
    global gameStarted
    global gameEnded
    global RIGHT_MOUSE_UP   
    if gameStarted == False and gameEnded == False:
        for i in range(10):
            for j in range(10):
                screen.blit(MinesweeperUnexploredTile, (i * 50, j * 50))
                
        if(pygame.mouse.get_pressed(num_buttons = 3)[0]):
            gameStarted = True
            evalAction(posX, posY, 0)
            # clickedArr[posX][posY] = 0
            # if arr[posX][posY] < 0:
            #     gameEnded = True
            #     clickSpot[0] = posX
            #     clickSpot[1] = posY
            
        
    elif gameEnded == False:
         for i in range(10):
            for j in range(10):
                if(clickedArr[i][j] == 0):
                    if arr[i][j] == -10:
                        screen.blit(MinesweeperMineTile, (i * 50, j * 50))
                    if arr[i][j] == 0:
                        screen.blit(MinesweeperBlankTile, (i * 50, j * 50))
                    if arr[i][j] == 1:
                        screen.blit(MinesweeperOneTile, (i * 50, j * 50))
                    if arr[i][j] == 2:
                        screen.blit(MinesweeperTwoTile, (i * 50, j * 50))
                    if arr[i][j] == 3:
                        screen.blit(MinesweeperThreeTile, (i * 50, j * 50))
                    if arr[i][j] == 4:
                        screen.blit(MinesweeperFourTile, (i * 50, j * 50))
                    if arr[i][j] == 5:
                        screen.blit(MinesweeperFiveTile, (i * 50, j * 50))
                    if arr[i][j] == 6:
                        screen.blit(MinesweeperSixTile, (i * 50, j * 50))
                else:
                    if flaggedArr[i][j]:
                        screen.blit(MinesweeperFlagTile, (i * 50, j * 50))
                    else:
                        screen.blit(MinesweeperUnexploredTile, (i * 50, j * 50))
         if(pygame.mouse.get_pressed(num_buttons = 3)[0]):
             evalAction(posX, posY, 0)
            # if clickedArr[posX][posY] == 0:
            #     numAdjacentFlags = 0
            #     if posX-1 >= 0 and posY-1 >= 0 and flaggedArr[posX-1][posY-1] == True:
            #         numAdjacentFlags += 1
            #     if posX-1 >= 0 and posY >= 0 and flaggedArr[posX-1][posY] == True:
            #         numAdjacentFlags += 1
            #     if posX-1 >= 0 and posY+1 < 10 and flaggedArr[posX-1][posY+1] == True:
            #         numAdjacentFlags += 1   
            #     if posX >= 0 and posY-1 >= 0 and flaggedArr[posX][posY-1] == True:
            #         numAdjacentFlags += 1 
            #     if posX >= 0 and posY+1 < 10 and flaggedArr[posX][posY+1] == True:
            #         numAdjacentFlags += 1 
            #     if posX+1 < 10 and posY-1 >= 0 and flaggedArr[posX+1][posY-1] == True:
            #         numAdjacentFlags += 1 
            #     if posX+1 < 10 and posY < 10 and flaggedArr[posX+1][posY] == True:
            #         numAdjacentFlags += 1 
            #     if posX+1 < 10 and posY+1 < 10 and flaggedArr[posX+1][posY+1] == True:
            #         numAdjacentFlags += 1 
            #     # print(numAdjacentFlags)
            #     if numAdjacentFlags == arr[posX][posY]:
            #         clear(posX, posY)
            #     clickedArr[posX][posY] = 0
            # if arr[posX][posY] >= 0 and flaggedArr[posX][posY] == False:
            #     clearAdjacent(posX, posY)
            #     clickedArr[posX][posY] = 0
            # if arr[posX][posY] < 0 and flaggedArr[posX][posY] == False:
            #     gameEnded = True
            #     clickSpot[0] = posX
            #     clickSpot[1] = posY
            #     clickedArr[posX][posY] = 0
         if(pygame.mouse.get_pressed(num_buttons = 3)[1]):
             print(getObs())
            
         if(pygame.mouse.get_pressed(num_buttons = 3)[2]):
            evalAction(posX, posY, 2)
            # if clickedArr[posX][posY] == -1 and RIGHT_MOUSE_UP == True:
            #     flaggedArr[posX][posY] = not flaggedArr[posX][posY]
            RIGHT_MOUSE_UP = False
         else:
            RIGHT_MOUSE_UP = True
    else:
        for i in range(10):
            for j in range(10):
                if(clickedArr[i][j] == 0):
                    if i == clickSpot[0] and j == clickSpot[1]:
                        screen.blit(MinesweeperMineTileClicked, (i * 50, j * 50))
                    elif arr[i][j] == -10:
                        screen.blit(MinesweeperMineTile, (i * 50, j * 50))
                    elif arr[i][j] == 0:
                        screen.blit(MinesweeperBlankTile, (i * 50, j * 50))
                    elif arr[i][j] == 1:
                        screen.blit(MinesweeperOneTile, (i * 50, j * 50))
                    elif arr[i][j] == 2:
                        screen.blit(MinesweeperTwoTile, (i * 50, j * 50))
                    elif arr[i][j] == 3:
                        screen.blit(MinesweeperThreeTile, (i * 50, j * 50))
                    elif arr[i][j] == 4:
                        screen.blit(MinesweeperFourTile, (i * 50, j * 50))
                    elif arr[i][j] == 5:
                        screen.blit(MinesweeperFiveTile, (i * 50, j * 50))
                    elif arr[i][j] == 6:
                        screen.blit(MinesweeperSixTile, (i * 50, j * 50))
                else:
                    if i == clickSpot[0] and j == clickSpot[1]:
                        screen.blit(MinesweeperMineTileClicked, (i * 50, j * 50))
                    elif flaggedArr[i][j]:
                        screen.blit(MinesweeperFlagTile, (i * 50, j * 50))
                    elif arr[i][j] == -10:
                        screen.blit(MinesweeperMineTile, (i * 50, j * 50))
                    else:
                        screen.blit(MinesweeperUnexploredTile, (i * 50, j * 50))


def isGameFinished():
    
    return gameEnded

def getClickedArr():
    return clickedArr

def getArr():
    return arr

def endConditionsSatisfied():
    cnt = 0
    for i in range(10):
        for j in range(10):
            if arr[i][j] >= 0 and clickedArr[i][j] == 0:
                cnt += 1
    if cnt == 90:
        return True
    return False
    #return cnt

def getObs():
    newArr = [[-1 for x in range(10)] for y in range(10)]
    for i in range(10):
        for j in range(10):
            if(clickedArr[i][j] == 0):
                newArr[i][j] = arr[i][j]
            else:
                if(flaggedArr[i][j] == True):
                    newArr[i][j] = -8
                else:
                    newArr[i][j] = -5
    # print(newArr)
    return newArr
def evalAction(posX, posY, a):
    reward = 0
    tempVal = 0
    global gameEnded
    if(a == 0):
     if clickedArr[posX][posY] == 0:
        
        numAdjacentFlags = 0
        if posX-1 >= 0 and posY-1 >= 0 and flaggedArr[posX-1][posY-1] == True:
            numAdjacentFlags += 1
        if posX-1 >= 0 and posY >= 0 and flaggedArr[posX-1][posY] == True:
            numAdjacentFlags += 1
        if posX-1 >= 0 and posY+1 < 10 and flaggedArr[posX-1][posY+1] == True:
            numAdjacentFlags += 1   
        if posX >= 0 and posY-1 >= 0 and flaggedArr[posX][posY-1] == True:
            numAdjacentFlags += 1 
        if posX >= 0 and posY+1 < 10 and flaggedArr[posX][posY+1] == True:
            numAdjacentFlags += 1 
        if posX+1 < 10 and posY-1 >= 0 and flaggedArr[posX+1][posY-1] == True:
            numAdjacentFlags += 1 
        if posX+1 < 10 and posY < 10 and flaggedArr[posX+1][posY] == True:
            numAdjacentFlags += 1 
        if posX+1 < 10 and posY+1 < 10 and flaggedArr[posX+1][posY+1] == True:
            numAdjacentFlags += 1 
                # print(numAdjacentFlags)
        # if numAdjacentFlags == arr[posX][posY]:
        #     reward += clear(posX, posY)
        clickedArr[posX][posY] = 0
        reward -= 0.3
     elif arr[posX][posY] >= 0 and flaggedArr[posX][posY] == False:
            
            numAdjacentCleared = 0
            if posX-1 >= 0 and posY-1 >= 0 and clickedArr[posX-1][posY-1] == 0:
                numAdjacentCleared += 1
            if posX-1 >= 0 and posY >= 0 and clickedArr[posX-1][posY] == 0:
                numAdjacentCleared += 1
            if posX-1 >= 0 and posY+1 < 10 and clickedArr[posX-1][posY+1] == 0:
                numAdjacentCleared += 1   
            if posX >= 0 and posY-1 >= 0 and clickedArr[posX][posY-1] == 0:
                numAdjacentCleared += 1 
            if posX >= 0 and posY+1 < 10 and clickedArr[posX][posY+1] == 0:
                numAdjacentCleared += 1 
            if posX+1 < 10 and posY-1 >= 0 and clickedArr[posX+1][posY-1] == 0:
                numAdjacentCleared += 1 
            if posX+1 < 10 and posY < 10 and clickedArr[posX+1][posY] == 0:
                numAdjacentCleared += 1 
            if posX+1 < 10 and posY+1 < 10 and clickedArr[posX+1][posY+1] == 0:
                numAdjacentCleared += 1 
            tempVal += clearAdjacent(posX, posY)    
            if(numAdjacentCleared == 0):
                reward -= 0.3
            else:
                reward += 0.3
            clickedArr[posX][posY] = 0
     if arr[posX][posY] < 0 and flaggedArr[posX][posY] == False:
            reward = -1
            gameEnded = True
            clickSpot[0] = posX
            clickSpot[1] = posY
            clickedArr[posX][posY] = 0
    # if(a >= 1):
    #     if clickedArr[posX][posY] == -1:
    #         flaggedArr[posX][posY] = not flaggedArr[posX][posY]
    #         if arr[posX][posY] == -10 and flaggedArr[posX][posY]:
    #             reward += 0.05
    #         if arr[posX][posY] == -10 and not flaggedArr[posX][posY]:
    #             reward -= 0.05
    #     else:
    #         reward -= 0.05
    # if reward != 0:
    #     print(endConditionsSatisfied())
    if endConditionsSatisfied():
        gameEnded = True
        print("DING DING DING")
        reward += 1
    # print(reward)
    return reward

def setup():
    global clickedArr
    global arr
    global flaggedArr
    global clickSpot
    global screen
    global clock
    global running
    global gameStarted
    global gameEnded
    global RIGHT_MOUSE_UP   
    global running
    global MinesweeperBlankTile
    global MinesweeperOneTile
    global MinesweeperTwoTile
    global MinesweeperThreeTile
    global MinesweeperFourTile
    global MinesweeperFiveTile
    global MinesweeperSixTile
    global MinesweeperUnexploredTile
    global MinesweeperFlagTile
    global MinesweeperMineTile
    global MinesweeperMineTileClicked
    
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    
    MinesweeperBlankTile = pygame.image.load('Image Files/MinesweeperBlankTile.png').convert()
    MinesweeperBlankTile = pygame.transform.scale(MinesweeperBlankTile, (50, 50))
    MinesweeperOneTile = pygame.image.load('Image Files/MinesweeperOneTile.png').convert()
    MinesweeperOneTile = pygame.transform.scale(MinesweeperOneTile, (50, 50))
    MinesweeperTwoTile = pygame.image.load('Image Files/MinesweeperTwoTile.png').convert()
    MinesweeperTwoTile = pygame.transform.scale(MinesweeperTwoTile, (50, 50))
    MinesweeperThreeTile = pygame.image.load('Image Files/MinesweeperThreeTile.png').convert()
    MinesweeperThreeTile = pygame.transform.scale(MinesweeperThreeTile, (50, 50))
    MinesweeperFourTile = pygame.image.load('Image Files/MinesweeperFourTile.png').convert()
    MinesweeperFourTile = pygame.transform.scale(MinesweeperFourTile, (50, 50))
    MinesweeperFiveTile = pygame.image.load('Image Files/MinesweeperFiveTile.png').convert()
    MinesweeperFiveTile = pygame.transform.scale(MinesweeperFiveTile, (50, 50))
    MinesweeperSixTile = pygame.image.load('Image Files/MinesweeperSixTile.png').convert()
    MinesweeperSixTile = pygame.transform.scale(MinesweeperSixTile, (50, 50))
    MinesweeperUnexploredTile = pygame.image.load('Image Files/MinesweeperUnexploredTile.png').convert()
    MinesweeperUnexploredTile = pygame.transform.scale(MinesweeperUnexploredTile, (50, 50))
    MinesweeperFlagTile = pygame.image.load('Image Files/MinesweeperFlagTile.png').convert()
    MinesweeperFlagTile = pygame.transform.scale(MinesweeperFlagTile, (50, 50))
    MinesweeperMineTile = pygame.image.load('Image Files/MinesweeperMineTile.png').convert()
    MinesweeperMineTile = pygame.transform.scale(MinesweeperMineTile, (50, 50))
    MinesweeperMineTileClicked = pygame.image.load('Image Files/MinesweeperMineTileClicked.png').convert()
    MinesweeperMineTileClicked = pygame.transform.scale(MinesweeperMineTileClicked, (50, 50))
    
    running = True
    gameStarted = False
    gameEnded = False
    RIGHT_MOUSE_UP = True

    clickSpot = [0,0]

    arr = [[-1 for x in range(10)] for y in range(10)]
    clickedArr = [[-1 for x in range(10)] for y in range(10)]
    flaggedArr = [[False for x in range(10)] for y in range(10)]

    for i in range(10):
        mineX = random.randint(0, 9)
        mineY = random.randint(0, 9)
        while(arr[mineX][mineY] < -1 or (mineX == 5 and mineY == 5)):
            mineX = random.randint(0, 9)
            mineY = random.randint(0, 9)
    
        arr[mineX][mineY] = -10
        # arr[0][3] = -10
        # arr[6][2] = -10
        # arr[8][8] = -10
        # arr[9][4] = -10
        # arr[3][5] = -10
        # arr[1][6] = -10
        # arr[1][7] = -10
        # arr[0][8] = -10
        # arr[5][6] = -10
        # arr[0][0] = -10
    
    for i in range(10):
     for j in range(10):
        if(arr[i][j] != -10):
            numAdjacentMines = 0
            if i-1 >= 0 and j-1 >= 0 and arr[i-1][j-1] == -10:
                numAdjacentMines += 1
            if i-1 >= 0 and j >= 0 and arr[i-1][j] == -10:
                numAdjacentMines += 1
            if i-1 >= 0 and j+1 < 10 and arr[i-1][j+1] == -10:
                numAdjacentMines += 1   
            if i >= 0 and j-1 >= 0 and arr[i][j-1] == -10:
                numAdjacentMines += 1 
            if i >= 0 and j+1 < 10 and arr[i][j+1] == -10:
                numAdjacentMines += 1 
            if i+1 < 10 and j-1 >= 0 and arr[i+1][j-1] == -10:
                numAdjacentMines += 1 
            if i+1 < 10 and j < 10 and arr[i+1][j] == -10:
                numAdjacentMines += 1 
            if i+1 < 10 and j+1 < 10 and arr[i+1][j+1] == -10:
                numAdjacentMines += 1 
            arr[i][j] = numAdjacentMines
    # render()


def clear(i, j):
    reward = 0
    if(clickedArr[i][j] != 0):
        reward = 0.05
    if(clickedArr[i][j] == 0):
        reward -= 0.3     
            
    clickedArr[i][j] = 0  
    
    global gameEnded
    if i-1 >= 0 and j-1 >= 0:
       if arr[i-1][j-1] == 0 and clickedArr[i-1][j-1] != 0:
           reward += clear(i-1, j-1)
       if clickedArr[i-1][j-1] != 0 and flaggedArr[i-1][j-1] == False:
           clickedArr[i-1][j-1] = 0
           reward += 0.05
       if arr[i-1][j-1]  < 0 and flaggedArr[i-1][j-1] == False:
           reward = -1
           print(reward)
           gameEnded = True
           clickSpot[0] = i-1
           clickSpot[1] = j-1
           
    if i-1 >= 0 and j >= 0:
        if arr[i-1][j] == 0 and clickedArr[i-1][j] != 0:
           reward += clear(i-1, j)
        if clickedArr[i-1][j] != 0 and flaggedArr[i-1][j] == False:
           clickedArr[i-1][j] = 0
           reward += 0.05
        if arr[i-1][j]  < 0 and flaggedArr[i-1][j] == False:
        #    global gameEnded;
           reward = -1
           print(reward)
           gameEnded = True
           
           clickSpot[0] = i-1
           clickSpot[1] = j   
        
    if i-1 >= 0 and j+1 < 10:
        if arr[i-1][j+1] == 0 and clickedArr[i-1][j+1] != 0:
           reward += clear(i-1, j+1)
        if clickedArr[i-1][j+1] != 0 and flaggedArr[i-1][j+1] == False:
           clickedArr[i-1][j+1] = 0
           reward += 0.05
        if arr[i-1][j+1]  < 0  and flaggedArr[i-1][j+1] == False:
        #    global gameEnded;
           reward = -1
           print(reward)
           gameEnded = True
           
           clickSpot[0] = i-1
           clickSpot[1] = j+1
    
    if i >= 0 and j-1 >= 0:
        if arr[i][j-1] == 0 and clickedArr[i][j-1] != 0:
           reward += clear(i, j-1)
        if clickedArr[i][j-1] != 0 and flaggedArr[i][j-1] == False:
           clickedArr[i][j-1] = 0
           reward += 0.05
        if arr[i][j-1]  < 0  and flaggedArr[i][j-1] == False:
        #    global gameEnded;
           reward = -1
           print(reward)
           gameEnded = True
          
           clickSpot[0] = i
           clickSpot[1] = j-1
           
    if i >= 0 and j+1 < 10:
        if arr[i][j+1] == 0 and clickedArr[i][j+1] != 0:
           reward += clear(i, j+1)
        if clickedArr[i][j+1] != 0 and flaggedArr[i][j+1] == False:
           clickedArr[i][j+1] = 0 
           reward += 0.05
        if arr[i][j+1]  < 0 and flaggedArr[i][j+1] == False:
        #    global gameEnded;
           reward = -1
           print(reward)
           gameEnded = True
           
           clickSpot[0] = i
           clickSpot[1] = j+1  
              
    if i+1 < 10 and j-1 >= 0:
        if arr[i+1][j-1] == 0 and clickedArr[i+1][j-1] != 0:
           reward += clear(i+1, j-1)
        if clickedArr[i+1][j-1] != 0 and flaggedArr[i+1][j-1] == False:
           clickedArr[i+1][j-1] = 0
           reward += 0.05
        if arr[i+1][j-1]  < 0  and flaggedArr[i+1][j-1] == False:
        #    global gameEnded;
           reward = -1
           print(reward)
           gameEnded = True
           
           clickSpot[0] = i+1
           clickSpot[1] = j-1
                   
    if i+1 < 10 and j < 10:
        if arr[i+1][j] == 0 and clickedArr[i+1][j] != 0:
           reward += clear(i+1, j)
        if clickedArr[i+1][j] != 0 and flaggedArr[i+1][j] == False:
           clickedArr[i+1][j] = 0
           reward += 0.05   
        if arr[i+1][j]  < 0  and flaggedArr[i+1][j] == False:
        #    global gameEnded;
           reward = -1
           print(reward)
           gameEnded = True
           
           clickSpot[0] = i+1
           clickSpot[1] = j
                
    if i+1 < 10 and j+1 < 10:
        if arr[i+1][j+1] == 0 and clickedArr[i+1][j+1] != 0:
           reward += clear(i+1, j+1)
        if clickedArr[i+1][j+1] != 0 and flaggedArr[i+1][j+1] == False:
           clickedArr[i+1][j+1] = 0
           reward += 0.05
        if arr[i+1][j+1]  < 0 and flaggedArr[i+1][j+1] == False:
        #    global gameEnded;
           reward = -1
           print(reward)
           gameEnded = True
           
           clickSpot[0] = i+1
           clickSpot[1] = j+1 
           
     
    return reward 

def clearAdjacent(i, j):
    reward = 0
    if(clickedArr[i][j] != 0):
        reward = 0.05
    
    if i-1 >= 0 and j-1 >= 0:
       if arr[i-1][j-1] == 0 and clickedArr[i-1][j-1] != 0:
           reward += clear(i-1, j-1)
       
           
    if i-1 >= 0 and j >= 0:
        if arr[i-1][j] == 0 and clickedArr[i-1][j] != 0:
            reward += clear(i-1, j)
        
    if i-1 >= 0 and j+1 < 10:
        if arr[i-1][j+1] == 0 and clickedArr[i-1][j+1] != 0:
            reward += clear(i-1, j+1)
        
    if i >= 0 and j-1 >= 0:
        if arr[i][j-1] == 0 and clickedArr[i][j-1] != 0:
            reward += clear(i, j-1)
        
    if i >= 0 and j+1 < 10:
        if arr[i][j+1] == 0 and clickedArr[i][j+1] != 0:
            reward += clear(i, j+1)
        
    if i+1 < 10 and j-1 >= 0:
        if arr[i+1][j-1] == 0 and clickedArr[i+1][j-1] != 0:
            reward += clear(i+1, j-1)
              
    if i+1 < 10 and j < 10:
        if arr[i+1][j] == 0 and clickedArr[i+1][j] != 0:
            reward += clear(i+1, j)
             
    if i+1 < 10 and j+1 < 10:
        if arr[i+1][j+1] == 0 and clickedArr[i+1][j+1] != 0:
            reward += clear(i+1, j+1)
    if(clickedArr[i][j] == 0):
        reward -= 0.3     
            
    clickedArr[i][j] = 0
    return reward    


#  limits FPS to 60
# setup()

# render()
# cnt = 0
        
# arr = getArr()
# clickedArr = getClickedArr()
            
# for i in range(10):
#                 for j in range(10):
#                     if(clickedArr[i][j] == 0 and arr[i][j] >= 0):
#                         cnt += 1
# if(cnt != 0):
#     print(cnt)
pygame.quit()


