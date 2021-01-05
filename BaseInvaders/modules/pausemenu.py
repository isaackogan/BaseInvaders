import pygame
from PIL import Image, ImageFilter, ImageEnhance
import os
from io import StringIO, BytesIO
from config import *
import webbrowser
from BaseInvaders.modules.resourcetools import rounded_rectangle
from main import dis
from BaseInvaders.modules.sounds import *


class PauseButton:
    """Responsible for displaying scoreboard items (not calculating values in them)"""
    def __init__(self):
        self.rect_x, self.rect_y = 1062, 36
        self.rect_width, self.rect_height = 70, 65

        self.text_x, self.text_y = 0, 0
        self.text_width, self.text_height = 0, 0

        self.border_thickness = 8
        self.rect_radius = 0.2
        self.border_radius = 0.35

        self.text = "II"
        self.font = franklin_gothic_medium

        self.rect_color = COLOR_TAN
        self.border_color = COLOR_BURLYWOOD
        self.text_color = COLOR_BROWN

        # Packaged Data
        self.border_data = None
        self.rect_data = None
        self.text_data = None
        self.completed_surface_data = None

    def mouse_on_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.rect_x - self.border_thickness < mouse_x < (self.rect_x + self.rect_width + (self.border_thickness * 2))) and \
                (self.rect_y - self.border_thickness < mouse_y < (self.rect_y + self.rect_height + (self.border_thickness * 2))):
            return True
        else:
            return False

    def get_border(self):
        self.border_data = rounded_rectangle((0, 0, self.rect_width + (self.border_thickness * 2), self.rect_height + (self.border_thickness * 2)), self.border_color, self.border_radius)
        return self.border_data

    def get_text_pos(self):
        size = self.font.size(self.text)
        return (self.rect_width / 2) - (size[0] / 2) + 8, (self.rect_height / 2) - (size[1] / 2) + 7

    def get_rectangle(self):
        # Get the colours
        if self.mouse_on_button():
            self.rect_color = COLOR_TAN_DARK
            self.border_color = COLOR_BURLYWOOD_DARK
            self.text_color = COLOR_BROWN_DARK
        else:
            self.rect_color = COLOR_TAN
            self.border_color = COLOR_BURLYWOOD
            self.text_color = COLOR_BROWN

        # Get the "main" rectangle
        self.rect_data = rounded_rectangle((0, 0, self.rect_width, self.rect_height), self.rect_color, self.rect_radius)

        # Get the border from the "main" rectangle
        border_surface = self.get_border()

        # Blit the main rectangle onto the border surface
        border_surface.blit(self.rect_data, (self.border_thickness, self.border_thickness))

        # Blit the text onto the border surface
        border_surface.blit(self.font.render(self.text, True, self.text_color), self.get_text_pos())

        # Return the completed surface
        return border_surface

    def get_image(self):
        """Gets the completed image with text on rounded rectangle surface, returns"""
        self.completed_surface_data = self.get_rectangle()

        #self.rect_data.blit(self.text_data, (self.text_x, self.text_y))
        return self.completed_surface_data


class PauseMenu:
    def __init__(self):
        self.dis = dis
        self.background = None

        self.stop_menu = False
        self.end_game = False

        self.buttons = {
            'resume_button': Resume(),
            'endgame_button': EndGame(),
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
                        pygame.mixer.Sound.play(sounds['button_click_sound'])
                        if self.buttons[button] == self.buttons['resume_button']:
                            self.stop_menu = True
                        if self.buttons[button] == self.buttons['endgame_button']:
                            self.end_game = True
                        if self.buttons[button] == self.buttons['credits_button']:
                            webbrowser.open('https://github.com/isaackogan/BaseInvaders', new=2)
                        if self.buttons[button] == self.buttons['quitgame_button']:
                            pygame.quit(), exit()

        self.highlight_buttons()

    def highlight_buttons(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in self.buttons:
            self.buttons[button].text_colour, self.buttons[button].button_colour = self.buttons[button].text_colour_light, self.buttons[button].button_colour_light

            if (self.buttons[button].button_x < mouse_x < (self.buttons[button].button_x + self.buttons[button].button_width)) and (self.buttons[button].button_y < mouse_y < (self.buttons[button].button_y + self.buttons[button].button_height)):
                self.buttons[button].text_colour, self.buttons[button].button_colour = self.buttons[button].text_colour_dark, self.buttons[button].button_colour_dark

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

    def run_menu(self):
        pygame.mixer.music.pause()
        display_copy = self.dis.copy()
        self.get_background(self.dis, 2)

        while True:

            self.handle_events()

            if self.end_game:
                return self.end_game

            self.dis.blit(self.background, (0, 0))

            for each in self.buttons:
                self.dis.blit(self.buttons[each].get_image(), (self.buttons[each].button_x, self.buttons[each].button_y))

            pygame.display.flip()

            if self.stop_menu:
                self.count_in(display_copy)

                # Reset the object & break
                self.__init__()
                pygame.mixer.music.unpause()
                break

    def count_in(self, copy):
        count, continue_loop, count_string = 0, True, None

        while continue_loop:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(), exit()
                if event.type == pygame.USEREVENT:
                    count += 0.01

                    self.dis.blit(copy, (0, 0))

                    if 0.5 < count < 1.0: count_string = "3"
                    if 1.0 < count < 1.5: count_string = "2"
                    if 1.5 < count < 2.0: count_string = "1"
                    if 2.0 < count:
                        continue_loop = False
                        break

                    # If there's a string to display (error locking)
                    if count_string is not None:
                        font_size = franklin_gothic_large.size(count_string)
                        self.dis.blit(franklin_gothic_large.render(count_string, True, COLOR_BGRD_BLUE_DARK), (DISPLAY_X / 2 - font_size[0] / 2, 150))

            pygame.display.flip()


class PauseMenuButtons:
    def __init__(self):
        self.button_width = 400
        self.button_height = 80
        self.button_y = 0
        self.text = "null"
        self.button_x = (DISPLAY_X / 2) - (self.button_width / 2)
        self.sub_surface = None

        self.button_colour_light = (COLOR_TAN)
        self.button_colour_dark = (COLOR_BURLYWOOD)
        self.text_colour_light = (242, 242, 242)
        self.text_colour_dark = (255, 255, 255)

        self.button_colour = self.button_colour_light
        self.text_colour = self.text_colour_light

    def create_surface(self):
        self.sub_surface = pygame.Surface((self.button_width, self.button_height))

    def get_text_location(self):
        """Returns text, position when centered"""
        return bahnschrift_font.size(self.text)

    def get_image(self):

        pygame.draw.rect(self.sub_surface, self.button_colour, pygame.Rect(0, 0, self.button_x, self.button_y))

        self.sub_surface.blit(bahnschrift_font.render(
            self.text, True, self.text_colour), (
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


class EndGame(PauseMenuButtons):
    def __init__(self):
        PauseMenuButtons.__init__(self)
        self.text = "End Game"
        self.create_surface()
        self.button_y = 415


class QuitGame(PauseMenuButtons):
    def __init__(self):
        PauseMenuButtons.__init__(self)
        self.text = "Close Game"
        self.create_surface()
        self.button_y = 515
