from random import choice
from BaseInvaders.config import *
from BaseInvaders.modules.resourcetools import rot_center
from math import ceil

class LevelsSystem:
    def __init__(self):
        self.amount = 1
        self.bases = 0
        self.level = 1

    @staticmethod
    def bases_at_level(level):
        """Get Bases from Level"""
        return ceil(((level**2)/0.2) - 5)

    def update_level(self):
        needed = self.bases_at_level(self.level + 1)

        if self.bases >= needed:
            self.level += 1
            return True


class BaseObjective:
    def __init__(self):
        # Initial Values (Variable)
        self.objective = choice(list(bases.keys()))     # Pick a random new objective

        # Initial Values (Hardcoded)
        self.rotation = -90                             # Set the rotation to -90 (0 degrees relative to start of timer)
        self.size_iterator = 0                          # Set the size iterator to 0 by default

        # Settings
        self.state_pos = 1                              # Set the display state to 1 (filled with colour)
        self.position_x = 596                           # Set the default X position of the object
        self.position_y = ground + 103                  # Set the default Y position of the object

        # Timer
        self.time_per_base = 5
        self.time_left = self.time_per_base

    def new_base(self):
        """
        Get the old base, spawn a new base that is
        different from the old base and update the
        objective, rotation, and set the size iterator.
        """
        # Set the old/new values (for comparisons)
        old, new = self.objective, self.objective

        # Prevent the new base from being the same as the old (increase variation)
        while old == new: new = choice(list(bases.keys()))

        # Update the objective, reset the rotation, set the size iterator (inflate image for X frames as visual queue they got a new base)
        self.objective = new
        self.rotation = -90
        self.size_iterator = 30

    def get_image(self):
        """
        Get the valid image, resize it if the user just
        got a base objective point (feedback indicator),
        rotate the image based on the time left. No returns.
        """
        # Get the base image & assign its scale dimensions
        image, dimensions = bases[self.objective][self.state_pos], base_dimensions

        # If they just got a point, inflate the image size as visual feedback
        if self.size_iterator > 0:  # If the "size iterator" (# of frames for increase) is > 0, inflate the image
            self.size_iterator -= 1  # Reduce size iterator
            dimensions = (round(dimensions[0] * 1.2), round(dimensions[1] * 1.2))  # Change dimensions (inflate the image)

        # Get the rotation of the image
        self.rotation = self.get_rotation()

        # Scale the image to its appropriate dimension and rotate it accordingly
        image = rot_center(pygame.transform.smoothscale(image, dimensions), self.rotation - 90, self.position_x, self.position_y)  # "-90" rotates the position of 0 degrees to -90

        return image

    def get_rotation(self):
        return (self.time_left / self.time_per_base) * 360

    def handle_collisions(self, collided_base):
        """
        Determine if the collision was with the objective base,
        spawn a new base if it was and return True. Otherwise,
        return False and do nothing.
        """
        # Run a number of validity checks for collisions
        conditions = [
            self.objective == "cytosine" and collided_base == "guanine",
            self.objective == "guanine" and collided_base == "cytosine",
            self.objective == "adenine" and collided_base == "thymine",
            self.objective == "thymine" and collided_base == "adenine"
        ]

        # If no conditions simply return here
        if not any(conditions):
            return False

        # If conditions spawn new base and return True
        self.new_base()
        return True
