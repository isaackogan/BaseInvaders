from BaseInvaders.config import *
from config import DISPLAY_X
from random import choice, randint
from math import floor


class Nuclease:
    def __init__(self):
        # Loading Resources
        self.states = nuclease                                          # Valid display locations for bases

        # Settings
        self.position_y = -100                                      # Spawn position @ Y level
        self.change_x = 2                                         # Change the x position by
        self.change_y = 3                                         # Change the y position by
        self.screen_width = DISPLAY_X                               # Width of the screen (for direction changes)

        # Initial Values (Hardcoded)
        self.state_pos = 1                                          # Initial position of image states
        self.state_change_amount = 0.5
        self.regen_nuclease = False                                    # Boolean for removing the base on remove event

        # Initial Values (Variable)
        self.direction = choice([True, False])                      # Random spawn direction
        self.position_x = randint(50, self.screen_width - 50)       # Random spawn position @ X level
        self.flip = True

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

            if self.position_x > self.screen_width - nuclease_dimensions[0]:
                self.direction = not self.direction

        # Move Down (Constant)
        self.position_y += self.change_y

        # If hitting the ground
        if self.position_y + nuclease_dimensions[1] >= ground:
            self.regen_nuclease = True

    # Get a display surface of the base
    def get_image(self, increment=True):
        """Return the current position of the base
        :return: A scale pygame surface for the base (image)
        """
        if self.flip:
            if self.state_pos < len(self.states): self.state_pos += self.state_change_amount
            else: self.flip = False
        if not self.flip:
            if self.state_pos > 1: self.state_pos -= self.state_change_amount
            else: self.flip = True

        # Return scaled image at the requested state position
        return pygame.transform.scale(self.states[floor(self.state_pos)], nuclease_dimensions)
