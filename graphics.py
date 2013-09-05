import pygame
from pygame.locals import *
import sys

from constants import *

def draw(screen, statsArr):
    drawBG(screen)
    ##drawHeader(screen)
    drawGrid(screen, statsArr)
    drawStats(screen, statsArr)

def drawBG(screen):
    screen.fill(BLUE)

def drawHeader(screen):
    pass

def drawGrid(screen, statsArr):

    maxRows = len(statsArr)
    boxHeight = (SCREEN_HEIGHT-HEAD_PADDING-FOOT_PADDING)/maxRows

    for i in xrange(0, maxRows):
        pygame.draw.rect(screen, BLACK, (40, HEAD_PADDING + boxHeight * i, 1200, boxHeight), 5)

def drawStats(screen, statsArr):

    maxRows = len(statsArr)
    boxHeight = (SCREEN_HEIGHT-HEAD_PADDING-FOOT_PADDING)/maxRows
    textPosTop = boxHeight/4

    # Display name column
    for row in xrange(0, maxRows):
        writeText(screen, WHITE, str(statsArr[row][0]), (50, HEAD_PADDING + textPosTop + boxHeight * row), 45)

    # Display team column
    for row in xrange(0, maxRows):
        writeText(screen, WHITE, str(statsArr[row][1]), (250, HEAD_PADDING + textPosTop + boxHeight * row), 45)

    # Display score column
    for row in xrange(0, maxRows):
        writeText(screen, WHITE, str(statsArr[row][2]), (550, HEAD_PADDING + textPosTop + boxHeight * row), 45)

## Displays plain text on screen
## Used for debugging purposes only
def writeText(screen, color, text, location, size):
    ## Initialise font engine
    pygame.font.init()

    ## Define font and size
    font = pygame.font.Font(None, size)

    ## Create screen object
    obj = font.render(text, 1, color)

    ## Render text on screen
    screen.blit(obj, location)