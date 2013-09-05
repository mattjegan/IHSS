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
    screen.fill(BG_COLOR)

def drawHeader(screen):
    pass

def drawGrid(screen, statsArr):

    maxRows = len(statsArr)
    boxHeight = (SCREEN_HEIGHT-HEAD_PADDING-FOOT_PADDING)/maxRows

    for i in xrange(0, maxRows):
        pygame.draw.rect(screen, GRID_COLOR, (GRID_SIDE_PADDING, HEAD_PADDING + boxHeight * i, GRID_WIDTH, boxHeight), GRID_BORDER)

def drawStats(screen, statsArr):

    maxRows = len(statsArr)
    boxHeight = (SCREEN_HEIGHT-HEAD_PADDING-FOOT_PADDING)/maxRows
    textSize = int(boxHeight/2)
    textPosTop = GRID_BORDER + (boxHeight-textSize)/2

    for col in xrange(0, len(statsArr[0])):
        # Display data
        for row in xrange(0, maxRows):
            writeText(screen, TEXT_COLOR, str(statsArr[row][col]), ((TEXT_SPACING*col) + TEXT_LEFT_PADDING, HEAD_PADDING + textPosTop + boxHeight * row), textSize)

## Displays plain text on screen
## Used for debugging purposes only
def writeText(screen, color, text, location, size):
    ## Initialise font engine
    pygame.font.init()

    ## Define font and size
    font = pygame.font.Font(None, size)

    ## Create screen object
    obj = font.render(text, True, color)

    ## Render text on screen
    screen.blit(obj, location)