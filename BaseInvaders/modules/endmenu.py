import pygame
from main import dis
import sqlite3
from BaseInvaders.config import *
from config import *
from BaseInvaders.modules.sounds import *

class EndGameMenu:
    def __init__(self):
        self.dis = dis
        self.run_menu = True
        self.position_x = 0
        self.position_y = 0

        self.statistics_data = self.get_statistics()  # (:bases, :xp, :level, :time, :date)
        self.xp_high_score = self.get_statistics(True)[1]  # Gets high score

        self.button_text = "CONTINUE"
        self.button_font = franklin_gothic_large_3

        self.text_size = self.button_font.size(self.button_text)

        self.button_width = 480
        self.button_height = 130

        self.button_x = DISPLAY_X / 2 - self.button_width / 2
        self.button_y = 725

        self.button_text_light = COLOR_WHITE
        self.button_text_dark = COLOR_WHITE_DARK

        self.button_light = COLOR_WHITE_DARK
        self.button_dark = COLOR_WHITE_SEMI_DARK_ALT

        self.button_color = self.button_light
        self.button_text_color = self.button_text_light

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.exit(), exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_on_button():
                    pygame.mixer.Sound.play(sounds['button_click_sound'])
                    self.run_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                    self.run_menu = False

    def mouse_on_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        conditions = [
            self.button_x < mouse_x < (self.button_x + self.button_width),
            self.button_y < mouse_y < (self.button_y + self.button_height)
        ]

        return all(conditions)

    def get_button(self):

        if not self.mouse_on_button():
            self.button_color = self.button_light
            self.button_text_color = self.button_text_light
        else:
            self.button_color = self.button_dark
            self.button_text_color = self.button_text_dark

        button_surface = pygame.Surface((self.button_width, self.button_height))
        button_surface.fill(self.button_color)

        button_surface.blit(franklin_gothic_large_3.render(self.button_text, True, self.button_text_color),
                            (self.button_width / 2 - self.text_size[0] / 2, self.button_height / 2 - self.text_size[1] / 2))

        return button_surface

    def display_graphics(self):
        self.dis.blit(end_game_menu, (0, 0))

        high_score_message = "- NEW BEST!" if (self.xp_high_score == self.statistics_data[1]) and (not self.statistics_data[1] == 0) else ""

        self.dis.blit(franklin_gothic_small.render(f"{self.statistics_data[1]} XP {high_score_message}", True, COLOR_WHITE_SEMI_DARK), (375, 281))
        self.dis.blit(franklin_gothic_small.render(f"Lvl. {self.statistics_data[2]}", True, COLOR_WHITE_SEMI_DARK), (375, 401))
        self.dis.blit(franklin_gothic_small.render(f"{self.statistics_data[0]} Bases", True, COLOR_WHITE_SEMI_DARK), (375, 521))
        self.dis.blit(franklin_gothic_small.render(f"{self.statistics_data[3]}", True, COLOR_WHITE_SEMI_DARK), (375, 641))

        self.dis.blit(self.get_button(), (self.button_x, self.button_y))

    def get_statistics(self, top=False):
        extra = "ORDER BY xp DESC LIMIT 1" if top else ""

        # Connect to the Database
        connect = sqlite3.connect('./BaseInvaders/statistics.db')
        cursor = connect.cursor()

        # Retrieve Leaderboard Top 10
        cursor.execute(f"SELECT * FROM statistics {extra}")
        raw_data = cursor.fetchall()
        raw_data = raw_data[-1]

        # Terminate the connection
        connect.close()

        return raw_data


def run_end_menu():
    emenu = EndGameMenu()

    while emenu.run_menu:
        emenu.handle_events()
        emenu.display_graphics()
        pygame.display.flip()

    return emenu.run_menu