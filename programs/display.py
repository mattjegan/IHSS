import pygame
from pygame.locals import *
import time
import sys
import operator
import playerClass
import teamClass

WIDTH = 1280
PADDINGX = 20
HEIGHT = 720
TOPPADDINGY = 200
PADDINGY = 20
STATPAD = 10
ALLTIMEPTITLE = 90

def main():
    pygame.init()

    global WIDTH
    WIDTH = pygame.display.Info().current_w
    global HEIGHT
    HEIGHT = pygame.display.Info().current_h - 44

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    startTime = time.time()

    # Screens
    # 0 = All time player stats
    # 1 = Game stats
    # 2 = All time goalie stats
    # 3 = Goalie game stats
    currentScreen = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    pygame.quit()
                    sys.exit()

        ## Get updated data
        teamsAllTime, maxTeamPlayers = loadData("teamData.txt")
        #teamsGame, maxTeamP2 = loadData("game.txt")

        ## Draw background
        screen.fill((0,0,0))

        ## Calculate time:
        currentTime = time.time()

        ## Determine intervals between screen change
        if currentTime - startTime > 5:
            currentScreen += 1
            currentScreen = currentScreen % 2 ## Make between range 0 -> 3 inclusive
            startTime = time.time()

        ## Determine screen to show
        if currentScreen == 0: displayAllTimePlayerStats(screen, teamsAllTime, 5)
        #elif currentScreen == 1: displayGameStats()
        elif currentScreen == 1: displayAllTimeGoalieStats(screen, teamsAllTime, 5)
        #elif currentScreen == 3: displayGoalieGameStats()

        ## Render screen
        pygame.display.update()

def loadData(fileName):
        dataFile = open(fileName, "rU")
        dataArray = [line for line in dataFile]
        dataFile.close()

        teams = []
        currentTeam = -1
        players = 0
        maxTeamPlayers = 5

        for item in dataArray:
            if str(item)[0] != '-':
                currentTeam += 1
                newTeam = teamClass.Team(str(item).strip())
                teams.append(newTeam)

                if players > maxTeamPlayers:
                    maxTeamPlayers = players

                players = 0
            else:
                players += 1
                # (self, playerID, firstName, lastName, number, isGoalie=False)
                playerData = [part for part in item.strip().split(';')]

                # Remove minus sign
                playerData[0] = playerData[0][1:]

                # Set isGoalie flag
                if int(playerData[9]) == 0:
                    playerData[9] = False
                else:
                    playerData[9] = True

                newPlayer = playerClass.Player(playerData[0], playerData[1], playerData[2], int(playerData[3]), int(playerData[4]), int(playerData[5]), int(playerData[6]), int(playerData[7]), int(playerData[8]), int(playerData[9]), int(playerData[10]), int(playerData[11]), int(playerData[12]), int(playerData[13]), int(playerData[14]))
                # Assign to team
                teams[currentTeam].addPlayer(newPlayer)

        return teams, maxTeamPlayers

def getFontWidth(size, text="a"):
    pygame.font.init()
    return pygame.font.Font("Consolas.ttf", size).size(text)[0]

def getFontHeight(size, text="a"):
    pygame.font.init()
    return pygame.font.Font("Consolas.ttf", size).size(text)[1]

## Displays plain text on screen
## Used for debugging purposes only
def writeText(screen, text, location, size):
    ## Initialise font engine
    pygame.font.init()
    
    ## Define font and size
    ## Consolas width = 29
    font = pygame.font.Font("Consolas.ttf", size)

    ## Create screen object
    obj = font.render(text, 1, (255,0,0))

    ## Render text on screen
    screen.blit(obj, location)

