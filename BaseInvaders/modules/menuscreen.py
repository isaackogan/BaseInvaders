from config import *
import pygame
from main import dis
import webbrowser

menu_screen_image = pygame.image.load('./BaseInvaders/resources/MenuScreen.png')


class MenuScreen:
    def __init__(self):
        self.dis = dis
        self.run_menu = True
        self.background = menu_screen_image
        self.buttons = [
            PlayButton(),
            TutorialButton(),
            StatisticsButton(),
            CreditsButton(),
            ExitGameButton(),
            EditCharacterButton()]
        self.return_to_menu = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for idx, button in enumerate(self.buttons):
                    if self.button_collision(button):
                        # Play Button
                        if idx == 0:
                            self.run_menu = False
                        if idx == 3:
                            webbrowser.open('https://github.com/isaackogan/BaseInvaders', new=2)
                        if idx == 4:
                            pygame.quit(), exit()

    def button_collision(self, button):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        conditions = [
            button.button_x < mouse_x < (button.button_x + button.size[0]),
            button.button_y < mouse_y < (button.button_y + button.size[1])
        ]

        # Return True/False if all conditions are met
        return all(conditions)

    def draw_graphics(self):

        self.dis.blit(self.background, (0, 0))

        for button in self.buttons:

            button_result = button.get_button(self.button_collision(button))

            self.dis.blit(button_result[0], button_result[1])


class MenuButton:
    def __init__(self):
        self.button_x = 680
        self.button_y = 0

        self.font = None
        self.font_color = COLOR_WHITE
        self.font_color_dark = COLOR_WHITE_DARK
        self.text = None

    def get_button(self, large=False):
        if large: font_color = self.font_color_dark
        else: font_color = self.font_color

        text = self.font.render(self.text, True, font_color)

        return text, (self.button_x, self.button_y)


class PlayButton(MenuButton):
    def __init__(self):
        MenuButton.__init__(self)
        self.button_x = 690
        self.button_y = 322
        self.font = franklin_gothic_large_2
        self.text = "PLAY"
        self.size = self.font.size(self.text)


class TutorialButton(MenuButton):
    def __init__(self):
        MenuButton.__init__(self)
        self.button_y = 555
        self.font = franklin_gothic_medium_2
        self.text = "Tutorial"
        self.size = self.font.size(self.text)


class StatisticsButton(MenuButton):
    def __init__(self):
        MenuButton.__init__(self)
        self.button_y = 625
        self.font = franklin_gothic_medium_2
        self.text = "Statistics"
        self.size = self.font.size(self.text)


class CreditsButton(MenuButton):
    def __init__(self):
        MenuButton.__init__(self)
        self.button_y = 695
        self.font = franklin_gothic_medium_2
        self.text = "Credits"
        self.size = self.font.size(self.text)


class ExitGameButton(MenuButton):
    def __init__(self):
        MenuButton.__init__(self)
        self.button_y = 765
        self.font = franklin_gothic_medium_2
        self.text = "Exit Game"
        self.size = self.font.size(self.text)


class EditCharacterButton(MenuButton):
    def __init__(self):
        MenuButton.__init__(self)
        self.button_x = 230
        self.button_y = 770
        self.font = franklin_gothic_medium_2
        self.text = "Edit Character"
        self.size = self.font.size(self.text)


def run_start_menu():
    smenu = MenuScreen()

    while smenu.run_menu:
        smenu.handle_events()
        smenu.draw_graphics()
        pygame.display.flip()

    return smenu.return_to_menu

