from BaseInvaders.config import *
from BaseInvaders.resources.characters.load_characters import *
from abc import ABCMeta, abstractmethod
from BaseInvaders.config import DISPLAY_X
import json


class Character:
    """Handler for all characters to control the image produced & movement"""
    def __init__(self):

        # Initial Values (Hardcoded)
        self.display_image = None               # Image being displayed (surface)
        self.offsets = {}                       # Character's offsets (based on the model/child class)
        self.state = ''                         # Character's movement state (based on the model/child class)
        self.hit_box = (0, 0, 0, 0)             # Character's hitbox (based on the model/child class)
        self.position_y = ground - 177          # Character's spawn location @ Y coordinate (based on the model/child class)
        self.direction = 'right'                # Character's initial direction
        self.flip_offset = 0                    # Character's flip offset (based on object's direction variable)
        self.screen_bound_offset_left = 0       # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 0      # Offset on right side of screen for character border
        self.pressed_keys = None                # All keys the player is currently pressing
        self.slide_iterator = 0
        self.moving = False

        # Settings (Hardcoded)
        __metaclass__ = ABCMeta                 # Let the meta know there's an abstract method in this class
        self.position_x = 50                    # Set the default spawn position @ X coordinate
        self.change_amount = 10                 # Set the default change amount (speed) of the character 10

        # Settings (Variable)
        self.screen_width = DISPLAY_X           # Get the screen width from config

    @staticmethod
    def set_character():
        """
        Static class method to set the character choice

        Actions:
            1. Initialize a copy of each character (very low-mem, so it doesn't matter)
            2. Load the json file and see what character is saved there
            3. Pick the character with the matching key from the json file in the choices
            4. Return the library key value at the json file selected character & discard other objects from memory

        :return: valid Character object (my own class!!)
        """
        character_choice = {
            'standard_boy': Boy(),
            'standard_girl': Girl(),
            'zombie_boy': ZombieBoy(),
            'zombie_girl': ZombieGirl(),
            'ninja_boy': NinjaBoy(),
            'ninja_girl': NinjaGirl(),
            'cat_animal': AnimalCat(),
            'dog_animal': AnimalDog(),
            'adventure_boy': AdventureBoy(),
            'adventure_girl': AdventureGirl()
        }

        with open('./BaseInvaders/resources/user_data.json') as data:
            preferences = json.load(data)

        character = preferences.get('preferences').get('character')

        return character_choice[character]

    def handle_movement(self):
        """
        Move the character based on the pressed keys,
        set the state based on movement (or lack thereof).

        Locks movement to X co-ords 0, screen width

        This method returns nothing and simply updates
        the attributes for the object itself + returns a bool value

        Actions:
            1. Get the pressed keys
            2. Check the keys
            3. Based on the keys' corresponding direction change the position & lock to screen + change state to running
            4. Return bool if successfully moved
            5. Otherwise return nothing and set state to idle


        :return: (bool) -> True = moving, None = not moving

        """

        # Get pressed keys
        self.pressed_keys = pygame.key.get_pressed()

        # If their pressed keys are "RIGHT ARROW" or "D", move accordingly
        if self.pressed_keys[pygame.K_RIGHT] or self.pressed_keys[ord('d')]:
            self.direction, self.state = 'right', 'run'                                                                 # Direction, state = right, run

            if not self.position_x + self.screen_bound_offset_right + self.change_amount < self.screen_width - 120:     # If the new position goes off right side of screen
                return

            self.position_x += self.change_amount                                               # Move right by the change amount (movement speed)
            return True

        # If their pressed keys are "LEFT ARROW" or "A", move accordingly
        if self.pressed_keys[pygame.K_LEFT] or self.pressed_keys[ord('a')]:
            self.direction, self.state = 'left', 'run'                                          # Direction, state = right, run

            if not self.position_x + self.screen_bound_offset_left + self.change_amount > 40:   # If the new position goes off left side of screen
                return

            self.position_x -= self.change_amount                                               # Move left by the change amount (movement speed)
            return True

        # If none of those are their pressed keys, set state to idle
        self.state = 'idle'
        return

    def update_image(self, increment_position=True):
        """
        Get the valid image for the user based on their state

        Actions:
            1. Get the current state
            2. Check direction, flip if left
        :return: No returns, only updates information within the object
        """
        # Get the current state
        if increment_position:
            self.get_state()

        # If the direction is right
        if self.direction == 'right':
            self.flip_offset = 0                                                        # Reset the X offset as there is no flipping
            return

        # If the direction is left
        self.display_image = pygame.transform.flip(self.display_image, True, False)     # Transform the image through pygame.transform
        self.flip_offset = self.offsets[self.state]                                     # Set the X offset due to image transformation

    @abstractmethod
    def get_state(self):
        """
        Abstract method to create valid value for get_state.
        In reality, we pull from the child class for this
        method, however this abstract method is provided to
        clarify that to the program reader."""
        pass

    def slide(self, slide_iterator):
        """
        Slide the user based on the value of the slide iterator (gets progressively slower)

        Actions:
            1. Check direction
            2. Check if movement goes off the screen, cancel if it does
            3. Move the user by 0.2 pixels * the iterator amount (2, 1.8, etc.)

        :param slide_iterator: value to multiply the hardcoded pixel amount by
        :return: No returns
        """

        if self.direction == 'right':
            if not self.position_x + self.screen_bound_offset_right + self.change_amount < self.screen_width - 120:     # If the new position goes off right side of screen
                return

            self.position_x += 0.2 * slide_iterator

        if self.direction == 'left':
            if not self.position_x + self.screen_bound_offset_left + self.change_amount > 40:  # If the new position goes off left side of screen
                return

            self.position_x -= 0.2 * slide_iterator


