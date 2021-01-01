from config import *
import pygame
from BaseInvaders.modules.loading_screen.loadingscreen import loading_screen
from config import caption_image
import sqlite3
from time import sleep

pygame.init()

dis = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))

pygame.display.set_icon(caption_image)

if __name__ == '__main__':
    percent_loaded = 0

    while percent_loaded < 100:
        pygame.display.set_caption(f"Base Invaders (Loading: {round((percent_loaded / 100) * 100)}%)")
        percent_loaded += 0.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), exit()

        loading_screen(dis, percent_loaded)

        if percent_loaded == 50:
            from BaseInvaders.baseinvaders import *

        if percent_loaded == 75:
            """Create stats database if one doesn't exist"""
            connect = sqlite3.connect('./BaseInvaders/statistics.db')
            cursor = connect.cursor()

            try:
            # Create Statistics Table for [Bases, XP, Level, Time, Data of Achievement]
                cursor.execute("CREATE TABLE statistics (bases INTEGER, xp INTEGER, level INTEGER, time STRING, date STRING)")
                connect.commit()
            except sqlite3.OperationalError:
                pass

            connect.close()

        pygame.display.flip()

    sleep(1)
    base_invaders()

