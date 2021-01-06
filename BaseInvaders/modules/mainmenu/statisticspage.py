from BaseInvaders.config import *
import sqlite3
from main import dis, DISPLAY_X
from BaseInvaders.config import bahnschrift_font_small, COLOR_WHITE, COLOR_WHITE_DARK, franklin_gothic_medium, COLOR_WHITE_SEMI_DARK_ALT
from BaseInvaders.resources.sounds.load_sounds import *


class MenuStatisticsPage:
    """Statistics Page Menu"""
    def __init__(self):
        """Class Constructor"""
        self.dis = dis                      # Copy of the display's memory address

        self.leaderboard_y = 220            # Leaderboard Y position

        self.lb_image_width = 0             # Image width
        self.lb_header_offset = 50          # Header offset for the category titles
        self.lb_image_height = 500          # Height of the leaderboard image

        self.lb_image_pos = -5              # Leaderboard image position
        self.stat_image_height = None       # Stat image height

        self.scroll_speed = 20              # Scroll speed (pixels per scroll event)
        self.stop_menu = False              # Stop menu bool (default false cause we want to run the menu)

        self.button_x = 300                 # X position of the back button
        self.button_y = 775                 # Y position of the back button

        self.button_width = 600             # Button width
        self.button_height = 100            # Button height

    def handle_events(self):
        """
        Handle statistics page events

        QUIT -> Quit the game
        MOUSEBUTTONDOWN + BUTTON4 -> Scroll Down
        MOUSEBUTTONDOWN + BUTTON5 -> Scroll Up
        MOUSEBUTTONDOWN + mouse_on_button() -> Escape menu (only 1 button so we cheat)
        KEYDOWN + K_ESCAPE -> Escape menu

        :return: No returns
        """

        # Get event queue
        for event in pygame.event.get():

            # On quit event, quit game
            if event.type == pygame.QUIT:
                pygame.quit(), quit()

            # On mouse button event, run checks
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Scroll Down
                if event.button == 4:
                    self.lb_image_pos = self.lb_image_pos + self.scroll_speed if (self.lb_image_pos + self.scroll_speed) < 0 else -5

                # Scroll Up
                elif event.button == 5:
                    if (self.lb_image_pos - self.scroll_speed) > (-1 * self.stat_image_height) + self.lb_image_height: self.lb_image_pos -= self.scroll_speed

                # Click Button
                if self.mouse_on_button():
                    pygame.mixer.Sound.play(sounds['button_click_sound'])  # Play button click sound
                    self.stop_menu = True  # Stop the menu

            # If they click the escape button, stop the menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.stop_menu = True

    def get_leaderboard(self):
        """
        Retrieve the leaderboard from the StatisticsLeaderboard class

        Actions:
            1. Create a blank w/ the size of DISPLAYABLE statistics
            (a box in which we want to display statistics INSIDE that
            doesn't exceed the bounds of the box
            2. Create an instance of the StatisticsLeaderboard class
            3. Grab the leaderboard image from the class (calculated there) + its width/height
            4. Define class attributes based off of the received heights
            5. Blit the image onto the lb_image surface (only allows whatever fits in there at the lb x position to be in the visible display)
            6. Return the Surface with our valid lb image

        :return: valid pygame.Surface object (leaderboard image)
        """

        # Create a surface
        lb_image = pygame.Surface((self.lb_image_width, self.lb_image_height), pygame.SRCALPHA, 32)
        lb_image = lb_image.convert_alpha()

        # Get the raw leaderboard image, image width and height
        leaderboard_instance = StatisticsLeaderboard()
        leaderboard_table = leaderboard_instance.create_leaderboard_table(leaderboard_instance.get_leaderboard())  # Gets LB image, LB image width, LB image height

        # Define class attributes based off what we got from the leaderboard
        self.stat_image_height = leaderboard_table[2]
        self.lb_image_width = leaderboard_table[1]

        # Blit the leaderboard image at its correct position (determined by scroll wheel) in the box. Only a certain part of the image will be in visible range
        lb_image.blit(leaderboard_table[0], (0, self.lb_image_pos))

        # Return the image
        return lb_image

    def display_graphics(self):
        """
        Display the graphics for the statistics page
        :return: No returns
        """

        # Blit the background
        self.dis.blit(statistics_menu, (0, 0))

        # Blit the leaderboard
        self.dis.blit(self.get_leaderboard(), (DISPLAY_X / 2 - self.lb_image_width / 2, self.leaderboard_y))

        # Set bold to True for this font (temporarily)
        bahnschrift_font_small.set_bold(True)

        # Blit the header items
        self.dis.blit(bahnschrift_font_small.render("Position", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2), self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("XP", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 150, self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("Level", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 300, self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("Bases", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 450, self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("Time", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 600, self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("Date", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 750, self.leaderboard_y - self.lb_header_offset))

        # Set bold to False for this font
        bahnschrift_font_small.set_bold(False)

        # Blit the button onto the display
        self.dis.blit(self.get_button(), (self.button_x, self.button_y))

    def run_menu(self):
        """
        Main loop for the menu.

        Actions:
            1. Run While Loop
            2. Reset the class with self.__init__

        While Loop:
            a) Handle events
            b) Display graphics
            c) Update the display

        :return:  No returns
        """

        while not self.stop_menu:
            self.handle_events()
            self.display_graphics()
            pygame.display.flip()

        self.__init__()

    def mouse_on_button(self):
        """
        Check if the mouse is on the button

        Actions:
            1. Get mouse pos
            2. Evaluate conditions based on mouse pos
            3. Return True/False whether or not all conditions are met

        :return: (bool) -> True if mouse is on button, False if mouse is not on button
        """

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Evaluate if mouse x & button x and mouse y & button y overlap
        conditions = [
            self.button_x < mouse_x < (self.button_x + self.button_width),
            self.button_y < mouse_y < (self.button_y + self.button_height)
        ]

        # Return bool of whether or not all conditions are met
        return all(conditions)

    def get_button(self):
        """
        Get a button with text blitted on it based off of whether or not a mouse is on it

        Actions:
            1. Create surface
            2. Set colour variables based on presence of mouse on button location
            3. Fill button with calculated colour
            4. Get text size & render + blit text onto the surface with calculated colour
            5. Return Surface object

        :return: valid pygame.Surface object (Button with text in its center)
        """

        # Create button surface based on its defined width & height
        button_surface = pygame.Surface((self.button_width, self.button_height))

        # Get the text & button colours
        button_color = COLOR_WHITE_SEMI_DARK_ALT if self.mouse_on_button() else COLOR_WHITE_DARK
        text_color = COLOR_WHITE_DARK if self.mouse_on_button() else COLOR_WHITE

        # Fill the button with the appropriate colour
        button_surface.fill(button_color)

        # Get the text size & blit the text onto the surface in its center with the calculated colour
        text_size = franklin_gothic_medium.size("Back")
        button_surface.blit(franklin_gothic_medium.render(
            "Back", True, text_color), (self.button_width / 2 - text_size[0] / 2, self.button_height / 2 - text_size[1] / 2)
        )

        # Return the Surface object
        return button_surface


class StatisticsLeaderboard:
    """Statistics Leaderboard Class"""
    def __init__(self):
        """Construct the class"""
        self.limit = max_leaderboard_number                 # Define statistic limit
        self.leaderboard_data = self.get_leaderboard()      # Retrieve the leaderboard data

    def get_leaderboard(self):
        """
        Get the leaderboard from the database

        Actions:
            1. Connect to database + define cursor
            2. Retrieve top X data sorted by XP
            3. Close connection
            4. Return raw data

        :return: List item with tuples inside it which contain values inside them for the leaderboard
        """

        # Connect to the Database
        connect = sqlite3.connect('./BaseInvaders/statistics.db')
        cursor = connect.cursor()

        # Retrieve Leaderboard Top 10
        cursor.execute(f"SELECT * FROM statistics ORDER BY xp DESC LIMIT {self.limit}")
        raw_data = cursor.fetchall()

        # Terminate the connection
        connect.close()

        # Return raw data
        return raw_data

    @staticmethod
    def create_leaderboard_table(dataset):
        """Create a leaderboard table image using a dataset

        Actions:
            1. Iterate through all data in memory
            2. Create table based on set values times the index of the value in the iteration (splits them up so they don't spawn on each other)
            3. When finished blitting, crop the image to the edge of the last date
            4. Return the finished image

        :param: List item with tuples inside it which contain values inside them for the leaderboard
        :return: valid pygame.Surface object, ready to be blitted!
        """

        # Set function attributes for the leaderboard
        image_height = 50*len(dataset) + 50
        text_surface = pygame.Surface((1500, image_height), pygame.SRCALPHA, 32)
        text_surface = text_surface.convert_alpha()
        lb_spacer = 40

        # List of dates
        dates = []

        # Parse leaderboard data to create strings based on the data given
        for idx, entry in enumerate(dataset):

            # Exclude data sets with "None" as the fourth value in the tuple
            if str(entry[4]) == "None":
                pass
            # Otherwise blit the following onto the text surface and append the date to a list to be used in calculations
            else:

                # Position
                text_surface.blit(bahnschrift_font_small.render(f"#{idx + 1}", True, COLOR_WHITE), (0, idx * lb_spacer))

                # XP
                text_surface.blit(bahnschrift_font_small.render(str(entry[1]), True, COLOR_WHITE), (150, idx * lb_spacer))

                # Level
                text_surface.blit(bahnschrift_font_small.render(str(entry[2]), True, COLOR_WHITE), (300, idx * lb_spacer))

                # Bases
                text_surface.blit(bahnschrift_font_small.render(str(entry[0]), True, COLOR_WHITE), (450, idx * lb_spacer))

                # Time
                text_surface.blit(bahnschrift_font_small.render(str(entry[3]), True, COLOR_WHITE), (600, idx * lb_spacer))

                # Date
                text_surface.blit(bahnschrift_font_small.render(str(entry[4]), True, COLOR_WHITE), (750, idx * lb_spacer))

                # Append the date to the dates entry to check the max length of the date & calculate its end to crop there
                dates.append(entry[4])

        # Try & Except Statement
        try:
            # Get the max date size and crop the image at the end of the pixel for that date (so we can center the image when it's returned to call)
            return text_surface, 750 + max([bahnschrift_font_small.size(date)[0] for date in dates]), image_height

        except ValueError:
            # If there are no dates (no values)
            return text_surface, 820, image_height