"""
 _____ _                  _               _ 
/  ___| |                | |             | |
\ `--.| |_ __ _ _ __   __| | __ _ _ __ __| |
 `--. \ __/ _` | '_ \ / _` |/ _` | '__/ _` |
/\__/ / || (_| | | | | (_| | (_| | | | (_| |
\____/ \__\__,_|_| |_|\__,_|\__,_|_|  \__,_|
                                            
"""


class Boy(Character):
    """Standard Boy Character"""
    def __init__(self):
        # Initialize Super class
        Character.__init__(self)                                                # Main "Character" parent class

        # Loading Resources
        self.states = boy_states                                                # Character's images in a dictionary w/ states as keys

        # Initial Values (Hardcoded)
        self.state_pos = 0                                                      # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                 # Default hitbox location values are none (specified on image call)

        # Settings (Hardcoded)
        self.state = 'idle'                                                     # Default state is idle when initialized
        self.offsets = {'idle': 122, 'run': 120, 'walk': 121, 'dead': 100}      # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y = ground - 177                                          # Set the default spawn position @ Y coordinate

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object
        """

        # Increment the states
        if increment:

            # If it's the final frame of the death animation, cancel
            if not (self.state == 'dead' and self.state_pos == len(self.states[self.state])):
                # Increment
                self.state_pos += 1

            # Set to first position if position > # of positions
            if self.state_pos > len(self.states[self.state]): self.state_pos = 1

        # Set the display image
        self.display_image = self.states[self.state][self.state_pos]

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x - (self.flip_offset / 9), self.position_y + 8, 110, 171)               # If Idle
        if self.state == 'run': self.hit_box = (self.position_x + 8 - (self.flip_offset / 3), self.position_y + 8, 120, 171)            # If running
        if self.state == 'dead': self.hit_box = (self.position_x + 34 - (self.flip_offset * 2.2), self.position_y + 78, 195, 101)       # If dead
        if self.state == 'walk': self.hit_box = (self.position_x - (self.flip_offset / 9), self.position_y + 8, 110, 171)               # If walk


class Girl(Character):
    """Standard Girl Character"""
    def __init__(self):
        Character.__init__(self)                                                # Initialize main "Character" parent class
        self.states = girl_states                                               # Character's images in a dictionary w/ states as keys
        self.state_pos = 0                                                      # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                 # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                     # Default state is idle when initialized
        self.offsets = {'idle': -20, 'run': -20, 'walk': 0, 'dead': 90}         # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y = ground - 149                                          # Set the default spawn position @ Y coordinate
        self.screen_bound_offset_left = 60                                      # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 47                                     # Offset on right hand side of screen for character border
        self.change_amount = 8                                                  # Movement speed override
        self.screen_bound_offset_left = 50       # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 10      # Offset on right side of screen for character border

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Speed is slowed down for the girl via "change_amount"
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state])):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]): self.state_pos = 1            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                        # Set the display image

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x + 15 - (self.flip_offset / 1.6), self.position_y, 115, 151)        # If Idle
        if self.state == 'run': self.hit_box = (self.position_x + 8 - (self.flip_offset / 1.6), self.position_y, 124, 151)          # If running
        if self.state == 'dead': self.hit_box = (self.position_x + 38 - (self.flip_offset / 1.6), self.position_y + 50, 174, 101)   # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x + 8 - (self.flip_offset / 1.6), self.position_y, 124, 151)         # If walking


r"""
______                _     _      
|___  /               | |   (_)     
   / /  ___  _ __ ___ | |__  _  ___ 
  / /  / _ \| '_ ` _ \| '_ \| |/ _ \
