import pygame
from pygame.locals import *
import sys

from constants import *

def draw(screen):
    drawBG(screen)
    ##drawHeader(screen)
    drawGrid(screen)
    drawStats(screen)

def drawBG(screen):
    screen.fill(BLUE)

def drawHeader(screen):
    pass

def drawGrid(screen):

    maxPlayer = 15
    boxHeight = (SCREEN_HEIGHT-HEAD_PADDING-FOOT_PADDING)/maxPlayer

    for i in xrange(0, maxPlayer):
        pygame.draw.rect(screen, BLACK, (40, HEAD_PADDING + boxHeight * i, 1200, boxHeight), 5)

def drawStats(screen):

    maxPlayer = 15
    boxHeight = (SCREEN_HEIGHT-HEAD_PADDING-FOOT_PADDING)/maxPlayer
    textPosTop = boxHeight/4

    for i in xrange(0, maxPlayer):
        writeText(screen, WHITE, "Matthew", (50, HEAD_PADDING + textPosTop + boxHeight * i), 45)

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