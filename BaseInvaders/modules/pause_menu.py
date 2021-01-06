from PIL import Image, ImageFilter, ImageEnhance
import os
from BaseInvaders.config import *
import webbrowser
from BaseInvaders.modules.resource_tools import rounded_rectangle
from main import dis
from BaseInvaders.resources.sounds.load_sounds import *
from config import *


class PauseButton:
    """Responsible for displaying scoreboard items (not calculating values in them)"""
    def __init__(self):
        """Get the default attributes for the Pause Button"""
        self.rect_x, self.rect_y = 1062, 36                 # X location of the pause button
        self.rect_width, self.rect_height = 70, 65          # Width of the pause button rectangle

        self.text_x, self.text_y = 0, 0                     # Where to display the text
        self.text_width, self.text_height = 0, 0            # Width and height of the text

        self.rect_radius = 0.2                              # Radius for the rounded rect
        self.border_radius = 0.35                           # Border radius for the rounded rect
        self.border_thickness = 8                           # Border thickness for the rounded rect

        self.text = "II"                                    # Physical text value
        self.font = franklin_gothic_medium                  # Font object passed in from config

        self.rect_color = COLOR_TAN                         # Colour of the rectangle
        self.border_color = COLOR_BURLYWOOD                 # Colour of the border
        self.text_color = COLOR_BROWN                       # Colour of the text

        # Packaged Data
        self.border_data = None                             # Border rounded_rect Surface Data
        self.rect_data = None                               # Rect rounded_rect Surface Data
        self.text_data = None                               # Text Surface Data
        self.completed_surface_data = None                  # Completed surface data (all 3 surfaces blitting onto one another)

    def mouse_on_button(self):
        """Check if the mouse is on the button

        Actions:
            1. Get the mouse position
            2. Check if those mouse position overlaps with where the button is
            3. Return boolean based on whether or not it is

        :return (bool): Whether or not the mouse was on the button

        """

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Check if the mouse coordinates are within the rectangle coordinates @ the X and Y
        mbn_conditions = [
            self.rect_x - self.border_thickness < mouse_x < (self.rect_x + self.rect_width + (self.border_thickness * 2)),
            self.rect_y - self.border_thickness < mouse_y < (self.rect_y + self.rect_height + (self.border_thickness * 2))
        ]

        # If they are, return True-- otherwise, return False
        if all(mbn_conditions): return True
        else: return False

    def get_border(self):
        """
        Get a pygame.Surface rounded rectangle border object

        :return: Valid pygame.Surface Object
        """
        # Create a rounded rectangle based on the described thickness.
        self.border_data = rounded_rectangle(
            (0, 0, self.rect_width + (self.border_thickness * 2), self.rect_height + (self.border_thickness * 2)), self.border_color, self.border_radius
        )
        return self.border_data

    def get_rectangle(self):
        """
        Get ta pygame.Surface rounded rectangle object w/ a border

        Actions:
            1. Check if the mouse is on the button & set the rectangles' colours based on that
            2. Get the regular rectangle Surface object
            3. Get the border surface object
            4. Blit the rectangle onto the border in the correct position and return the result

        :return: valid pygame.Surface object (rounded rect with rounded rect blitted on top)
        """

        # Get the colours for the rectangle based on whether or not the mouse is on the button when checking --> True = On, False = Off
        if self.mouse_on_button():
            self.rect_color = COLOR_TAN_DARK            # Highlight darker colour if mouse is on button
            self.border_color = COLOR_BURLYWOOD_DARK
            self.text_color = COLOR_BROWN_DARK
        else:
            self.rect_color = COLOR_TAN                 # Return to normal ambient light colour if not on button
            self.border_color = COLOR_BURLYWOOD
            self.text_color = COLOR_BROWN

        # Get the "main" rectangle
        self.rect_data = rounded_rectangle((0, 0, self.rect_width, self.rect_height), self.rect_color, self.rect_radius)

        # Get the border from the "main" rectangle
        border_surface = self.get_border()

        # Blit the main rectangle onto the border surface
        border_surface.blit(self.rect_data, (self.border_thickness, self.border_thickness))

        # Return the completed surface
        return border_surface

    def get_image(self):
        """
        Gets the completed image with text on rounded rectangle surface, returns

        Actions:
            1. Get the rounded rectangle (with the border behind it) surface
            2. Get the text size
            3. Get the position based off of the estimated text size
            4. Blit the text in the correct (centered) location on the button

        :return: valid pygame.Surface object with the text calculated and blitted onto the rectangle
        """
        self.completed_surface_data = self.get_rectangle()

        # Get the size for the text
        text_size = self.font.size(self.text)

        # Get the position for the text
        text_position = (self.rect_width / 2) - (text_size[0] / 2) + 8, (self.rect_height / 2) - (text_size[1] / 2) + 7

        # Blit the text onto the completed rectangle surface
        self.completed_surface_data.blit(self.font.render(self.text, True, self.text_color), text_position)

        return self.completed_surface_data