./ /__| (_) | | | | | | |_) | |  __/
\_____/\___/|_| |_| |_|_.__/|_|\___|                           
"""


class ZombieBoy(Character):
    """Standard Zombie Character (Male)"""
    def __init__(self):
        Character.__init__(self)                                                        # Initialize main "Character" parent class
        self.states = boy_zombie_states                                                 # Character's images in a dictionary w/ states as keys
        self.state_pos = 0                                                              # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                         # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                             # Default state is idle when initialized
        self.offsets = {'idle': 50, 'run': 50, 'walk': 50, 'dead': -45}                 # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y_init = ground - 168                                             # Set the default spawn position @ Y coordinate
        self.position_y = self.position_y_init                                          # Y position override for specific state
        self.screen_bound_offset_left = -15                                             # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 15                                             # Offset on left hand side of screen for character border
        self.change_amount = 10

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Ground is overridden for dead state due to bad image"
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state])):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]): self.state_pos = 1            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                        # Set the display image

        if self.state == 'dead': self.position_y = ground - 149                             # Override the Y position in the death state
        else: self.position_y = self.position_y_init

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x + 18 - (self.flip_offset / 1), self.position_y + 15, 109, 155)     # If Idle
        if self.state == 'run': self.hit_box = (self.position_x + 5 - (self.flip_offset / 1.5), self.position_y + 15, 114, 155)     # If running
        if self.state == 'dead': self.hit_box = (self.position_x + 30 - (self.flip_offset / 1.6), self.position_y + 65, 169, 86)    # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x + 5 - (self.flip_offset / 1.5), self.position_y + 15, 114, 155)    # If walking


class ZombieGirl(Character):
    """Standard Zombie Character (Girl)"""
    def __init__(self):
        Character.__init__(self)                                                        # Initialize main "Character" parent class
        self.states = girl_zombie_states                                                # Character's images in a dictionary w/ states as keys
        self.state_pos = 0                                                              # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                         # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                             # Default state is idle when initialized
        self.offsets = {'idle': 25, 'run': 25, 'walk': 50, 'dead': 55}                  # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y_init = ground - 186                                             # Set the default spawn position @ Y coordinate
        self.position_y = self.position_y_init                                          # Y position override for death state
        self.screen_bound_offset_left = 10                                              # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 40                                             # Offset on right hand side of screen for character border
        self.change_amount = 8                                                          # Character movement speed override

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Ground is overridden for dead state due to bad image"
        NOTE: X Change/Speed amount overridden
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state])):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]): self.state_pos = 1            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                        # Set the display image

        if self.state == 'dead': self.position_y = ground - 182                             # Override the Y position in the death state
        else: self.position_y = self.position_y_init

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x + 33 - (self.flip_offset / 0.7), self.position_y + 15, 119, 173)   # If Idle
        if self.state == 'run': self.hit_box = (self.position_x + 30 - (self.flip_offset / 0.8), self.position_y + 10, 122, 178)    # If running
        if self.state == 'dead': self.hit_box = (self.position_x + 33 - (self.flip_offset / 1.6), self.position_y + 65, 179, 119)   # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x + 30 - (self.flip_offset / 0.8), self.position_y + 10, 122, 178)   # If walking


"""
 _   _ _       _       
