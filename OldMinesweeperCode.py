import pygame
import random
window_size = 500
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
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
    while(arr[mineX][mineY] < -1):
        mineX = random.randint(0, 9)
        mineY = random.randint(0, 9)
    
    arr[mineX][mineY] = -10
    
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

def clear(i, j):
    clickedArr[i][j] = 0
    
    global gameEnded
    if i-1 >= 0 and j-1 >= 0:
       if arr[i-1][j-1] == 0 and clickedArr[i-1][j-1] != 0:
           clear(i-1, j-1)
       if clickedArr[i-1][j-1] != 0 and flaggedArr[i-1][j-1] == False:
           clickedArr[i-1][j-1] = 0
       if arr[i-1][j-1]  < 0 and flaggedArr[i-1][j-1] == False:
          
           gameEnded = True
           clickSpot[0] = i-1
           clickSpot[1] = j-1
           
    if i-1 >= 0 and j >= 0:
        if arr[i-1][j] == 0 and clickedArr[i-1][j] != 0:
           clear(i-1, j)
        if clickedArr[i-1][j] != 0 and flaggedArr[i-1][j] == False:
           clickedArr[i-1][j] = 0
        if arr[i-1][j]  < 0 and flaggedArr[i-1][j] == False:
        #    global gameEnded;
           gameEnded = True
           clickSpot[0] = i-1
           clickSpot[1] = j   
        
    if i-1 >= 0 and j+1 < 10:
        if arr[i-1][j+1] == 0 and clickedArr[i-1][j+1] != 0:
           clear(i-1, j+1)
        if clickedArr[i-1][j+1] != 0 and flaggedArr[i-1][j+1] == False:
           clickedArr[i-1][j+1] = 0
        if arr[i-1][j+1]  < 0  and flaggedArr[i-1][j+1] == False:
        #    global gameEnded;
           gameEnded = True
           clickSpot[0] = i-1
           clickSpot[1] = j+1
    
    if i >= 0 and j-1 >= 0:
        if arr[i][j-1] == 0 and clickedArr[i][j-1] != 0:
           clear(i, j-1)
        if clickedArr[i][j-1] != 0 and flaggedArr[i][j-1] == False:
           clickedArr[i][j-1] = 0
        if arr[i][j-1]  < 0  and flaggedArr[i][j-1] == False:
        #    global gameEnded;
           gameEnded = True
           clickSpot[0] = i
           clickSpot[1] = j-1
           
    if i >= 0 and j+1 < 10:
        if arr[i][j+1] == 0 and clickedArr[i][j+1] != 0:
           clear(i, j+1)
        if clickedArr[i][j+1] != 0 and flaggedArr[i][j+1] == False:
           clickedArr[i][j+1] = 0 
        if arr[i][j+1]  < 0 and flaggedArr[i][j+1] == False:
        #    global gameEnded;
           gameEnded = True
           clickSpot[0] = i
           clickSpot[1] = j+1  
              
    if i+1 < 10 and j-1 >= 0:
        if arr[i+1][j-1] == 0 and clickedArr[i+1][j-1] != 0:
           clear(i+1, j-1)
        if clickedArr[i+1][j-1] != 0 and flaggedArr[i+1][j-1] == False:
           clickedArr[i+1][j-1] = 0
        if arr[i+1][j-1]  < 0  and flaggedArr[i+1][j-1] == False:
        #    global gameEnded;
           gameEnded = True
           clickSpot[0] = i+1
           clickSpot[1] = j-1
                   
    if i+1 < 10 and j < 10:
        if arr[i+1][j] == 0 and clickedArr[i+1][j] != 0:
           clear(i+1, j)
        if clickedArr[i+1][j] != 0 and flaggedArr[i+1][j] == False:
           clickedArr[i+1][j] = 0   
        if arr[i+1][j]  < 0  and flaggedArr[i+1][j] == False:
        #    global gameEnded;
           gameEnded = True
           clickSpot[0] = i+1
           clickSpot[1] = j
                
    if i+1 < 10 and j+1 < 10:
        if arr[i+1][j+1] == 0 and clickedArr[i+1][j+1] != 0:
           clear(i+1, j+1)
        if clickedArr[i+1][j+1] != 0 and flaggedArr[i+1][j+1] == False:
           clickedArr[i+1][j+1] = 0
        if arr[i+1][j+1]  < 0 and flaggedArr[i+1][j+1] == False:
        #    global gameEnded;
           gameEnded = True
           clickSpot[0] = i+1
           clickSpot[1] = j+1     

def clearAdjacent(i, j):
    clickedArr[i][j] = 0
    if i-1 >= 0 and j-1 >= 0:
       if arr[i-1][j-1] == 0 and clickedArr[i-1][j-1] != 0:
           clear(i-1, j-1)
       
           
    if i-1 >= 0 and j >= 0:
        if arr[i-1][j] == 0 and clickedArr[i-1][j] != 0:
           clear(i-1, j)
        
    if i-1 >= 0 and j+1 < 10:
        if arr[i-1][j+1] == 0 and clickedArr[i-1][j+1] != 0:
           clear(i-1, j+1)
        
    if i >= 0 and j-1 >= 0:
        if arr[i][j-1] == 0 and clickedArr[i][j-1] != 0:
           clear(i, j-1)
        
    if i >= 0 and j+1 < 10:
        if arr[i][j+1] == 0 and clickedArr[i][j+1] != 0:
           clear(i, j+1)
        
    if i+1 < 10 and j-1 >= 0:
        if arr[i+1][j-1] == 0 and clickedArr[i+1][j-1] != 0:
           clear(i+1, j-1)
              
    if i+1 < 10 and j < 10:
        if arr[i+1][j] == 0 and clickedArr[i+1][j] != 0:
           clear(i+1, j)
             
    if i+1 < 10 and j+1 < 10:
        if arr[i+1][j+1] == 0 and clickedArr[i+1][j+1] != 0:
           clear(i+1, j+1)
         


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
    if gameStarted == False and gameEnded == False:
        for i in range(10):
            for j in range(10):
                screen.blit(MinesweeperUnexploredTile, (i * 50, j * 50))
                
        if(pygame.mouse.get_pressed(num_buttons = 3)[0]):
            gameStarted = True
            clickedArr[posX][posY] = 0
            if arr[posX][posY] < 0:
                gameEnded = True
                clickSpot[0] = posX
                clickSpot[1] = posY
            
        
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
                if numAdjacentFlags == arr[posX][posY]:
                    clear(posX, posY)
                clickedArr[posX][posY] = 0
            if arr[posX][posY] >= 0 and flaggedArr[posX][posY] == False:
                clearAdjacent(posX, posY)
                clickedArr[posX][posY] = 0
            if arr[posX][posY] < 0 and flaggedArr[posX][posY] == False:
                gameEnded = True
                clickSpot[0] = posX
                clickSpot[1] = posY
                clickedArr[posX][posY] = 0
            
            
         if(pygame.mouse.get_pressed(num_buttons = 3)[2]):
             
            if clickedArr[posX][posY] == -1 and RIGHT_MOUSE_UP == True:
                flaggedArr[posX][posY] = not flaggedArr[posX][posY]
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
        
    # RENDER YOUR GAME HERE
    # print(pygame.mouse.get_pressed(num_buttons = 3))
    # print(pygame.mouse.get_pos())
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