class PauseMenu:
    """Everything to do with the regular running of the Pause Menu"""
    def __init__(self):
        """Initialize class attributes & any embedded objects"""
        self.dis = dis                              # Display
        self.menu_background = None                 # The game background to blit buttons on top of
        self.stop_menu = False                      # Stop menu boolean (if true, stop the menu)
        self.end_game = False                       # Whether or not to end the game

        self.buttons = {                                            # Dictionary with all the button objects inside them.
            'resume_button': PauseMenuButton("Resume Game", 215),
            'endgame_button': PauseMenuButton("End Game", 415),
            'credits_button': PauseMenuButton("Credits", 315),      # (Display text, Y_coordinate)
            'quitgame_button': PauseMenuButton("Close Game", 515)
        }

        self.blur_amount = 2                        # How much to blur the screen background by

    def handle_events(self):
        """
        Handle events within the pause menu loop

        Quit -> Quit the game
        KEYDOWN + key.K_ESCAPE -> If they click the escape key, unpause
        MOUSEBUTTONDOWN -> If they click the mouse_button_down key, run an action
        highlight_buttons() -> Highlight buttons if the mouse is on top of them

        MOUSEBUTTONDOWN Actions:
            1. If resume button; resume
            2. If credits button; open project GitHub page in system browser
            3. If end game button; set the "end_game" class attribute to True
            4. If quit game button; close the game

        :return: No returns
        """

        # Get a list of all the events in the event queue
        for event in pygame.event.get():

            # If they click the QUIT button, exit the code
            if event.type == pygame.QUIT:
                pygame.quit(), quit()

            # If they click the KEYDOWN button and it's the escape button
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.stop_menu = True

            # If they click down on their button
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Iterate through all buttons
                for button in self.buttons:

                    # If the mouse is not on the currently iterated button, return.
                    if not self.mouse_on_button(button):
                        continue

                    # Play the button click sound
                    pygame.mixer.Sound.play(sounds['button_click_sound'])

                    # Run an action depending on the button ID we're on
                    if button == 'resume_button':
                        self.stop_menu = True  # Stop the menu
                    if button == 'endgame_button':
                        self.end_game = True  # End the game
                    if button == 'credits_button':
                        webbrowser.open('https://github.com/isaackogan/BaseInvaders', new=2)  # Open webpage
                    if button == 'quitgame_button':
                        pygame.quit(), exit()  # Close the code

        self.highlight_buttons()  # Highlight buttons if your mouse is over them

    def mouse_on_button(self, button):
        """
        Check if your mouse is on a button
        :param button: Button that your mouse is on

        Actions:
            1. Get the mouse x and y position
            2. Check if the mouse x and y overlap with the button's x and y
            3. Return a boolean (True/False) depending on whether or not the
               mouse meets both the x overlap and y overlap conditions

        :return (bool): True/False whether or not caller meets all specified conditions
        """

        # Get the mouse X & Y positions
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # The conditions to check for (whether or not the mouse is on the button) (mbn = mouse on button)
        mbn_conditions = [
            self.buttons[button].button_x < mouse_x < (self.buttons[button].button_x + self.buttons[button].button_width),
            self.buttons[button].button_y < mouse_y < (self.buttons[button].button_y + self.buttons[button].button_height)
        ]

        # Return a bool (True/False) whether or not all conditions are met
        return all(mbn_conditions)

    def highlight_buttons(self):
        """
        Highlight buttons if your mouse is on it

        Actions:
            1. Iterate through the buttons
            2. Set the button's colour to the light colour by default
            3. Check if the mouse is on the specified button
            4. If the mouse is on the specified button, override the button's colour to the dark version

        :return: No returns, only modified class attributes
        """

        # Iterate through all buttons in the dictionary
        for button in self.buttons:
            # Set the default colour to the light version w/ light text & a light rectangle
            self.buttons[button].text_colour = self.buttons[button].text_colour_light
            self.buttons[button].button_colour = self.buttons[button].button_colour_light

            # If the mouse isn't on the button continue to the next iteration
            if not self.mouse_on_button(button):
                continue

            # If we're here, the mouse was on the button and its colour should be set to the dark variant including its text & rectangle
            self.buttons[button].text_colour = self.buttons[button].text_colour_dark
            self.buttons[button].button_colour = self.buttons[button].button_colour_dark

    def get_background(self):
        """
        Create a background by displaying a blurred & darkened version of the current display

        Actions:
            1. Convert the screen to bytes holding the image's data
            2. Load the byte data into Pillow as a Pillow Image Object
            3. Apply a blur filter as well as enhance the brightness to *0.7 (70%) in order to darken
            4. Save the new image to disk
            5. Set the self.menu_background attribute to the Image object loaded in Pygame
            6. Delete the image from disk

        :return: Return the menu background Surface object
        """

        # Convert the current display into an image
        image_data = pygame.image.tostring(self.dis, 'RGB')  # Byte-string of the image data

        # Create a blurred Image object via the Pillow library
        pillow_image = Image.frombytes('RGB', (DISPLAY_X, DISPLAY_Y), image_data)  # Create a PIL image object from bytes w/ the DISPLAY_X, DISPLAY_Y size using image_data
        pillow_image = pillow_image.filter(ImageFilter.GaussianBlur(radius=self.blur_amount))  # Add a blur mask to the image (create the blur effect)
        pillow_image = ImageEnhance.Brightness(pillow_image).enhance(0.7)  # Set the brightness to 0.7 (70%), to make it darker

        # Convert the Pillow object to a real image & save it
        pillow_image_path = "./BaseInvaders/resources/pause_menu_background.png"
        pillow_image.save(pillow_image_path)

        # Set the menu background to the PyGame image object just saved by loading it from the path we just defined
        self.menu_background = pygame.image.load(pillow_image_path)

        # Remove the path & return the menu_background PyGame image object
        os.remove(pillow_image_path)
        return self.menu_background

    def run_menu(self):
        """
        Main loop to run the pause menu

        Actions:
            1. Pause all music, copy the display, get the blurred background
            2. While Loop while stop_menu is false
                a) Handle events
                b) If the end_game class attr. is true, return True to end the game
                c) Blit the blurred menu background
                d) Get the images of and then blit each button
                e) Update the display
            3. When stop_menu is false, run the count in function/loop
            4. Reset the object via self.__init__ and unpause any paused music

        :returns:
            None -> Nothing happens
            True -> Game will end upon returning to location of call
        """

        # Set the loop up
        pygame.mixer.music.pause()  # Pause any running music
        display_copy = self.dis.copy()  # Copy the display for the count in later
        self.get_background()  # Get the new background image

        # Menu Main Loop
        while not self.stop_menu:

            # Handle events + end the game if requested
            self.handle_events()
            if self.end_game: return self.end_game  # Early break

            # Display the Menu Background
            self.dis.blit(self.menu_background, (0, 0))  # Blit the menu background

            # Display the Buttons (get the button images then display them)
            for each in self.buttons:
                self.dis.blit(self.buttons[each].get_image(), (self.buttons[each].button_x, self.buttons[each].button_y))

            # Update the Display
            pygame.display.flip()

        # If a menu stop is requested perform menu stop actions
        self.count_in(display_copy)  # Give them a 3 second count in animation

        # Reset the object & break
        self.__init__()
        pygame.mixer.music.unpause()  # Unpause the music

    def count_in(self, copy):
        """
        Count back into the game
        :param copy: A copy of the current display

        Actions:
            1. Handle events:
                a) Quit -> Quit the game
                b) USEREVENT -> Add to the count in timer every 0.01 seconds
            2. Draw Graphics
                a) Draw background
                b) Get and draw count in decal
            3. Update display

        :return: No returns, just stop looping
        """

        count_in_timer, continue_loop, count_string = 0, True, None

        # Count-in loop
        while continue_loop:

            # Get Events
            for event in pygame.event.get():

                # If they click the quit button, quit
                if event.type == pygame.QUIT:
                    pygame.quit(), exit()

                # At every user event, add to the timer & perform actions
                if event.type == pygame.USEREVENT:
                    count_in_timer += 0.01

            # Draw Background
            self.dis.blit(copy, (0, 0))

            if 0.5 < count_in_timer < 1.0: count_string = "3"
            if 1.0 < count_in_timer < 1.5: count_string = "2"
            if 1.5 < count_in_timer < 2.0: count_string = "1"
            if 2.0 < count_in_timer: continue_loop = False

            # If there's a string to display (error locking)
            if count_string is not None:

                # Get the font size
                font_size = franklin_gothic_large.size(count_string)

                # Display the font in the center of the screen
                self.dis.blit(franklin_gothic_large.render(count_string, True, COLOR_BGRD_BLUE_DARK), (DISPLAY_X / 2 - font_size[0] / 2, 150))

            # Update the display
            pygame.display.flip()


