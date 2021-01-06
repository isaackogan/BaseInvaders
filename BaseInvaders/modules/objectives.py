from random import choice
from BaseInvaders.config import *
from BaseInvaders.modules.resource_tools import rot_center
from math import ceil


class LevelsSystem:
    """Level System Class used to get the level"""
    def __init__(self):
        self.bases = 0      # Number of bases captured
        self.level = 1      # Current Level (Default is 1)

    @staticmethod
    def bases_at_level(level):
        """Get Bases from Level

        :return: ceiling whole # value of the level based on a parabolic equation (i think it was parabolic, i forgot as of writing this docstring lol)"""
        return ceil(((level**2)/0.6) - 2)  # Calculate & Return (Old Equation in case this one breaks: ceil(((level ** 2) / 0.2) - 5))

    def update_level(self):
        """
        Update the level based on the # of bases achieved

        Actions:
            1. Calculate bases needed
            2. Check if current exceeds needed
            3. Change level if current exceeds needed & return True, else don't return anything

        :returns: True if the level changed, None (nothing) if it doesn't
        """

        # Check how many bases are needed at the next level
        needed = self.bases_at_level(self.level + 1)

        # Check if the # of bases exceeds or is equal to the # needed to level up
        if self.bases >= needed:
            self.level += 1  # Add a level
            return True


class BaseObjective:
    """Base Objective Class"""
    def __init__(self):
        """Set the default class attributes for the Base objective"""
        # Initial Values (Variable)
        self.objective = choice(list(bases.keys()))     # Pick a random new objective

        # Initial Values (Hardcoded)
        self.rotation = -90                             # Set the rotation to -90 (0 degrees relative to start of timer)
        self.size_iterator = 0                          # Set the size iterator to 0 by default

        # Settings
        self.position_x = 596                           # Set the default X position of the object
        self.position_y = ground + 103                  # Set the default Y position of the object

        # Timer
        self.time_per_base = 28                         # Amount of time to get each base (default, will be changed over time)
        self.time_left = self.time_per_base             # Amount of initial time left

    def new_base(self):
        """
        Get the old base, spawn a new base that is
        different from the old base and update the
        objective, rotation, and set the size iterator.

        Actions:
            1. Get the old base
            2. Create a new base until it isn't the same as the old one
            3. Update the attributes to reflect a new objective (means we don't need to re-initialize the objective tyo change it)

        :return: No returns
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

        Actions:
            1. Get the base and its scale
            2. Increase the size if they just got a point
            3. Continue on to get the rotation based on achieved/needed * 360 degrees in a circle
            4. Rotate the image according to the needed degrees around its center and scale it to the right size

        :return: Valid pygame.Image object (The rotated base)
        """
        # Get the base image & assign its scale dimensions
        image, dimensions = bases[self.objective], base_dimensions

        # If they just got a point, inflate the image size as visual feedback
        if self.size_iterator > 0:  # If the "size iterator" (# of frames for increase) is > 0, inflate the image
            self.size_iterator -= 1  # Reduce size iterator
            dimensions = (round(dimensions[0] * 1.2), round(dimensions[1] * 1.2))  # Change dimensions (inflate the image)

        # Get the rotation of the image - Get the fractional amount of time completed and multiply by 360 (360 degrees in a full circle)
        self.rotation = (self.time_left / self.time_per_base) * 360

        # Scale the image to its appropriate dimension and rotate it accordingly
        image = rot_center(pygame.transform.smoothscale(image, dimensions), self.rotation - 90, self.position_x, self.position_y)  # "-90" rotates the position of 0 degrees to -90

        return image

    def handle_collisions(self, collided_base):
        """
        Determine if the collision was with the objective base,
        spawn a new base if it was and return True. Otherwise,
        return False and do nothing.

        :param collided_base: The base that collided

        Actions:
            1. Depending on what collided with what determine
               whether or not it collided with the proper base
               for the objective.
            2. If it did, return True. If it didn't, return False.

        :returns (bool): Return True if the base collided with was the right one, False if it was the wrong one.

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
