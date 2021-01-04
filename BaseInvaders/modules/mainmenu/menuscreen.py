from config import *
import pygame
from main import dis
import webbrowser
import sqlite3
import json
from BaseInvaders.modules.characters import *
from BaseInvaders.modules.mainmenu.tutorialslides import Tutorial


menu_screen_image = pygame.image.load('./BaseInvaders/resources/MenuScreen.png')
from BaseInvaders.modules.mainmenu.statisticspage import MenuStatisticsPage


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
            NextCharacterButton(),
            PreviousCharacterButton()
        ]
        self.statistics_page = MenuStatisticsPage()
        self.button_cooldown = 0
        self.character_choice = self.get_character()
        self.character_image_scale = 1.7

    def handle_events(self):
        for event in pygame.event.get():
            if self.button_cooldown > 0: self.button_cooldown -= 1
            if event.type == pygame.QUIT:
                pygame.quit(), exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.change_character(1)
                for idx, button in enumerate(self.buttons):
                    if self.button_collision(button):

                        if self.button_cooldown > 0:
                            break

                        self.button_cooldown = 30

                        # Play Button
                        if idx == 0:
                            self.run_menu = False
                        if idx == 1:
                            Tutorial().run_menu()
                        if idx == 2:
                            self.statistics_page.run_menu()
                        if idx == 3:
                            webbrowser.open('https://github.com/isaackogan/BaseInvaders', new=2)
                        if idx == 4:
                            pygame.quit(), exit()
                        if idx == 5:
                            self.change_character('fwd')
                        if idx == 6:
                            self.change_character('bwd')

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

        self.dis.blit(pygame.transform.smoothscale(
            self.get_character(),
            (
                round(self.character_choice.get_width() / self.character_image_scale),
                round(self.character_choice.get_height() / self.character_image_scale))
            ),
            self.get_character_pos()
        )

    def get_character_pos(self):
        character_position = {
            'standard_boy': (310, 437),
            'standard_girl': (255, 455),
            'zombie_boy': (280, 422),
            'zombie_girl': (232, 407),
            'ninja_boy': (320, 470),
            'ninja_girl': (295, 437),
            'cat_animal': (240, 450),
            'dog_animal': (239, 448),
            'adventure_boy': (290, 450),
            'adventure_girl': (222, 433),
        }

        with open('./BaseInvaders/resources/user_data.json') as data:
            preferences = json.load(data)

        character_choice = preferences.get('preferences').get('character')

        character_position = character_position[character_choice]

        return character_position

    def get_character(self):
        character_choices = {
            'standard_boy': pygame.image.load('./BaseInvaders/resources/characters/standard/boy/idle/Idle (1).png'),
            'standard_girl': pygame.image.load('./BaseInvaders/resources/characters/standard/girl/idle/Idle (1).png'),
            'zombie_boy':  pygame.image.load('./BaseInvaders/resources/characters/zombie/zombieboy/idle/Idle (1).png'),
            'zombie_girl':  pygame.image.load('./BaseInvaders/resources/characters/zombie/zombiegirl/idle/Idle (1).png'),
            'ninja_boy': pygame.image.load('./BaseInvaders/resources/characters/ninja/ninjaboy/idle/Idle__000.png'),
            'ninja_girl': pygame.image.load('./BaseInvaders/resources/characters/ninja/ninjagirl/idle/Idle__000.png'),
            'cat_animal': pygame.image.load('./BaseInvaders/resources/characters/animal/cat/idle/Idle (1).png'),
            'dog_animal': pygame.image.load('./BaseInvaders/resources/characters/animal/dog/idle/Idle (1).png'),
            'adventure_boy': pygame.image.load('./BaseInvaders/resources/characters/adventure/adventureboy/idle/Idle__000.png'),
            'adventure_girl': pygame.image.load('./BaseInvaders/resources/characters/adventure/adventuregirl/idle/Idle (1).png')
        }
        with open('./BaseInvaders/resources/user_data.json') as data:
            preferences = json.load(data)

        return character_choices[preferences.get('preferences').get('character')]

    def change_character(self, direction):
        character_choices = [
            'standard_boy',
            'standard_girl',
            'zombie_boy',
            'zombie_girl',
            'ninja_boy',
            'ninja_girl',
            'cat_animal',
            'dog_animal',
            'adventure_boy',
            'adventure_girl'
        ]

        with open('./BaseInvaders/resources/user_data.json') as data:
            preferences = json.load(data)
            current_pref_id = character_choices.index(preferences['preferences']['character'])

            if direction == 'fwd':
                if current_pref_id + 1 < len(character_choices):
                    current_pref_id += 1
                else:
                    current_pref_id = 0

            if direction == 'bwd':
                if current_pref_id - 1 >= 0:
                    current_pref_id -= 1
                else:
                    current_pref_id = len(character_choices) - 1

            preferences['preferences']['character'] = character_choices[current_pref_id]

        with open('./BaseInvaders/resources/user_data.json', 'w') as file:
            json.dump(preferences, file)

            print(current_pref_id)

        self.character_choice = self.get_character()


class MenuButton:
    def __init__(self):
        self.button_x = 680
        self.button_y = 0

        self.font = None
        self.font_color = COLOR_WHITE
        self.font_color_dark = COLOR_WHITE_DARK
        self.text = None

    def get_button(self, large=False):
        if large:
            font_color = self.font_color_dark
        else:
            font_color = self.font_color

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


class NextCharacterButton(MenuButton):
    def __init__(self):
        MenuButton.__init__(self)
        MenuButton.__init__(self)
        self.button_x = 455
        self.button_y = 770
        self.font = franklin_gothic_medium_2
        self.text = "Next"
        self.size = self.font.size(self.text)


class PreviousCharacterButton(MenuButton):
    def __init__(self):
        MenuButton.__init__(self)
        self.button_x = 220
        self.button_y = 770
        self.font = franklin_gothic_medium_2
        self.text = "Back"
        self.size = self.font.size(self.text)


def run_start_menu(clock):
    smenu = MenuScreen()

    while smenu.run_menu:
        smenu.handle_events()
        smenu.draw_graphics()
        pygame.display.flip()
        clock.tick(25)

    return smenu.run_menu
