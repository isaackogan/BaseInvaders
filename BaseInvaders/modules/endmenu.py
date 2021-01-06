from main import dis
import sqlite3
from BaseInvaders.config import *
from BaseInvaders.resources.sounds.load_sounds import *


class EndGameMenu:
    """End of game Menu"""
    def __init__(self):
        """Initialize Class Attributes"""
        self.dis = dis                                              # Copy display memory address
        self.run_menu = True                                        # By default set the menu run bool to True

        self.statistics_data = self.get_statistics()                # GET THE STATISTICS - (:bases, :xp, :level, :time, :date)
        self.xp_high_score = self.get_statistics()[1]               # Gets high score

        self.button_text = "CONTINUE"                               # Text for the button
        self.button_font = franklin_gothic_large_3                  # Font for the button

        self.text_size = self.button_font.size(self.button_text)    # Text size for the text for the button

        self.button_width = 480                                     # Button width
        self.button_height = 130                                    # Button Height

        self.button_x = DISPLAY_X / 2 - self.button_width / 2       # X position of the button (centered on the screen)
        self.button_y = 725                                         # Y position of the button (hardcoded)

        self.button_text_light = COLOR_WHITE                        # Dark colour variant for text
        self.button_text_dark = COLOR_WHITE_DARK                    # Dark colour variant for text

        self.button_light = COLOR_WHITE_DARK                        # Light colour variant for button
        self.button_dark = COLOR_WHITE_SEMI_DARK_ALT                # Dark colour variant for button

        self.button_color = self.button_light                       # Current button colour
        self.button_text_color = self.button_text_light             # Current button text colour

    def handle_events(self):
        """
        Handle the events in the menu.

        Get the event queue and iterate through it.
            Quit -> Exit the game
            MOUSEBUTTONDOWN + mouse_on_button() -> Button click sound & stop the end-game menu
            KEYDOWN + K_SPACE/K_ESCAPE -> Stop the end-game menu

        :return: No returns
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), exit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.mouse_on_button():
                pygame.mixer.Sound.play(sounds['button_click_sound'])
                self.run_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                    self.run_menu = False

    def mouse_on_button(self):
        """Check if the mouse is on the button

        Actions:
            1. Get the mouse_x, mouse_y positions
            2. Check if the mouse location overlaps with the button location
            3. Return True/False whether or not all(conditions) are True

        :return: (bool) -> True/False whether or not the button overlaps with the mouse location
        """

        # Get mouse location
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Check conditions if X overlaps with mouse X and Y overlaps with mouse Y
        conditions = [
            self.button_x < mouse_x < (self.button_x + self.button_width),
            self.button_y < mouse_y < (self.button_y + self.button_height)
        ]

        # Return whether or not they both overlap
        return all(conditions)

    def get_button(self):
        """
        Get the button to be displayed

        Actions:
            1. Check if the mouse is on the button; if it is do the dark colour, if it isn't do the light colour
            2. Create a surface for the button & fill it appropriately with the selected colour
            3. Blit the text in the center of the button & return the button surface

        :return: valid pygame.Surface object (button with text on it)
        """

        # Update the button colour based on whether or not the mouse is on the button
        (self.button_color, self.button_text_color) = (self.button_dark, self.button_text_dark) if self.mouse_on_button() else (self.button_light, self.button_text_light)

        # Create the button surface & fill it with the appropriate calculated colour
        button_surface = pygame.Surface((self.button_width, self.button_height))
        button_surface.fill(self.button_color)

        # Blit the text onto the center of the button
        button_surface.blit(franklin_gothic_large_3.render(
            self.button_text, True, self.button_text_color), (self.button_width / 2 - self.text_size[0] / 2, self.button_height / 2 - self.text_size[1] / 2)
        )

        # Return the button Surface object
        return button_surface

    def display_graphics(self):
        """
        Display the graphics onto the screen

        Actions:
            1. Set a high score message based on whether or not the high score was achieved
            2. Display the end game menu image
            3. Blit the statistics onto the screen in fixed positions (statistics were calculated in the class constructor when it was called)
            4. Blit the button onto the screen

        :return: No return
        """

        # Set the high score message
        high_score_message = "- NEW BEST!" if (self.xp_high_score == self.statistics_data[1]) and (not self.statistics_data[1] == 0) else ""

        # Blit the end-game menu background image
        self.dis.blit(end_game_menu, (0, 0))

        # Blit the XP data
        self.dis.blit(franklin_gothic_small.render(f"{self.statistics_data[1]} XP {high_score_message}", True, COLOR_WHITE_SEMI_DARK), (375, 281))

        # Blit the Level data
        self.dis.blit(franklin_gothic_small.render(f"Lvl. {self.statistics_data[2]}", True, COLOR_WHITE_SEMI_DARK), (375, 401))

        # Blit the Bases data
        self.dis.blit(franklin_gothic_small.render(f"{self.statistics_data[0]} Bases", True, COLOR_WHITE_SEMI_DARK), (375, 521))

        # Blit the time survived data
        self.dis.blit(franklin_gothic_small.render(f"{self.statistics_data[3]}", True, COLOR_WHITE_SEMI_DARK), (375, 641))

        # Blit the button image
        self.dis.blit(self.get_button(), (self.button_x, self.button_y))

    @staticmethod
    def get_statistics(top=False):
        """
        Get the statistics

        Actions:
            1. Connect to the db, set up a cursor
            2. Get the needed statistics (all or top 1 depending on param "top")
            3. Dump the data into raw_data variable from the cursor
            4. Take only the last value
            5. Terminate connection & return data

        :param top: (bool) -> Retrieve the top statistic, or all statistics? True = Top, False = All
        :return: (list) -> list with tuples inside that contain the statistic values
        """

        # If we're looking to the top value, add an order by xp and limit to the top 1, otherwise, just grab all values
        extra = "ORDER BY xp DESC LIMIT 1" if top else ""

        # Connect to the Database
        connect = sqlite3.connect('./BaseInvaders/statistics.db')
        cursor = connect.cursor()

        # Retrieve entire leaderboard in memory (lol)
        cursor.execute(f"SELECT * FROM statistics {extra}")  # Select all values
        raw_data = cursor.fetchall()  # Fetch all values as a list with tuples inside that contain the values
        raw_data = raw_data[-1]  # Get the last value (the most recent, aka our value)

        # Terminate the connection
        connect.close()

        return raw_data


def run_end_menu():
    """
    Main function/loop to run the end menu

    Actions:
        1. Create class instance "end_menu"
        2. Run a while loop
            a) Handle events
            b) Display graphics
            c) Update the screen
        3. Return the result of end_menu.run_menu (always false)

    :return: (bool) False
    """

    # Create an instance of the end game class
    end_menu = EndGameMenu()

    # Run a while loop
    while end_menu.run_menu:

        # Handle events
        end_menu.handle_events()

        # Display graphics
        end_menu.display_graphics()

        # Flip the graphics
        pygame.display.flip()

    # Always returns false when it ends because false is required to stop the loop
    return end_menu.run_menu
