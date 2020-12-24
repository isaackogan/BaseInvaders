from config import *
from BaseInvaders.baseinvaders import *
import pygame

pygame.init()
dis = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))

if __name__ == '__main__':
    base_invaders()

