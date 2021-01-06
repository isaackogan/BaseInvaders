from random import choice, randint
from BaseInvaders.config import bases, ground, base_dimensions
from BaseInvaders.config import DISPLAY_X
import pygame


class Base:
    """'Base' Class"""
    def __init__(self):
        """Constructor for 'Base' class attributes"""
        # Loading Resources
        self.bases = bases                                          # Valid display locations for bases

        # Settings
        self.change_x = 1.2                                         # Change the x position by
        self.change_y = 1                                           # Change the y position by
        self.screen_width = DISPLAY_X                               # Width of the screen (for direction changes)

        # Initial Values (Hardcoded)
        self.remove_base = False                                    # Boolean for removing the base on remove event

        # Initial Values (Variable)
        self.direction = choice([True, False])                      # Random spawn direction
        self.type = choice(list(self.bases.keys()))                 # Random base type
        self.position_x = randint(50, self.screen_width - 50)       # Random spawn position @ X level
        self.position_y = -100                                      # Static spawn position @ Y level

    def handle_movement(self):
        """
        Handle the movement of the base by changing its
        x, y positions based on direction and de-spawning
        if it is lower than the ground. No returns.

        Actions:
            1a. Check the direction; if left move left, if right move right
            1b. If direction hits wall; bounce
            2. Move down constantly
            3. If hitting the ground queue the base's removal

        """

        # If Direction is Left
        if self.direction:
            self.position_x -= self.change_x  # Reduce x by change amount

            if self.position_x <= 0:  # If off the screen
                self.direction = not self.direction  # Switch directions

        # If Direction is Right
        if not self.direction:  # False = Right
            self.position_x += self.change_x  # Add to x by change amount

            if self.position_x > self.screen_width - base_dimensions[0]:  # If off the screen
                self.direction = not self.direction  # Switch directions

        # Move Down (Constant)
        self.position_y += self.change_y  # Move down

        # If hitting the ground
        if self.position_y + base_dimensions[1] >= ground:  # If hitting the ground
            self.remove_base = True  # Remove the base

    # Get a display surface of the base
    def get_image(self):
        """Return the current position of the base
        :return: A scale pygame surface for the base (image)
        """

        # Return scaled image at the requested state position
        return pygame.transform.scale(self.bases[self.type], base_dimensions)
