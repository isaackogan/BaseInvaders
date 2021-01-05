from BaseInvaders.modules.resourcetools import rounded_rectangle
import pygame
from config import *


class ScoreBoardItem:
    """Responsible for displaying scoreboard items (not calculating values in them)"""
    def __init__(self):
        self.rect_x, self.rect_y = 0, 36
        self.rect_width, self.rect_height = 267, 65

        self.text_x, self.text_y = 0, 0
        self.text_width, self.text_height = 0, 0

        self.border_thickness = 8
        self.rect_radius = 0.2
        self.border_radius = 0.35

        # Packaged Data
        self.border_data = None
        self.rect_data = None
        self.text_data = None
        self.completed_surface_data = None
        self.display_string = None

    def get_border(self):
        self.border_data = rounded_rectangle((0, 0, self.rect_width + (self.border_thickness * 2), self.rect_height + (self.border_thickness * 2)), COLOR_BURLYWOOD, self.border_radius)
        return self.border_data

    def get_rectangle(self):
        # Get the "main" rectangle
        self.rect_data = rounded_rectangle((0, 0, self.rect_width, self.rect_height), COLOR_TAN, self.rect_radius)

        # Get the border from the "main" rectangle
        border_surface = self.get_border()

        # Blit the main rectangle onto the border surface
        border_surface.blit(self.rect_data, (self.border_thickness, self.border_thickness))

        # Return the completed surface
        return border_surface

    def get_image(self):
        """Gets the completed image with text on rounded rectangle surface, returns"""
        # Get Rect
        self.completed_surface_data = self.get_rectangle()

        self.completed_surface_data.blit(self.get_text(), (self.text_x, self.text_y))
        return self.completed_surface_data

    def get_text(self):
        text_size = franklin_gothic_small.size(self.display_string)
        text = franklin_gothic_small.render(self.display_string, True, COLOR_BROWN)

        self.text_x = ((self.rect_width + (self.border_thickness * 2)) / 2) - (text_size[0] / 2)
        self.text_y = ((self.rect_height + (self.border_thickness * 2)) / 2 - (text_size[1] / 2))

        return text


class ScoreSB(ScoreBoardItem):
    def __init__(self):
        ScoreBoardItem.__init__(self)
        self.score_to_next_level = 5
        self.rect_x = 51

        self.display_string = "None"

    def set_display_string(self, value):
        self.display_string = f"{value[0]}/{value[1]} bp"

class LevelSB(ScoreBoardItem):
    def __init__(self):
        ScoreBoardItem.__init__(self)
        self.score = 0
        self.score_to_next_level = 5
        self.rect_x = 385

        self.display_string = "None"

    def set_display_string(self, value):
        self.display_string = f"Level {value}"


class ExperienceSB(ScoreBoardItem):
    def __init__(self):
        ScoreBoardItem.__init__(self)
        self.score = 5
        self.score_to_next_level = 5
        self.rect_x = 729

        self.xp = 0
        self.xp_increase = 10
        self.display_string = "None"

    def set_display_string(self, value):
        self.display_string = f"{('{:,}'.format(value))} XP"







