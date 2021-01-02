from config import *
import pygame
from BaseInvaders.modules.loadingscreen import loading_screen
from config import caption_image
import sqlite3
from time import sleep


pygame.init()

dis = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))


class RunBaseInvaders:
    def __init__(self):
        pygame.display.set_icon(caption_image)
        self.percent_loaded = 0
        self.connection = None
        self.cursor = None

    def load_game(self):
        while self.percent_loaded < 100:

            # Handle Quit Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(), exit()

            # Set Game Caption Based on Load %
            pygame.display.set_caption(f"Base Invaders (Loading: {round((self.percent_loaded / 100) * 100)}%)")
            self.percent_loaded += 0.5

            # Loading Screen Graphics
            loading_screen(dis, self.percent_loaded)

            if self.percent_loaded == 50: from BaseInvaders.baseinvaders import base_invaders

            if self.percent_loaded == 75:
                self.connection = sqlite3.connect('./BaseInvaders/statistics.db')
                self.cursor = self.connection.cursor()

                try:
                    # Create Statistics Table for [Bases, XP, Level, Time, Data of Achievement]
                    self.cursor.execute("CREATE TABLE statistics (bases INTEGER, xp INTEGER, level INTEGER, time STRING, date STRING)")
                    self.connection.commit()
                except sqlite3.OperationalError:
                    # If a statistics database currently exists
                    pass

                self.connection.close()

            pygame.display.flip()

        sleep(1)
        base_invaders()


if __name__ == '__main__':
    RunBaseInvaders().load_game()

