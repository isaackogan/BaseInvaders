import pygame
from PIL import Image, ImageFilter, ImageEnhance
import os
from io import StringIO, BytesIO
from config import *
import webbrowser


class PauseMenu:
    def __init__(self):
        self.dis = None
        self.background = None

        self.stop_menu = False
        self.end_game = False

        self.buttons = {
            'resume_button': Resume(),
            'mainmenu_button': MainMenu(),
            'credits_button': Credits(),
            'quitgame_button': QuitGame()
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                    self.stop_menu = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for button in self.buttons:
                    if (self.buttons[button].button_x < mouse_x < (self.buttons[button].button_x + self.buttons[button].button_width)) and \
                            (self.buttons[button].button_y < mouse_y < (self.buttons[button].button_y + self.buttons[button].button_height)):
                        if self.buttons[button] == self.buttons['resume_button']:
                            self.stop_menu = True
                        if self.buttons[button] == self.buttons['mainmenu_button']:
                            self.end_game = True
                            print("End Game")
                        if self.buttons[button] == self.buttons['credits_button']:
                            webbrowser.open('https://github.com/isaackogan/BaseInvaders', new=2)

                        if self.buttons[button] == self.buttons['quitgame_button']:
                            pygame.quit(), exit()

        self.highlight_buttons()

    def highlight_buttons(self):
        pass

    def get_background(self, display, blur_amount):
        data = pygame.image.tostring(display, 'RGB')
        img = Image.frombytes("RGB", (DISPLAY_X, DISPLAY_Y), data)
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_amount))

        img = ImageEnhance.Brightness(img).enhance(0.7)
        path = "./BaseInvaders/resources/background.png"

        img.save(path)
        self.background = pygame.image.load(path)
        os.remove(path)
        return self.background

    def run_menu(self, display):
        self.dis = display
        self.get_background(display, 2)

        while True:

            self.handle_events()
            self.dis.blit(self.background, (0, 0))

            for each in self.buttons:
                self.dis.blit(self.buttons[each].get_image(), (self.buttons[each].button_x, self.buttons[each].button_y))

            pygame.display.flip()

            if self.stop_menu:
                self.__init__()
                break


class PauseMenuButtons:
    def __init__(self):
        self.button_width = 400
        self.button_height = 80
        self.button_y = 0
        self.text = "null"
        self.button_x = (DISPLAY_X / 2) - (self.button_width / 2)
        self.sub_surface = None

        self.button_colour = None
        self.highlight = False

    def create_surface(self):
        self.sub_surface = pygame.Surface((self.button_width, self.button_height))

    def get_text_location(self):
        """Returns text, position when centered"""
        return pause_menu_font.size(self.text)

    def get_image(self):
        if self.highlight:
            self.button_colour = COLOUR_BLACK
        if not self.highlight:
            self.button_colour = (COLOR_BURLYWOOD)

        pygame.draw.rect(self.sub_surface, self.button_colour, pygame.Rect(0, 0, self.button_x, self.button_y))

        self.sub_surface.blit(pause_menu_font.render(
            self.text, True, (242, 242, 242)), (
            (
                    self.button_width / 2) - (self.get_text_location()[0] / 2), (self.button_height / 2) - (self.get_text_location()[1] / 2)
        ))

        return self.sub_surface


class Resume(PauseMenuButtons):
    def __init__(self):
        PauseMenuButtons.__init__(self)
        self.text = "Resume Game"
        self.create_surface()
        self.button_y = 215


class Credits(PauseMenuButtons):
    def __init__(self):
        PauseMenuButtons.__init__(self)
        self.text = "Credits"
        self.create_surface()
        self.button_y = 315


class MainMenu(PauseMenuButtons):
    def __init__(self):
        PauseMenuButtons.__init__(self)
        self.text = "Main Menu"
        self.create_surface()
        self.button_y = 415


class QuitGame(PauseMenuButtons):
    def __init__(self):
        PauseMenuButtons.__init__(self)
        self.text = "Close Game"
        self.create_surface()
        self.button_y = 515
