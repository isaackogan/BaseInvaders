from BaseInvaders.resources.backgroundanims.load_anims import *
from random import choice
from math import floor


class BackgroundAnimation:
    """Background animation Class"""
    def __init__(self):
        """Constructor for background animation class"""
        self.x = None                   # Default anim x position
        self.y = None                   # Default anim y position
        self.frame_position = 1.0       # Default position of the frame
        self.frames = 0                 # Default number of frames
        self.images = {}                # Empty library of frame images
        self.current_image = None       # Empty setting for current frame image
        self.change_amount = 1          # Amount to change the frames by
        self.reset_position = 1         # Position to reset the frames to

    def get_image(self):
        """
        Iterate through frame positions and get the resulting image + supports slower/faster iterations

        Actions:
            1. Increase frame position by change amount
            2. If the frame pos > frames for that objects, reset it to the reset position
            3. If the frame pos is an integer (whole number), use that frame position
            4. If the frame pos is not an integer (not a whole number, mid-position), always pick the floor (round down) whole number
            5. Update the image depending on the frame pos

        :return: No returns, just modifying class attributes
        """

        self.frame_position += self.change_amount
        if self.frame_position > self.frames: self.frame_position = self.reset_position

        # If whole, use me
        if float(self.frame_position).is_integer(): self.current_image = self.images[int(self.frame_position)]

        # Else floor it (go to the lowest)
        else: self.current_image = self.images[int(floor(self.frame_position))]


class BunsenBurner(BackgroundAnimation):
    """Bunsen Burner animation"""
    def __init__(self):
        BackgroundAnimation.__init__(self)      # Initialize super class
        self.images = bunsen_burner_images      # Get the images from the loaded dictionary
        self.frames = len(self.images)          # Get the # of frames in the dict
        self.x = 398                            # Set X-position override
        self.y = 375                            # Set Y-position override
        self.change_amount = 0.5                # Set change-amount override


class Microscope(BackgroundAnimation):
    """Microscope Animation"""
    def __init__(self):
        BackgroundAnimation.__init__(self)      # Initialize super class
        self.images = microscope_images         # Get the images from the loaded dictionary
        self.frames = len(self.images)          # Get the # of frames in the dict
        self.x = 186                            # Set X-position override
        self.y = 443                            # Set Y-position override


class TestTubeRack(BackgroundAnimation):
    """Test tube animation"""
    def __init__(self):
        BackgroundAnimation.__init__(self)                  # Initialize super class
        self.images = sprinkler_images                      # Get the images from the loaded dictionary
        self.frames = len(self.images)                      # Get the # of frames in the dict
        self.x = choice([-12, -44, -76, 922, 954, 986])     # Set X-position override
        self.y = 383                                        # Set Y-position override
        self.change_amount = 0.2                            # Set change-amount override


class LargeTestTube(BackgroundAnimation):
    """Large test tube animation"""
    def __init__(self):
        BackgroundAnimation.__init__(self)      # Initialize super class
        self.images = smoke_images              # Get the images from the loaded dictionary
        self.frames = len(self.images)          # Get the # of frames in the dict
        self.x = 732                            # Set X-position override
        self.y = 370                            # Set Y-position override
        self.change_amount = 0.2                # Set change-amount override