| \ | (_)     (_)      
|  \| |_ _ __  _  __ _ 
| . ` | | '_ \| |/ _` |
| |\  | | | | | | (_| |
\_| \_/_|_| |_| |\__,_|
             _/ |      
            |__/       
"""


class NinjaBoy(Character):
    """Standard Ninja Character (Male)"""
    def __init__(self):
        Character.__init__(self)                                                    # Initialize main "Character" parent class
        self.states = boy_ninja_states                                              # Character's images in a dictionary w/ states as keys
        self.state_pos = -1                                                         # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                     # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                         # Default state is idle when initialized
        self.offsets = {'idle': 0, 'run': 15, 'walk': 15, 'dead': 15}               # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y_init = ground - 156                                         # Set the default spawn position @ Y coordinate
        self.position_y = self.position_y_init                                      # Y position offset for death state
        self.screen_bound_offset_left = -6                                          # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 20                                         # Offset on left hand side of screen for character border
        self.change_amount = 12

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Iterator starts at 000 and goes to 009, -1 added to greater than calculation to start at 0 instead of 1
        NOTE: Ground is overridden for dead state due to bad image"
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state]) - 1):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]) - 1: self.state_pos = 0            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                            # Set the display image

        if self.state == 'dead': self.position_y = ground - 169                                 # Override the Y position in the death state
        else: self.position_y = self.position_y_init

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x - (self.flip_offset / 0.6), self.position_y, 89, 158)          # If Idle
        if self.state == 'run': self.hit_box = (self.position_x - (self.flip_offset / 0.7), self.position_y, 134, 158)          # If running
        if self.state == 'dead': self.hit_box = (self.position_x - (self.flip_offset / 1.6), self.position_y + 75, 164, 96)     # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x - (self.flip_offset / 0.7), self.position_y, 134, 158)         # If walking


class NinjaGirl(Character):
    """Standard Ninja Character (Girl)"""
    def __init__(self):
        Character.__init__(self)                                                        # Initialize main "Character" parent class
        self.states = girl_ninja_states                                                 # Character's images in a dictionary w/ states as keys
        self.state_pos = -1                                                             # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                         # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                             # Default state is idle when initialized
        self.offsets = {'idle': 15, 'run': 15, 'walk': 15, 'dead': 15}                  # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y_init = ground - 156                                             # Set the default spawn position @ Y coordinate
        self.position_y = self.position_y_init                                          # Y position override for death state
        self.screen_bound_offset_left = -6                                              # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 7                                              # Offset on right hand side of screen for character border

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Iterator starts at 000 and goes to 009, -1 added to greater than calculation to start at 0 instead of 1
        NOTE: Ground is overridden for dead state due to bad image"
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state]) - 1):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]) - 1: self.state_pos = 0            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                            # Set the display image

        if self.state == 'dead': self.position_y = ground - 169                                 # Override the Y position in the death state
        else: self.position_y = self.position_y_init

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x - (self.flip_offset / 0.8), self.position_y, 98, 158)          # If Idle
        if self.state == 'run': self.hit_box = (self.position_x - (self.flip_offset / 0.7), self.position_y, 124, 158)          # If running
        if self.state == 'dead': self.hit_box = (self.position_x - (self.flip_offset / 3.9), self.position_y + 75, 164, 96)     # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x - (self.flip_offset / 0.7), self.position_y, 124, 158)         # If walking


"""
  ___        _                 _ 
 / _ \      (_)               | |
/ /_\ \_ __  _ _ __ ___   __ _| |
|  _  | '_ \| | '_ ` _ \ / _` | |
| | | | | | | | | | | | | (_| | |
\_| |_/_| |_|_|_| |_| |_|\__,_|_|
"""


class AnimalCat(Character):
    """Standard Animal Character (Cat)"""
    def __init__(self):
        Character.__init__(self)                                                        # Initialize main "Character" parent class
        self.states = cat_animal_states                                                 # Character's images in a dictionary w/ states as keys
        self.state_pos = 0                                                              # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                         # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                             # Default state is idle when initialized
        self.offsets = {'idle': 10, 'run': 15, 'walk': 50, 'dead': -35}                 # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y_init = ground - 163                                             # Set the default spawn position @ Y coordinate
        self.position_y = self.position_y_init                                          # Y position override for death state (bad image)
        self.screen_bound_offset_left = 30                                              # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 50                                             # Offset on right hand side of screen for character border
        self.change_amount = 10                                                         # Character speed override

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Ground is overridden for dead state due to bad image"
        NOTE: X Change/Speed amount overridden
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state])):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]): self.state_pos = 1            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                        # Set the display image

        if self.state == 'dead': self.position_y = ground - 162                             # Override the Y position in the death state
        else: self.position_y = self.position_y_init

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x + 33 - (self.flip_offset / 30), self.position_y + 8, 115, 157)     # If Idle
        if self.state == 'run': self.hit_box = (self.position_x + 45 - (self.flip_offset / 0.6), self.position_y + 10, 116, 155)    # If running
        if self.state == 'dead': self.hit_box = (self.position_x + 44 - (self.flip_offset / 25), self.position_y + 48, 150, 116)    # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x + 30 - (self.flip_offset / 1.5), self.position_y + 6, 115, 158)    # If walking


class AnimalDog(Character):
    """Standard Animal Character (Dog)"""
    def __init__(self):
        Character.__init__(self)                                                        # Initialize main "Character" parent class
        self.states = dog_animal_states                                                 # Character's images in a dictionary w/ states as keys
        self.state_pos = 0                                                              # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                         # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                             # Default state is idle when initialized
        self.offsets = {'idle': 10, 'run': 15, 'walk': 50, 'dead': -15}                 # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y_init = ground - 165                                             # Set the default spawn position @ Y coordinate
        self.position_y = self.position_y_init                                          # Y position override for death state
        self.screen_bound_offset_left = 30                                              # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 50                                             # Offset on right hand side of screen for character border
        self.change_amount = 10                                                         # Character speed override

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Ground is overridden for dead state due to bad image"
        NOTE: X Change/Speed amount overridden
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state])):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]): self.state_pos = 1            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                        # Set the display image

        if self.state == 'dead': self.position_y = ground - 162                             # Override the Y position in the death state
        else: self.position_y = self.position_y_init

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x + 33 + (self.flip_offset / 5), self.position_y + 4, 115, 163)      # If Idle
        if self.state == 'run': self.hit_box = (self.position_x + 35 - (self.flip_offset / 1.1), self.position_y, 126, 167)         # If running
        if self.state == 'dead': self.hit_box = (self.position_x + 44 - (self.flip_offset / 25), self.position_y + 48, 155, 116)    # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x + 33 - (self.flip_offset / 1.5), self.position_y, 115, 167)        # If walking


"""
   _____       .___                    __                        
  /  _  \    __| _/__  __ ____   _____/  |_ __ _________   ____  
 /  /_\  \  / __ |\  \/ // __ \ /    \   __\  |  \_  __ \_/ __ \ 
/    |    \/ /_/ | \   /\  ___/|   |  \  | |  |  /|  | \/\  ___/ 
\____|__  /\____ |  \_/  \___  >___|  /__| |____/ |__|    \___  >
        \/      \/           \/     \/                        \/ 
"""


class AdventureBoy(Character):
    """Basic Boy Character"""
    def __init__(self):
        Character.__init__(self)                                                        # Initialize main "Character" parent class
        self.states = boy_adventure_states                                              # Character's images in a dictionary w/ states as keys
        self.state_pos = -1                                                             # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                         # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                             # Default state is idle when initialized
        self.offsets = {'idle': 15, 'run': 15, 'walk': 15, 'dead': 15}                  # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y_init = ground - 160                                             # Set the default spawn position @ Y coordinate
        self.position_y = self.position_y_init                                          # Y position override for death state
        self.screen_bound_offset_left = -12                                             # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 35                                             # Offset on right hand side of screen for character border
        self.change_amount = 12                                                         # Character speed override

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Iterator starts at 000 and goes to 009, -1 added to greater than calculation to start at 0 instead of 1
        NOTE: Ground is overridden for dead state due to bad image"
        NOTE: X Change/Speed amount overridden
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state]) - 1):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]) - 1: self.state_pos = 0            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                            # Set the display image

        if self.state == 'dead': self.position_y = ground - 169                                 # Override the Y position in the death state
        else: self.position_y = self.position_y_init

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x - (self.flip_offset / 0.9), self.position_y - 3, 108, 165)     # If Idle
        if self.state == 'run': self.hit_box = (self.position_x - (self.flip_offset / 0.8), self.position_y, 139, 162)          # If running
        if self.state == 'dead': self.hit_box = (self.position_x - (self.flip_offset / 3.9), self.position_y + 90, 178, 81)     # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x - (self.flip_offset / 0.8), self.position_y, 139, 162)         # If walking


class AdventureGirl(Character):
    """Basic Girl Character"""
    def __init__(self):
        Character.__init__(self)                                                        # Initialize main "Character" parent class
        self.states = girl_adventure_states                                             # Character's images in a dictionary w/ states as keys
        self.state_pos = 0                                                              # Default state position is 0 (incremented to 1 on first image call)
        self.hit_box = (None, None, None, None)                                         # Default hitbox location values are none (specified on image call)
        self.state = 'idle'                                                             # Default state is idle when initialized
        self.offsets = {'idle': 10, 'run': 15, 'walk': 50, 'dead': -15}                 # Default offsets for the character's hitbox on the X coordinate if flipped
        self.position_y_init = ground - 170                                             # Set the default spawn position @ Y coordinate
        self.position_y = self.position_y_init                                          # Y position override for death state
        self.screen_bound_offset_left = 20                                              # Offset on left hand side of screen for character border
        self.screen_bound_offset_right = 74                                             # Offset on right hand side of screen for character border
        self.change_amount = 12                                                         # Character speed override

    def get_state(self, increment=True):
        """Get the current state of the user and update internal values based on it,
        including their hitbox. Values are specific to each child class based on the images.

        :param increment: Whether or not to increment the state when calling
        :return: No returns, just updated info within the object

        NOTE: Ground is overridden for dead state due to bad image"
        NOTE: X Change/Speed amount overridden
        """

        if not (self.state == 'dead' and self.state_pos == len(self.states[self.state])):   # If it's the final frame of the death animation, cancel
            self.state_pos += 1  # Increment

            if self.state_pos > len(self.states[self.state]): self.state_pos = 1            # Set to first position if position > # of positions

        self.display_image = self.states[self.state][self.state_pos]                        # Set the display image

        if self.state == 'dead': self.position_y = ground - 162                             # Override the Y position in the death state
        else: self.position_y = self.position_y_init

        # Update the hitbox based on the state (hardcoded hitbox values)
        if self.state == 'idle': self.hit_box = (self.position_x + 33 + (self.flip_offset / 0.5), self.position_y + 4, 115, 168)    # If Idle
        if self.state == 'run': self.hit_box = (self.position_x + 35 - (self.flip_offset / 0.9), self.position_y + 4, 145, 168)     # If running
        if self.state == 'dead': self.hit_box = (self.position_x + 14 - (self.flip_offset / 0.9), self.position_y + 88, 174, 86)    # If Dead
        if self.state == 'walk': self.hit_box = (self.position_x + 35 - (self.flip_offset / 0.9), self.position_y + 4, 145, 168)    # If walking