def displayAllTimePlayerStats(screen, teamsAllTime, amount):
    amountOfPlayers = 0
    for team in teamsAllTime:
        for player in team.players:
            amountOfPlayers += 1

    ## Draw title
    titleText = "All Time Player Stats"
    xPos = WIDTH/2 - getFontWidth(ALLTIMEPTITLE, titleText)/2
    yPos = TOPPADDINGY/2/2 - getFontHeight(ALLTIMEPTITLE, titleText)/2
    writeText(screen, titleText, (xPos, yPos), ALLTIMEPTITLE)

    ## Draw rectangles
    x = 0
    maxName = 0

    allPlayers = []
    for team in teamsAllTime:
        for player in team.players:
            allPlayers.append(player)

    ## Sort players by points
    allPlayers.sort(key=operator.attrgetter('points'))
    allPlayers.reverse()
    allPlayers = allPlayers[:amount]

    for player in allPlayers:
        width = WIDTH - (PADDINGX*2)
        height = (HEIGHT - TOPPADDINGY - (PADDINGY*2))/amountOfPlayers
        left = PADDINGX
        top = TOPPADDINGY + (x*height)
        info = pygame.Rect(left, top, width, height)
        pygame.draw.rect(screen, (255, 0, 0), info, 3)
        x += 1

        sizeOfText = height - (2*STATPAD)

    ## Write stats
    titleY = TOPPADDINGY - height
    bottom = top + height
    ## Write Names
    x = 0
    for player in allPlayers:
        top = TOPPADDINGY + (x*height)

        initX = PADDINGX + 3 + 5
        initY = top + (height/2) - (sizeOfText/3)
        
        if x == 1:
            writeText(screen, "#  Name", (initX, titleY), sizeOfText)
        x += 1

        name = player.getFullName()
        if len(name) > maxName:
            maxName = len(name)
        writeText(screen, player.getFullName(), (initX, initY), sizeOfText)

    ## Draw vert
    pygame.draw.line(screen, (255, 0, 0), (initX + PADDINGX + (2*getFontWidth(sizeOfText)), titleY), (initX + PADDINGX + (2*getFontWidth(sizeOfText)), bottom), 1)
    ## Draw vert
    pygame.draw.line(screen, (255, 0, 0), (initX + PADDINGX + (maxName*getFontWidth(sizeOfText)), titleY), (initX + PADDINGX + (maxName*getFontWidth(sizeOfText)), bottom), 1) 

    ## Write Goals
    x = 0
    for player in allPlayers:
        newX = initX + PADDINGX + (maxName*getFontWidth(sizeOfText))
        top = TOPPADDINGY + (x*height)
        x += 1
        initY = top + (height/2) - (sizeOfText/3)

        if x == 1:
            writeText(screen, "G", (newX, titleY), sizeOfText)

        writeText(screen, str(player.goals), (newX, initY), sizeOfText)

    ## Write Assists
    initX = newX
    ## Draw vert
    pygame.draw.line(screen, (255, 0, 0), (initX + PADDINGX + (2*getFontWidth(sizeOfText)), titleY), (initX + PADDINGX + (2*getFontWidth(sizeOfText)), bottom), 1)
    x = 0
    for player in allPlayers:
        newX = initX + PADDINGX + (2*getFontWidth(sizeOfText))
        top = TOPPADDINGY + (x*height)
        x += 1
        initY = top + (height/2) - (sizeOfText/3)

        if x == 1:
            writeText(screen, "A", (newX, titleY), sizeOfText)

        writeText(screen, str(player.assists), (newX, initY), sizeOfText)

    ## Write Points
    initX = newX
    ## Draw vert
    pygame.draw.line(screen, (255, 0, 0), (initX + PADDINGX + (2*getFontWidth(sizeOfText)), titleY), (initX + PADDINGX + (2*getFontWidth(sizeOfText)), bottom), 1)
    x = 0
    for player in allPlayers:
        newX = initX + PADDINGX + (2*getFontWidth(sizeOfText))
        top = TOPPADDINGY + (x*height)
        x += 1
        initY = top + (height/2) - (sizeOfText/3)

        if x == 1:
            writeText(screen, "P", (newX, titleY), sizeOfText)

        writeText(screen, str(player.points), (newX, initY), sizeOfText)

def displayGameStats():
    pass

def displayAllTimeGoalieStats(screen, teamsAllTime, amount):
    amountOfPlayers = 0
    for team in teamsAllTime:
        for player in team.players:
            amountOfPlayers += 1

    ## Draw title
    titleText = "All Time Goalie Stats"
    xPos = WIDTH/2 - getFontWidth(ALLTIMEPTITLE, titleText)/2
    yPos = TOPPADDINGY/2/2 - getFontHeight(ALLTIMEPTITLE, titleText)/2
    writeText(screen, titleText, (xPos, yPos), ALLTIMEPTITLE)

    ## Draw rectangles
    x = 0
    maxName = 0

    allPlayers = []
    for team in teamsAllTime:
        for player in team.players:
            allPlayers.append(player)
    
    ## Sort players by points
    allPlayers.sort(key=operator.attrgetter('savePercentage'))
    allPlayers.reverse()
    allPlayers = allPlayers[:amount]

    for player in allPlayers:
        width = WIDTH - (PADDINGX*2)
        height = (HEIGHT - TOPPADDINGY - (PADDINGY*2))/amountOfPlayers
        left = PADDINGX
        top = TOPPADDINGY + (x*height)
        info = pygame.Rect(left, top, width, height)
        pygame.draw.rect(screen, (255, 0, 0), info, 3)
        x += 1

        sizeOfText = height - (2*STATPAD)

    ## Write stats
    titleY = TOPPADDINGY - height
    bottom = top + height
    ## Write Names
    x = 0
    for player in allPlayers:
        top = TOPPADDINGY + (x*height)

        initX = PADDINGX + 3 + 5
        initY = top + (height/2) - (sizeOfText/3)
        
        if x == 1:
            writeText(screen, "#  Name", (initX, titleY), sizeOfText)
        x += 1

        name = player.getFullName()
        if len(name) > maxName:
            maxName = len(name)
        writeText(screen, player.getFullName(), (initX, initY), sizeOfText)

    ## Draw vert
    pygame.draw.line(screen, (255, 0, 0), (initX + PADDINGX + (2*getFontWidth(sizeOfText)), titleY), (initX + PADDINGX + (2*getFontWidth(sizeOfText)), bottom), 1)
    ## Draw vert
    pygame.draw.line(screen, (255, 0, 0), (initX + PADDINGX + (maxName*getFontWidth(sizeOfText)), titleY), (initX + PADDINGX + (maxName*getFontWidth(sizeOfText)), bottom), 1) 

    ## Write Save Percentage
    x = 0
    for player in allPlayers:
        newX = initX + PADDINGX + (maxName*getFontWidth(sizeOfText))
        top = TOPPADDINGY + (x*height)
        x += 1
        initY = top + (height/2) - (sizeOfText/3)

        if x == 1:
            writeText(screen, "Save %", (newX, titleY), sizeOfText)

        writeText(screen, str(player.savePercentage), (newX, initY), sizeOfText)

def displayGoalieGameStats():
    pass

if __name__ == "__main__": main()