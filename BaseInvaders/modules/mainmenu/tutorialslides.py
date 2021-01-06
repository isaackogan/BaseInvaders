from BaseInvaders.config import tutorial
from main import dis
from BaseInvaders.resources.sounds.load_sounds import *


class Tutorial:
    """Tutorial Class"""
    def __init__(self):
        """Initialize class attributes"""
        self.slide = 1              # Set the initial slide # value to 1 (obviously)
        self.slides = tutorial      # Get the dictionary of loaded slides
        self.stop_menu = False      # Set the stop menu value to False by default
        self.dis = dis              # Get a copy of the display's memory address

    def handle_events(self):
        """
        Handle game events

        QUIT -> Quit the game
        KEYDOWN -> Depending on the key(s), go forward, backward, or leave the menu
        MOUSEBUTTONDOWN -> Left click is forward slide, right click is backward slide

        Action:
            1. Limit the backwards movement to "1" and stop there.

        :return: No returns
        """

        # Get the event queue
        for event in pygame.event.get():

            # On quit event, quit the game
            if event.type == pygame.QUIT:
                pygame.quit(), quit()

            # On KEYDOWN event, run a number of checks
            if event.type == pygame.KEYDOWN:

                # Get a dictionary of possible conditions to be met
                keydown_conditions = {
                    'forward': event.key in [pygame.K_SPACE, ord("w"), ord("d"), pygame.K_UP, pygame.K_RIGHT],  # If they click SPACE, W, D, UP_ARROW, RIGHT_ARROW
                    'backward': event.key in [ord("a"), ord("s"), pygame.K_DOWN, pygame.K_LEFT],  # If they click A, S, DOWN_ARROW, LEFT_ARROW
                    'escape': event.key == pygame.K_ESCAPE  # If they click escape
                }

                # If any condition is met play the next slide sound
                if any(keydown_conditions): pygame.mixer.Sound.play(sounds['next_slide_sound'])

                # Change slide value based on condition result
                if keydown_conditions['forward']: self.slide += 1
                if keydown_conditions['backward']: self.slide -= 1
                if keydown_conditions['escape']: self.stop_menu = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown_conditions = {
                    'forward': event.button == 1,
                    'backward': event.button == 3
                }

                # If any condition is met play the next slide sound
                if any(mousebuttondown_conditions): pygame.mixer.Sound.play(sounds['next_slide_sound'])

                # Change slide value based on condition result
                if mousebuttondown_conditions['forward']: self.slide += 1
                if mousebuttondown_conditions['backward']: self.slide -= 1

        # Limit the slides to #1, never let it go to zero or lower (breaks the library as keys go from 1-len(library))
        if self.slide < 1: self.slide = 1

    def draw_graphics(self):
        """
        Draw the graphics on the screen if the slide # is valid
        or set the stop_menu attribute to True if it isn't and end
        the slideshow. No returns.
        """
        if self.slide > len(self.slides): self.stop_menu = True
        else: self.dis.blit(self.slides[self.slide], (0, 0))

    def run_menu(self):
        """
        Function to run the pause menu.

        Actions:
            1. Set the projector music to be the active track
            2. Play the music
            3. Start while loop

            While Loop:
                a) Handle events
                b) Draw graphics
                c) Update the display

            4. Stop the music

        :return: No returns
        """

        set_music('projector_sound_music')  # Set music
        pygame.mixer.music.play(-1)  # Play on loop forever

        # While the menu stop boolean is false, run actions
        while not self.stop_menu:
            self.handle_events()
            self.draw_graphics()
            pygame.display.flip()

        # Stop the music
        pygame.mixer.music.stop()
