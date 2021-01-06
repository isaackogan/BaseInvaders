from BaseInvaders.modules.characters import *
from BaseInvaders.modules.mainmenu.tutorialslides import Tutorial
from BaseInvaders.resources.sounds.load_sounds import *
from BaseInvaders.modules.mainmenu.statisticspage import MenuStatisticsPage
from BaseInvaders.resources.characters.load_characters import character_choices
from BaseInvaders.config import menu_screen_image, character_positions
from main import dis
import webbrowser


class MainMenu:
    """Menu Screen Class"""
    def __init__(self):
        """Initialize class attributes"""

        self.dis = dis                                      # Copy of display's memory address
        self.run_menu = True                                # Run menu boolean (True by default because we want to run the menu obviously)
        self.menu_background = menu_screen_image            # Background image

        self.buttons = [                                    # A list of buttons stored in memory
            PlayButton(),
            TutorialButton(),
            StatisticsButton(),
            CreditsButton(),
            ExitGameButton(),
            NextCharacterButton(),
            PreviousCharacterButton()
        ]

        self.statistics_page = MenuStatisticsPage()         # Initialize the statistics page to call back to later
        self.button_cooldown = 0                            # Set the button cooldown to 0 (we have a cooldown for buttons to stop double-clicks)
        self.character_choice = self.get_character()        # Set the default character choice to whatever is currently in the user's preferences
        self.character_image_scale = 1.7                    # Set the STATIC, hardcoded character image scale (1.7)

    def handle_events(self):
        """
        Handle all game events from within the loop

        MOUSEBUTTONDOWN + BUTTON -> Corresponding Action
        KEYDOWN + KEY -> Next character or Previous character (UP_ARROW = Forward, DOWN_ARROW = Backward, etc.)

        :return: No returns
        """

        # Get the event queue
        for event in pygame.event.get():

            # If the button cooldown iterator is greater than zero, reduce cooldown #
            if self.button_cooldown > 0: self.button_cooldown -= 1

            # On quit event, quit the game
            if event.type == pygame.QUIT:
                pygame.quit(), exit()

            # Run checks on mousebuttondown
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Check through the buttons

                for idx, button in enumerate(self.buttons):

                    # Check if button cooldown is > 0, if not, cancel
                    if self.button_cooldown > 0:
                        break

                    # If they don't collide with a button, continue to the next iteration & skip the rest of this iteration
                    if not self.mouse_on_button(button):
                        continue

                    # Since they're still here, they collided, so play the click sound & set the cooldown
                    pygame.mixer.Sound.play(sounds['button_click_sound'])
                    self.button_cooldown = 30

                    # PLAY Button
                    if idx == 0: self.run_menu = False

                    # TUTORIAL Button
                    if idx == 1:
                        Tutorial().run_menu()
                        set_music('menu_game_music')
                        pygame.mixer.music.play(-1)

                    # STATISTICS Button
                    if idx == 2: self.statistics_page.run_menu()

                    # CREDITS Button
                    if idx == 3: webbrowser.open('https://github.com/isaackogan/BaseInvaders', new=2)

                    # QUIT Button
                    if idx == 4: pygame.quit(), exit()

                    # CHANGE_CHARACTER FORWARD Button
                    if idx == 5: self.change_character('fwd')

                    # CHANGE_CHARACTER BACKWARD Button
                    if idx == 6: self.change_character('bwd')

            # If they click a key
            if event.type == pygame.KEYDOWN:

                # Set conditions
                keydown_conditions = {
                    'forward': event.key in [ord("w"), ord("d"), pygame.K_RIGHT, pygame.K_UP],
                    'backward': event.key in [ord("a"), ord("s"), pygame.K_LEFT, pygame.K_DOWN]
                }

                # If they meet any conditions, play the sound
                if any(keydown_conditions):
                    pygame.mixer.Sound.play(sounds['button_click_sound'])

                # Move forward/backward depending on which condition they met
                if keydown_conditions['forward']: self.change_character('fwd')
                if keydown_conditions['backward']: self.change_character('bwd')

    @staticmethod
    def mouse_on_button(button):
        """
        Check if the mouse is on the button via static method

        Actions:
            1. Get the mouse position
            2. Check if those mouse position overlaps with where the button is
            3. Return boolean based on whether or not it is

        :return (bool): Whether or not the mouse was on the button
        """

        mouse_x, mouse_y = pygame.mouse.get_pos()

        conditions = [
            button.button_x < mouse_x < (button.button_x + button.size[0]),
            button.button_y < mouse_y < (button.button_y + button.size[1])
        ]

        # Return True/False if all conditions are met
        return all(conditions)

    def draw_graphics(self):
        """
        Blit all items onto the display (all items are blitted here in the loop)
        :return: No returns
        """

        # Blit menu background onto display
        self.dis.blit(self.menu_background, (0, 0))

        # Iterate through the buttons & blit them onto the display
        for button in self.buttons:
            button_result = button.get_button(self.mouse_on_button(button))

            self.dis.blit(button_result[0], button_result[1])

        # Scale the character, calculate its location, and blit it into the display
        self.dis.blit(pygame.transform.smoothscale(
            self.get_character(),
            (
                round(self.character_choice.get_width() / self.character_image_scale),
                round(self.character_choice.get_height() / self.character_image_scale))
            ),
            self.get_character_pos()
        )

    @staticmethod
    def get_character_pos():
        """
        Get the position for the current character

        Actions:
            1. Open the json file
            2. See what the current character is
            3. Get the X, Y co-ords for that character
            4. Return the coordinates

        :return: Tuple of (X, Y) item coordinates in pixel values
        """

        # Open the json file & load the data into memory as a dictionary
        with open('./BaseInvaders/resources/user_data.json') as data:
            preferences = json.load(data)

        # Get the character preference
        character_choice = preferences.get('preferences').get('character')

        # Grab the corresponding character position
        character_position = character_positions[character_choice]

        # Return the Tuple
        return character_position

    @staticmethod
    def get_character():
        """
        Get the character image

        Actions:
            1. Load the json file
            2. See what the current character is
            3. Get the valid image for that character
            4. Return the image object

        :return: valid pygame.Image object to be displayed
        """

        # Open the json file & load the data into memory as a dictionary
        with open('./BaseInvaders/resources/user_data.json') as data:
            preferences = json.load(data)

        # Get the current character preference, return its image
        return character_choices[preferences.get('preferences').get('character')]

    def change_character(self, direction):
        """
        Change the character based on a selection of back and forward

        Actions:
            1. Get & match the character
            2. Increase/decrease depending on the direction chosen
            3. Overflow/Underflow if it is too small/too large
            4. Change the preference in the json file to the new preference at the id
            5. Get the new character choice (update the char attribute (Image Object) w/in the class)

        :param direction: 'fwd' or 'bwd' to move forward or backward
        :return: Returns nothing
        """

        # A list of options in which the user has picked one
        character_choice = [
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

        # Open the json file, load the data to memory
        with open('./BaseInvaders/resources/user_data.json') as data:
            preferences = json.load(data)

        # Get the current ID from preferences
        current_pref_id = character_choice.index(preferences['preferences']['character'])

        # If you click the forward button
        if direction == 'fwd':
            if current_pref_id + 1 < len(character_choice): current_pref_id += 1  # Move forward if you can
            else: current_pref_id = 0  # Set to 0 if you can't (overflow to beginning)

        # If you click the backward
        if direction == 'bwd':
            if current_pref_id - 1 >= 0: current_pref_id -= 1  # Move backward if you can
            else: current_pref_id = len(character_choice) - 1  # Set t0 len(character_choice) if you can't (underflow to end)

        # Edit the preference to the new selection
        preferences['preferences']['character'] = character_choice[current_pref_id]

        # Dump the new choice into the file/save
        with open('./BaseInvaders/resources/user_data.json', 'w') as file:
            json.dump(preferences, file)

        # Get the new character w/ self.character_choice
        self.character_choice = self.get_character()


class MenuButton:
    """Menu Button Class"""
    def __init__(self):
        """Set up the class attributes"""
        self.button_x = 680                             # Button X location
        self.button_y = 0                               # Button Y location

        self.font = None                                # Button font
        self.font_color = COLOR_WHITE                   # Button font colour
        self.font_color_dark = COLOR_WHITE_DARK         # Button font colour dark (no physical button, the button IS the text)
        self.text = None                                # Button text

    def get_button(self, mouse_button_collision=False):
        """
        Get the button

        Actions:
            1. Check if the mouse-button collision flag is True
            2. If it is, dark, else light
            3. Return the rendered font and the button location

        :param mouse_button_collision: (bool) -> True = Dark, False = Light
        :return: (Tuple) -> (valid pygame.Surface object of rendered text, (Tuple -> button x, button y))
        """

        # If the mouse is on the button, make it dark, otherwise it's light
        if mouse_button_collision: font_color = self.font_color_dark
        else: font_color = self.font_color

        # Return the rendered text, the button_x and button_y location
        return self.font.render(self.text, True, font_color), (self.button_x, self.button_y)


class PlayButton(MenuButton):
    """Play Button Class"""
    def __init__(self):
        MenuButton.__init__(self)                   # Initialize super class
        self.button_x = 690                         # Set button x
        self.button_y = 322                         # Set button y
        self.font = franklin_gothic_large_2         # Set button font
        self.text = "PLAY"                          # Set button text
        self.size = self.font.size(self.text)       # Calculate button size


class TutorialButton(MenuButton):
    """Play Button Class"""
    def __init__(self):
        MenuButton.__init__(self)                   # Initialize super class
        self.button_y = 555                         # Set button y
        self.font = franklin_gothic_medium_2        # Set button font
        self.text = "Tutorial"                      # Set button text
        self.size = self.font.size(self.text)       # Calculate button size


class StatisticsButton(MenuButton):
    """Statistics Button Class"""
    def __init__(self):
        MenuButton.__init__(self)                   # Initialize super class
        self.button_y = 625                         # Set button y
        self.font = franklin_gothic_medium_2        # Set button font
        self.text = "Statistics"                    # Set button text
        self.size = self.font.size(self.text)       # Calculate button size


class CreditsButton(MenuButton):
    """Credits Button Class"""
    def __init__(self):
        MenuButton.__init__(self)                   # Initialize super class
        self.button_y = 695                         # Set button y
        self.font = franklin_gothic_medium_2        # Set button font
        self.text = "Credits"                       # Set button text
        self.size = self.font.size(self.text)       # Calculate button size


class ExitGameButton(MenuButton):
    """Exit Game Button Class"""
    def __init__(self):
        MenuButton.__init__(self)                   # Initialize super class
        self.button_y = 765                         # Set button Y
        self.font = franklin_gothic_medium_2        # Set button font
        self.text = "Exit Game"                     # Set button text
        self.size = self.font.size(self.text)       # Calculate button size


class NextCharacterButton(MenuButton):
    """Next Character Button Class"""
    def __init__(self):
        MenuButton.__init__(self)                   # Initialize super class
        self.button_x = 455                         # Set button x
        self.button_y = 770                         # Set button y
        self.font = franklin_gothic_medium_2        # Set button font
        self.text = "Next"                          # Set button text
        self.size = self.font.size(self.text)       # Calculate button size


class PreviousCharacterButton(MenuButton):
    """Previous Character Button Class"""
    def __init__(self):
        MenuButton.__init__(self)                   # Initialize super class
        self.button_x = 220                         # Set button x
        self.button_y = 770                         # Set button y
        self.font = franklin_gothic_medium_2        # Set button font
        self.text = "Back"                          # Set button text
        self.size = self.font.size(self.text)       # Calculate button size


def run_start_menu(clock):
    """
    Run the start menu

    :param clock: The clock to tick
    :return: Return False (always, because it has to be false to stop the menu)
    """

    # Initialize the start menu class, set the music & set to play on a loop
    start_menu = MainMenu()
    set_music('menu_game_music')
    pygame.mixer.music.play(-1)

    # While the start menu run menu bool is true, run
    while start_menu.run_menu:
        start_menu.handle_events()      # Handle events
        start_menu.draw_graphics()      # Draw graphics
        pygame.display.flip()           # Update the display
        clock.tick(25)                  # Tick the display

    pygame.mixer.music.stop()           # Stop the music

    # Return False
    return start_menu.run_menu