class PauseMenuButton:
    """Pause Menu Button Class for the Pause Menu"""
    def __init__(self, text, button_y=0):
        """Set the (mostly static) class attributes

        :parameter text: (STR) Text to display
        :parameter button_y: (INT) Y-pixel-position of the button
        """
        self.button_width = 400                                         # Default button height 80
        self.button_height = 80                                         # Default button width 400

        self.button_y = button_y                                        # Default Y attribute to 0 (Will be overridden)
        self.text = text                                                # Set the default text to null
        self.button_x = (DISPLAY_X / 2) - (self.button_width / 2)       # Center the X position in the middle of the screen

        self.button_colour_light = COLOR_TAN                            # Light colour Button
        self.button_colour_dark = COLOR_BURLYWOOD                       # Dark colour Button
        self.text_colour_light = (242, 242, 242)                        # Light colour Text
        self.text_colour_dark = (255, 255, 255)                         # Dark colour Text

        self.button_colour = self.button_colour_light                   # Initial Button Colour
        self.text_colour = self.text_colour_light                       # Initial Text Colour

    def get_image(self):
        """
        Get the button image to display

        Actions:
            1. Create & fill an empty button surface
            2. Get the text size and render + blit the text onto the empty surface
            3. Return the completed surface

        :return: pygame.Surface object (completed button surface with text drawn)
        """

        # Create an empty button surface & fill it with the button's colour
        button_surface = pygame.Surface((self.button_width, self.button_height))
        button_surface.fill(self.button_colour)

        # Get the size estimate of the text for the font
        text_size = bahnschrift_font.size(self.text)

        # Blit the font onto the surface in the exact center based on its size
        button_surface.blit(bahnschrift_font.render(
            self.text, True, self.text_colour), (
            (
                    self.button_width / 2) - (text_size[0] / 2), (self.button_height / 2) - (text_size[1] / 2)
        ))

        # Return the completed surface
        return button_surface
