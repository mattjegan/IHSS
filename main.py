import pygame
from pygame.locals import *
import sys

from constants import *
import graphics
import processing

def main():
    running = True

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Calculate stats

        # Display graphics
        graphics.draw(screen)

        pygame.display.update()

if __name__ == "__main__": main()