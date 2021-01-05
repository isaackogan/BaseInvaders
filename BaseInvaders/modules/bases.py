from random import choice, randint
from BaseInvaders.config import bases, ground, base_dimensions
from config import DISPLAY_X
import pygame


class Base:
    def __init__(self):
        # Loading Resources
        self.bases = bases                                          # Valid display locations for bases

        # Settings
        self.change_x = 1.2                                         # Change the x position by
        self.change_y = 1                                         # Change the y position by
        self.screen_width = DISPLAY_X                               # Width of the screen (for direction changes)

        # Initial Values (Hardcoded)
        self.state_pos = 1                                          # Initial position of image states
        self.remove_base = False                                    # Boolean for removing the base on remove event

        # Initial Values (Variable)
        self.direction = choice([True, False])                      # Random spawn direction
        self.type = choice(list(self.bases.keys()))                 # Random base type
        self.position_x = randint(50, self.screen_width - 50)       # Random spawn position @ X level
        self.position_y = -100

    def handle_movement(self):
        """
        Handle the movement of the base by changing its
        x, y positions based on direction and de-spawning
        if it is lower than the ground. No returns.
        """
        # If Direction is Left
        if self.direction:
            self.position_x -= self.change_x

            if self.position_x <= 0:
                self.direction = not self.direction

        # If Direction is Right
        if not self.direction:  # False = Right
            self.position_x += self.change_x

            if self.position_x > self.screen_width - base_dimensions[0]:
                self.direction = not self.direction

        # Move Down (Constant)
        self.position_y += self.change_y

        # If hitting the ground
        if self.position_y + base_dimensions[1] >= ground:
            self.remove_base = True

    # Get a display surface of the base
    def get_image(self, increment=True):
        """Return the current position of the base
        :return: A scale pygame surface for the base (image)
        """
        # Increment the state position of the object's animation if requested
        if increment and (self.state_pos > len(self.bases[self.type])):
            self.state_pos = 1

        # Return scaled image at the requested state position
        return pygame.transform.scale(self.bases[self.type][self.state_pos], base_dimensions)
