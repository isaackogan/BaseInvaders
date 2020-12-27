from BaseInvaders.resources.backgroundanims.load_anims import *
from random import choice
from math import floor


class BackgroundAnimation:
    def __init__(self):
        self.x = None
        self.y = None
        self.frame_position = 1.0
        self.frames = 0
        self.images = {}
        self.current_image = None
        self.change_amount = 1
        self.reset_position = 1

    def get_image(self):
        self.frame_position += self.change_amount

        if self.frame_position > self.frames:
            self.frame_position = self.reset_position

        # If whole, use me
        if float(self.frame_position).is_integer():
            self.current_image = self.images[int(self.frame_position)]

        # Else floor it (go to the lowest)
        else:
            self.current_image = self.images[int(floor(self.frame_position))]


class BunsenBurner(BackgroundAnimation):
    def __init__(self):
        BackgroundAnimation.__init__(self)
        self.images = bunsen_burner_images
        self.frames = len(self.images)
        self.x = 398
        self.y = 375
        self.change_amount = 0.5


class Microscope(BackgroundAnimation):
    def __init__(self):
        BackgroundAnimation.__init__(self)
        self.images = microscope_images
        self.frames = len(self.images)
        self.x = 186
        self.y = 443


class TestTubeRack(BackgroundAnimation):
    def __init__(self):
        BackgroundAnimation.__init__(self)
        self.images = sprinkler_images
        self.frames = len(self.images)
        self.x = choice([-12, -44, -76, 922, 954, 986])
        self.y = 383
        self.change_amount = 0.2


class LargeTestTube(BackgroundAnimation):
    def __init__(self):
        BackgroundAnimation.__init__(self)
        self.images = smoke_images
        self.frames = len(self.images)
        self.x = 732
        self.y = 370
        self.change_amount = 0.2
