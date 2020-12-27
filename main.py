from config import *
import pygame
from BaseInvaders.modules.loading_screen.loadingscreen import loading_screen

pygame.init()
dis = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
dis.fill((109, 135, 153))

if __name__ == '__main__':
    percent_loaded = 0
    while percent_loaded < 120:
        percent_loaded += 0.5
        loading_screen(dis, percent_loaded)

        if percent_loaded == 50:
            from BaseInvaders.baseinvaders import *


        pygame.display.flip()

    base_invaders()


