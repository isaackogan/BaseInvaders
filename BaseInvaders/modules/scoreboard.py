from BaseInvaders.modules.resource_tools import rounded_rectangle
from BaseInvaders.config import *


class ScoreBoardItem:
    """Responsible for displaying scoreboard items (not calculating values in them)"""
    def __init__(self):
        """
        Set attributes for the scoreboard item class (there is no 'centralized' scoreboard)
        """
        self.rect_x, self.rect_y = 0, 36                    # Set the default spawn location @ X & Y for the item
        self.rect_width, self.rect_height = 267, 65         # Set the default rectangle width and height for the item

        self.text_x, self.text_y = 0, 0                     # Set the default X & Y for the text in the item
        self.text_width, self.text_height = 0, 0            # Set the default width & height for the text in the item

        self.border_thickness = 8                           # Set the default thickness of the border
        self.rect_radius = 0.2                              # Set the default radius of the rectangle's curved corners
        self.border_radius = 0.35                           # Set the default radius of the rectangle's outer border corners

        # Packaged Data
        self.border_data = None                             # Data for the border rounded_rectangle
        self.rect_data = None                               # Data for the actual rounded_rectangle
        self.display_string = None                          # Data for the string to be displayed as text
        self.text_data = None                               # Data for the text Surface object
        self.completed_surface_data = None                  # Data for the completed surface to be blitting

    def get_border(self):
        """
        Get the border rectangle
        :return: pygame.Surface Object (Rounded Rectangle)
        """
        self.border_data = rounded_rectangle(   # rounded_rectangle pygame.Surface object (x, y, width, height, colour, curve radius)
            (0, 0, self.rect_width + (self.border_thickness * 2), self.rect_height + (self.border_thickness * 2)), COLOR_BURLYWOOD, self.border_radius
        )
        return self.border_data

    def get_rectangle(self):
        """
        Get the regular rectangle WITH the rounded rectangle on it

        Actions:
            1. Create the rectangle as rect_data
            2. Create the border rectangle
            3. Blit the regular rectangle onto the border rectangle backing to create a "border" outline
            4. Return the new surface

        :return: pygame.Surface Object (Rounded Rectangle w/ Rounded Rectangle border on the outside)
        """

        # Get the "main" rectangle - rounded_rectangle pygame.Surface object (x, y, width, height, colour, curve radius)
        self.rect_data = rounded_rectangle((0, 0, self.rect_width, self.rect_height), COLOR_TAN, self.rect_radius)

        # Get the border from the "main" rectangle
        border_surface = self.get_border()  # Get the border rounded rect

        # Blit the main rectangle onto the border surface
        border_surface.blit(self.rect_data, (self.border_thickness, self.border_thickness))

        # Return the completed surface
        return border_surface

    def get_image(self):
        """
        Gets the completed image with text on rounded rectangle surface, returns

        Actions:
            1. Get the rectangle w/ its border (pygame.Surface object)
            2. Get the text and blit it onto the completed rectangle surface
            3. Return it the completed surface

        :return: pygame.Surface Object (Rounded rectangle w/ rounded rectangle border on the outside w/ text draw in the center)
        """

        # Get Rect
        self.completed_surface_data = self.get_rectangle()

        self.completed_surface_data.blit(self.get_text(), (self.text_x, self.text_y))  # Blit the value of the text onto the completed surface
        return self.completed_surface_data

    def get_text(self):
        """
        Get the text to display on the scoreboard item

        Actions:
            1. Get the size based on the font & display string
            2. Get a pygame.Surface object by rendering the font
            3. Update text's the X & Y based on the details of the size
            4. Return the value

        :return: pygame.Surface Object (Rendered text)
        """

        text_size = franklin_gothic_small.size(self.display_string)  # Get the text size
        text = franklin_gothic_small.render(self.display_string, True, COLOR_BROWN)  # Get the text

        self.text_x = ((self.rect_width + (self.border_thickness * 2)) / 2) - (text_size[0] / 2)  # Get the text by centering in the item
        self.text_y = ((self.rect_height + (self.border_thickness * 2)) / 2 - (text_size[1] / 2))  # Get the text y by centering in the item

        return text


class ScoreSB(ScoreBoardItem):
    def __init__(self):
        """Initialize Score Scoreboard-Specific Values"""
        ScoreBoardItem.__init__(self)           # Initialized super class
        self.rect_x = 51                        # Set the hardcoded X value
        self.display_string = "None"            # Set the default display string to None

    def set_display_string(self, value):
        """
        Set the display string of the scoreboard

        :param value: The value to set it to (calculated elsewhere)
        :return: Return the string to the object (attribute inherited from ScoreBoardItem)
        """
        self.display_string = f"{value[0]}/{value[1]} bp"


class LevelSB(ScoreBoardItem):
    def __init__(self):
        """Initialize Level Scoreboard-Specific Values"""
        ScoreBoardItem.__init__(self)           # Initialized super class
        self.rect_x = 385                       # Set the hardcoded X value
        self.display_string = "None"            # Set the default display string to None

    def set_display_string(self, value):
        """
        Set the display string of the scoreboard

        :param value: The value to set it to (calculated elsewhere)
        :return: Return the string to the object (attribute inherited from ScoreBoardItem)
        """
        self.display_string = f"Level {value}"


class ExperienceSB(ScoreBoardItem):
    def __init__(self):
        """Initialize Experience Scoreboard-Specific Values"""
        ScoreBoardItem.__init__(self)           # Initialized super class
        self.rect_x = 729                       # Set the hardcoded X value
        self.display_string = "None"            # Set the default display string to None

    def set_display_string(self, value):
        """
        Set the display string of the scoreboard

        Actions:
            1. Get Value
            2. Format it with "," after every 3 zeroes
            3. Turn into XP string and update value

        :param value: The value to set it to (calculated elsewhere)
        :return: Return the string to the object (attribute inherited from ScoreBoardItem)
        """
        self.display_string = f"{('{:,}'.format(value))} XP"







