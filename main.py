import sqlite3, json
from time import sleep
from config import *

from BaseInvaders.modules.resource_tools import parse_time

# Initialize PyGame
pygame.init()

# Set & create the display (used literally everywhere)
dis = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))


class GameLoader:
    def __init__(self):
        """
        Initialize the class attributes
        """
        pygame.display.set_icon(caption_image)
        self.connection, self.cursor = None, None
        self.percent_loaded = 0
        self.loading_bar_surface = None

    def load_game(self):
        """
        Load the game ("fake" but real loading screen)

        Run the load menu:
            1. Set the caption for the game based on the % loaded
            2. Increase progress bar via loading screen animation throughout loop & increase percent-loaded by 0.5 after each loop
            3. At 50%, load the main game resources
            4. At 75%, create the database if it doesn't exist and insert a null value to pull from in case they want to check statistics
            5. Throughout all of this update the display after each loop

        Sleep a second, set the caption to the permanent caption, and start the base_invaders() game function
        :return: No returns
        """
        while self.percent_loaded <= 100:

            # Add to the % loaded
            self.percent_loaded += 0.5

            # Handle Quit Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(), exit()

            # Loading Screen Graphics
            dis.blit(loading_screen_image, (0, 0))  # Blit the loading screen image
            dis.blit(self.get_loading_bar(), (330, 540))

            pygame.display.flip()

            # Set Game Caption Based on Load %
            pygame.display.set_caption(f"Base Invaders (Loading: {round((self.percent_loaded / 100) * 100)}%)")

            if self.percent_loaded == 50: from BaseInvaders.baseinvaders import base_invaders

            if self.percent_loaded == 75:
                self.connection = sqlite3.connect('./BaseInvaders/statistics.db')
                self.cursor = self.connection.cursor()

                try:
                    # Create Statistics Table for [Bases, XP, Level, Time, Data of Achievement]
                    self.cursor.execute("CREATE TABLE statistics (bases INTEGER, xp INTEGER, level INTEGER, time STRING, date STRING)")
                    self.cursor.execute(f"INSERT INTO statistics VALUES (:bases, :xp, :level, :time, :date)",
                                        {
                                            'bases': -100,
                                            'xp': -200,
                                            'level': -300,
                                            'time': parse_time(0),
                                            'date': "None"
                                        }
                                        )

                    self.cursor.connection.commit()

                    with open('BaseInvaders/resources/user_data.json') as data:
                        preferences = json.load(data)
                        preferences['first_game'], preferences['preferences']['character'] = "True", "standard_boy"

                    with open('BaseInvaders/resources/user_data.json', 'w') as file:
                        json.dump(preferences, file)

                # If a statistics database currently exists
                except sqlite3.OperationalError:
                    pass

                self.connection.close()

            # Update/flip the display
            pygame.display.flip()

        # Pause for a second, start the game & reset the caption
        sleep(1), pygame.display.set_caption("Base Invaders"), base_invaders()

    def get_loading_bar(self):
        """
        Get a loading bar for the loading screen

        Actions:
            1. Cap the % loaded display to 100 (stop from going off the screen)
            2. Calculate the # of pixels needed if the full pixel amount is 548 (% * pixel amount)
            3. Create a surface with the correct pixel amount, fill it blue and return the pygame.Surface object

        :return: Returns a valid pygame.Surface object (rectangular loading bar Surface)

        """

        capped_percent_loaded = 100 if self.percent_loaded > 100 else self.percent_loaded  # Lock the % loaded to 100 (how can you go past 100% after all)
        full_pixel_amount = 548  # Set constant value for the full # of pixels in a loading bar
        loaded_pixel_amount = round((capped_percent_loaded / 100) * full_pixel_amount)  # Calculate the # of pixels to load based on the % loaded

        self.loading_bar_surface = pygame.Surface((loaded_pixel_amount, 35))  # Create an empty surface object
        self.loading_bar_surface.fill(COLOR_LIGHT_BLUE)  # Fill the surface blue (our pseudo-rectangle object)

        return self.loading_bar_surface


if __name__ == '__main__':
    GameLoader().load_game()
