import pygame
from pygame.locals import *
import time
import sys
import playerClass
import teamClass

WIDTH = 1280
PADDINGX = 20
HEIGHT = 720
TOPPADDINGY = 100
PADDINGY = 20
STATPAD = 10

def main():
    pygame.init()

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
            currentScreen = currentScreen % 4 ## Make between range 0 -> 3 inclusive
            startTime = time.time()

        currentScreen = 0

        ## Determine screen to show
        if currentScreen == 0: displayAllTimePlayerStats(screen, teamsAllTime, maxTeamPlayers)
        elif currentScreen == 1: displayGameStats()
        elif currentScreen == 2: displayAllTimeGoalieStats()
        elif currentScreen == 3: displayGoalieGameStats()

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

## Displays plain text on screen
## Used for debugging purposes only
def writeText(screen, text, location, size):
    ## Initialise font engine
    pygame.font.init()

    ## Define font and size
    font = pygame.font.Font(None, size)

    ## Create screen object
    obj = font.render(text, 1, (255,0,0))

    ## Render text on screen
    screen.blit(obj, location)

def displayAllTimePlayerStats(screen, teamsAllTime, maxTeamPlayers):
    amountOfPlayers = 0
    for team in teamsAllTime:
        for player in team.players:
            amountOfPlayers += 1

    x = 0
    for team in teamsAllTime:
        for player in team.players:
            ## Draw rectangle
            width = WIDTH - (PADDINGX*2)
            height = (HEIGHT - TOPPADDINGY - (PADDINGY*2))/amountOfPlayers
            left = PADDINGX
            top = TOPPADDINGY + (x*height)
            info = pygame.Rect(left, top, width, height)
            pygame.draw.rect(screen, (255, 0, 0), info, 3)
            x += 1

            sizeOfText = height - (2*STATPAD)

            ## Write stats
            writeText(screen, player.saveData(False), (PADDINGX + 3 + 5, top + (height/2) - (sizeOfText/3)), sizeOfText)



def displayGameStats():
    pass

def displayAllTimeGoalieStats():
    pass

def displayGoalieGameStats():
    pass

if __name__ == "__main__": main()