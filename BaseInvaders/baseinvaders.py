# Importing Modules
from BaseInvaders.modules.background import BunsenBurner, LargeTestTube, Microscope, TestTubeRack
from BaseInvaders.modules.scoreboard import LevelSB, ScoreSB, ExperienceSB
from BaseInvaders.modules.objectives import BaseObjective, LevelsSystem
from BaseInvaders.modules.mainmenu.menuscreen import run_start_menu
from BaseInvaders.modules.pause_menu import PauseMenu, PauseButton
from BaseInvaders.modules.mainmenu.tutorialslides import Tutorial
from BaseInvaders.modules.resource_tools import parse_time
from BaseInvaders.modules.neucleases import Nuclease
from BaseInvaders.modules.endmenu import run_end_menu
from BaseInvaders.modules.characters import Character
from BaseInvaders.modules.bases import Base
from BaseInvaders.resources.sounds.load_sounds import *

# Importing Other Values/Libraries
from BaseInvaders.config import *
from main import dis
import json, time, random, sqlite3


class BaseInvaders:
    def __init__(self):
        """
        Initialize the class with its attributes
        """
        # Grabbing Values from config
        self.dis = dis                                                  # Grab the display surface from the main file

        # Null Values (Initializing)
        self.clock = None                                               # Clock for display update speed (FPS)
        self.objective = BaseObjective()                                # Objectives (The current base to go for)
        self.game_over = False, False                                   # Game Over (Whether or not to stop the game loop, what caused the game loop to end)
        self.current_background_animation = None                        # Current background animation

        # Time
        self.tick_speed = 30                                            # Tick speed for the clock
        self.general_timer = 0                                          # Set timer to 0
        self.base_timer = 0                                             # Set base timer to 0
        self.timer_time_left = 1                                        # Set base time left (time per base - base timer) to a non-zero value

        # Initializing Scoreboard
        self.scoreboards = {                                            # Set the scoreboards up (Experience, Score, Level)
            'experience_scoreboard': ExperienceSB(),
            'score_scoreboard': ScoreSB(),
            'levels_scoreboard': LevelSB()
        }

        # Initializing Character Information
        self.character = Character().set_character()                    # Set the default character (will be overridden later)
        self.pressed_keys = pygame.key.get_pressed()                    # Get the default keys pressed (will be overridden later)
        self.character_nuclease_collisions = 0                          # Number of times the character collides with the nuclease
        self.character_slide_iterator = 0                               # Number of frames to slide the user after walking

        # Initializing Base Information
        self.bases = []                                                 # A list of base objects
        self.last_spawn = Base()                                        # The last base which spawned
        self.base_spawnrate = 1.5                                       # How often they should spawn (seconds)

        # Initializing Pause Menu
        self.pause_menu = {                                             # Pause menu and attributes for it (in-game pause button, menu itself)
            'pause_menu': PauseMenu(),
            'pause_button': PauseButton()
        }

        # Initializing Game Statistics
        self.levelsystem = LevelsSystem()                               # Initialize the level system
        self.experience = 0                                             # Set the game XP
        self.xp_increase_amount = 10                                    # The amount the XP increases after getting a base

        # Nuclease Information
        self.nuclease_speed = [3, 4]                                    # The nuclease movement speed (Change by X, Change by Y) each time called
        self.nuclease_size_modifier = 1                                 # How big the nuclease should be (changes over time as level difficulty increases)
        self.nuclease = Nuclease(self.nuclease_speed)                   # Initialize the nuclease itself based on the speed it should run at

        # Initializing Sound Values
        self.klaxon_channel = pygame.mixer.Channel(1)                   # Set up the channel for the klaxon that blares when running out of time
        self.klaxon_sound = sounds['timer_alarm_sound']                 # Set up the sound to play on the klaxon channel (the alarm itself)

    def handle_events(self):
        """
        Handle the game events:

        quit -> Exit game
        USEREVENT -> Tick the timers & run timer-based events
        KEYDOWN (ESC) -> Pause the game
        MOUSEBUTTONDOWN (ON PAUSE BUTTON) -> Pause the game

        + Get values from events and calculate game updates based off them

        :return: No returns
        """

        # PYGAME EVENTS

        for event in pygame.event.get():

            # If they click the QUIT (X) Button
            if event.type == pygame.QUIT:
                pygame.quit(), exit()

            # On each user event (every 0.01 seconds)
            if event.type == pygame.USEREVENT:
                # Increase Timers, round their values to 2 decimal places (sometimes they can increase in odd amounts, this just locks any errors)
                self.general_timer = round(self.general_timer + 0.01, 2)
                self.base_timer = round(self.base_timer + 0.01, 2)
                self.timer_time_left = round(self.objective.time_per_base - self.base_timer, 2)

                # Handle all Timer/USEREVENT Based Events
                self.handle_timer_events()

                # Check if the game is over after the timer has been updated
                self.objective.time_left = round(self.objective.time_per_base - self.base_timer, 2)  # Time per base - the current stopwatch timer = Time left for the base
                if self.objective.time_left <= 0: self.game_over = True, True  # If they run out of time, end the game

            # On Keyboard Button Down event, run calculations (see pygame.key.get_pressed() for Character movement)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.pause_menu['pause_menu'].run_menu() is True: self.game_over = True, False   # Run the pause menu, if it returns "True," the user selected to end the game

            # On Mouse Button Down event, run calculations
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_menu['pause_button'].mouse_on_button():
                    pygame.mixer.Sound.play(sounds['button_click_sound'])
                    if self.pause_menu['pause_menu'].run_menu() is True: self.game_over = True, False  # Run the pause menu, if it returns "True," the user selected to end the game

        # CUSTOM EVENTS

        # Get the scoreboard values (NOTE: Calling these also updates the values with current data)
        self.scoreboards['score_scoreboard'].set_display_string(
            (
                self.levelsystem.bases - self.levelsystem.bases_at_level(self.levelsystem.level),
                self.levelsystem.bases_at_level(self.levelsystem.level + 1) - self.levelsystem.bases_at_level(self.levelsystem.level)
            )  # Get the value of the scoreboard based on the # of bases and the level (X bases needed at a certain level)
        )
        self.scoreboards['experience_scoreboard'].set_display_string(self.experience)  # Get the value of the scoreboard base on the XP
        self.scoreboards['levels_scoreboard'].set_display_string(self.levelsystem.level)  # Get the level based on the system level

        # Run Checks for Nuclease Regeneration
        if self.nuclease.regen_nuclease: self.nuclease = Nuclease(self.nuclease_speed, self.nuclease_size_modifier)  # If it says to regen the nuclease, regen it
        else: self.nuclease.handle_movement()  # Otherwise handle its movement as normal

        # Handle the movement, it will return whether or not they are moving, if they are set the slide iterator to 10 and moving value to True
        if self.character.handle_movement(): self.character.slide_iterator, self.character.moving = 10, True  # Handle the movement, if it returns true the user is moving, make 'em slide
        else: self.character.moving = False  # The user is not moving

        # If the user has been set up to slide via the slide iterator (frames they should slide for), slide the user
        if not self.character.moving and self.character_slide_iterator:
            self.character.slide(self.character_slide_iterator)  # Do the slide
            self.character_slide_iterator -= 1  # Reduce iterator

    def handle_timer_events(self):
        """
        Handle all timer-based events in the game (USEREVENT)

        Base Movement -> Move all base objects in the list "self.bases"
        Base Spawning -> Spawn bases every X seconds
        Game Music -> Start music loop at 0.1 seconds after game start
        Background Animation -> Switch to a new background animation every 15 seconds after start

        :return:
        """
        # Handle Base Movement (At every user event)
        for idx, item in enumerate(self.bases):  # For loop to iterate through all bases
            item.handle_movement()  # Handle their movement
            if item.remove_base:  # Remove them if they need to be removed
                self.bases.remove(item)

        # Start the game music at 0.1 seconds
        if 0.1 < self.general_timer < 0.2:
            set_music('game_music')
            pygame.mixer.music.play(-1)

        # Spawn New Bases every X seconds (but never the same one)
        if self.general_timer % self.base_spawnrate == 0:
            spawn = Base()
            while spawn.type == self.last_spawn.type:  # While it's the same base, spawn a new one
                spawn = Base()
            self.last_spawn = spawn  # Update the 'last base' value to check from
            self.bases.append(spawn)  # Add the bases to the list of bases when we get a satisfactory one

        # Every 15 seconds, do a random animation
        if self.general_timer % 15 == 0:
            self.current_background_animation = random.choice([LargeTestTube(), BunsenBurner(), Microscope(), TestTubeRack()])  # Run one of 9 different animations

    def get_background(self):
        """
        Get the current game background to display on the screen

        Klaxon Conditions -> What times it should display the klaxon background vs not
        Klaxon Sound -> If displaying the klaxon timer, run the sound if not already running

        :returns:
            Two returns.
            background_timer_red -> Klaxon timer
            background -> Regular background (Red-Klaxon free!)
        """
        # At 7-8, 5-6, 3-4, 1-2 and 0-0.2 seconds
        klaxon_conditions = [
            8 > self.timer_time_left > 7,
            6 > self.timer_time_left > 5,
            4 > self.timer_time_left > 3,
            2 > self.timer_time_left > 1,
            self.timer_time_left < 0.2
        ]

        # If any condition, loop the klaxon sound if it the channel isn't already busy (the sound isn't already being played)
        if any(klaxon_conditions):
            if not self.klaxon_channel.get_busy(): self.klaxon_channel.play(self.klaxon_sound)  # Play the klaxon sound on its channel
            return background_timer_red  # Set the display background to the red klaxon background

        # If the timer isn't at any of those intervals, then the klaxon doesn't need to blare and we can give the reg. background
        else:
            return background  # Set the display to the regular background

    def display_graphics(self, increment_character_state=True):
        """
        Display the graphics of the game on the screen (dis.blit to the screen)
        :param increment_character_state: Whether or not to increment the state of the character (useful for getting freeze-frames)

        Background -> Get then blit
        Background Animation -> Get then blit
        Scoreboards -> Loop thru all scoreboard and blit them
        Pause Button -> Get whether or not it should be highlighted (is it being moused over), and blit
        Character Image -> Update the character image (optional hitbox display included but commented to see all characters' hitboxes in all states)
        Base Timer -> Get the base timer image @ its proper rotation and blit it
        Bases -> Draw all the bases
        Nuclease -> Draw the Nuclease

        :return: No returns
        """

        # Main Background
        self.dis.blit(self.get_background(), (0, 0))

        # Background Animation
        if self.current_background_animation is not None:
            self.current_background_animation.get_image()
            self.dis.blit(self.current_background_animation.current_image, (self.current_background_animation.x, self.current_background_animation.y))

        # Draw all scoreboard items
        for item in self.scoreboards:
            self.dis.blit(self.scoreboards[item].get_image(), (self.scoreboards[item].rect_x, self.scoreboards[item].rect_y))

        # Draw Pause Button
        self.dis.blit(self.pause_menu['pause_button'].get_image(), (self.pause_menu['pause_button'].rect_x, self.pause_menu['pause_button'].rect_y))

        # Draw the Character
        self.character.update_image(increment_character_state)
        # Uncomment for Hitbox --> pygame.draw.rect(self.dis, (0, 0, 0), (self.character.hit_box[0], self.character.hit_box[1], self.character.hit_box[2], self.character.hit_box[3]))
        self.dis.blit(self.character.display_image, (self.character.position_x - self.character.flip_offset, self.character.position_y))

        # Draw the base timer based on the retrieved image
        base_timer = self.objective.get_image()
        self.dis.blit(base_timer[0], base_timer[1])

        # Draw the Bases
        for item in self.bases:
            self.dis.blit(item.get_image(), (item.position_x, item.position_y))

        # Draw the Nuclease
        self.dis.blit(self.nuclease.get_image(), (self.nuclease.position_x, self.nuclease.position_y))

    def handle_collisions(self):
        """
        Handle all object collisions within the game

        Base collides with base -> "Bump" each other in the opposite direction
        Base collides with player -> Get rid of base, check if it was the right base and handle actions based on the result
        Nuclease collides with the player -> Add a value to the nuclease collision counter, if exceeding the threshold, end the game

        :return: No returns
        """
        # If player hitbox is null cancel collision checks
        if None in self.character.hit_box:
            return

        # Creating rect objects for collision items
        character = pygame.Rect(
            self.character.hit_box[0],  # Character Hitbox
            self.character.hit_box[1],
            self.character.hit_box[2],
            self.character.hit_box[3]
        )

        nuclease_rect = pygame.Rect(
            self.nuclease.position_x,  # Nuclease Hitbox
            self.nuclease.position_y,
            nuclease_dimensions[0] * self.nuclease_size_modifier,
            nuclease_dimensions[1] * self.nuclease_size_modifier
        )

        # Checking Collisions

        # 1 - Base Collisions with objects
        for base in self.bases:  # Iterate through bases
            base_rect = pygame.Rect(base.position_x, base.position_y, base_dimensions[0], base_dimensions[1])

            # A - Base Collision with Base
            for other_base in self.bases:
                other_base_rect = pygame.Rect(other_base.position_x, other_base.position_y, base_dimensions[0], base_dimensions[1])

                # Switch direction on collision
                if base_rect.colliderect(other_base_rect) and base_rect != other_base_rect:
                    base.direction = not base.direction

                    # Prevent glitchy position changing (getting stuck in a loop of collisions and switching directions when the y values are equal)
                    if base.position_y > other_base.position_y:
                        base.position_y += 2

            # B - Base Collision with Character
            if base_rect.colliderect(character):
                got_base = self.objective.handle_collisions(base.type)

                # If the base they collided with was the objective base
                if got_base:
                    pygame.mixer.Sound.play(sounds['base_pickup_success_sound'])

                    self.base_timer = 0  # Reset the base timer if they caught the right one
                    self.experience, self.levelsystem.bases = self.experience + self.xp_increase_amount, self.levelsystem.bases + 1

                    # Update level & check for level up, run actions based on this
                    if self.levelsystem.update_level():  # Check the new level
                        pygame.mixer.Sound.play(sounds['level_up_sound'])
                        self.increase_difficulty()  # Increase game difficulty on level up

                # If the collided base wasn't the one they were supposed to get...
                else:
                    pygame.mixer.Sound.play(sounds['base_pickup_fail_sound'])

                    # Reduce the player's XP if they collide with/catch the wrong base as a penalty
                    if self.experience - 0.5 * self.xp_increase_amount >= 0:
                        self.experience -= round(0.5 * self.xp_increase_amount)

                # Remove the base always
                base.remove_base = True

        # 2 - Nuclease Collision with Player
        if nuclease_rect.colliderect(character):
            # Increase # of detected collisions with the Nuclease
            self.character_nuclease_collisions += 1

            # End game after a 10 frame collision buffer to give the user 'extra chances' to not die to/collide with the Nuclease
            if self.character_nuclease_collisions >= 10:
                pygame.mixer.Sound.play(sounds['player_crash_sound'])
                self.game_over = True, True  # End the game

    def increase_difficulty(self):
        """
        Increase the game difficulty

        Speed -> Increase speed every level
        Base Spawnrate -> Increase time per spawn by 0.5 seconds every 25 levels
        Time Per Base -> Time to get each base goes down by 1 second every 10 levels
        Nuclease Size -> Size increases every level by *0.1 current amount

        :return: No returns
        """
        # Increase the nuclease speed every level
        if self.nuclease_speed[0] < 20 and self.nuclease_speed[1] < 20:
            self.nuclease_speed[0] += 0.2  # Up by 0.2
            self.nuclease_speed[1] += 0.1  # Up by 0.1

        # Every 25 levels, make bases spawn slightly slower (Level 100 = 4 seconds)
        if self.levelsystem.level % 25 == 0: self.base_spawnrate += 0.5  # Decrease Spawn-rate

        # Every 10 levels decrement the amount of time per base (Level 100 = 15 seconds)
        if self.levelsystem.level % 10 == 0: self.objective.time_per_base -= 1  # Less time per base

        # Every level increase the size of the nuclease (Level 100 = Massive -- but fair)
        self.nuclease_size_modifier += 0.1  # Increase nuclease size (more likely to die to die)

    def death_actions(self):
        """
        A series of actions + an animation to be run on death

        Run Animation -> Set the player state to dead, update until they die
        Game Over Decal -> Display the game over decal every other second until the loop ends
        Event Handling:
            quit() -> Quit the game
            USEREVENT -> Add to the timer (timer is responsible for ending the loop when it's time)
            KEYDOWN -> If they press space or escape, end the animation early

        :return: No returns
        """

        # Stop the sounds being sent from before
        pygame.mixer.Sound.set_volume(self.klaxon_sound, 0)
        pygame.mixer.music.stop()

        pygame.mixer.Sound.play(sounds['game_over'])

        # Set default values; Dead & state pos 1 for death anim
        self.character.state, self.character.state_pos = 'dead', 1

        # Prep the values for the animation loop
        death_actions_loop, death_menu_time = True, 0

        # Death animation/action loop
        while death_actions_loop:

            # Define custom events for this mini-loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(), exit()
                if event.type == pygame.USEREVENT:
                    death_menu_time += 0.01  # Increase the time of death loop
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                        death_actions_loop = False  # Skip the animation on space/escape

            # Display graphics, but notice we don't handle normal events and have defined our own
            self.display_graphics()

            game_over_decal_conditions = [  # From 1-2, 3-4, 5-6
                1 < round(death_menu_time, 2) < 2,
                3 < round(death_menu_time, 2) < 4,
                5 < round(death_menu_time, 2) < 6
            ]

            # Display the game over decal if the conditions are met
            if any(game_over_decal_conditions):
                self.dis.blit(game_over, (DISPLAY_X / 2 - 320, 270))

            # End the loop after 7 seconds
            if round(death_menu_time, 2) > 7:
                death_actions_loop = False

            # Flip the display and tick the clock
            pygame.display.flip()
            self.clock.tick(self.tick_speed)

    def db_gamestats_insert(self):
        """
        Insert statistics into the database

        Steps for insertion:
            1. Connect to the database
            2. Set up a cursor for interacting with the database
            3. Execute an insert statement with (bases, xp, level, time, date)
            4. Commit the changes (save them), and close the database connection

        :return: No returns
        """

        # Open Connection to the database
        connect_db = sqlite3.connect('./BaseInvaders/statistics.db')  # Connect
        cursor_db = connect_db.cursor()  # Select a cursor for the database (a cursor is what you do actions in the database with)

        # Insert into the Database
        cursor_db.execute(f"INSERT INTO statistics VALUES (:bases, :xp, :level, :time, :date)",
                          {
                              'bases': self.levelsystem.bases,  # Bases (int)
                              'xp': self.experience,  # XP (int)
                              'level': self.levelsystem.level,  # Level (int)
                              'time': parse_time(self.general_timer),  # String (HH:MM:SS)
                              'date': time.strftime("%D")  # Date (MM/DD/YY)
                          }
                          )

        # Commit and close
        connect_db.commit(), connect_db.close()  # Commit (save) the changes, close the database connection

    def start_actions(self):
        """
        Run a series of actions at the start of the game before the player starts playing

        Run Player Animation:
            1. Set the character to walk mode & the timer to 0
            2. Run an animation to walk them to the middle

        Start Decal:
            1. Add to the decal size after each loop
            2. Stop displaying the decal after 6 seconds
            3. After 6 seconds switch to the 3, 2, 1 countdown decal

        Event Handling:
            quit() -> Exit the game
            USEREVENT -> Add to the timer which the loop is based off of after each USEREVENT (0.01 seconds)

        Reset all values at the end to not affect the game

        :return: No returns
        """
        self.display_graphics()  # Reset the screen anim
        self.character.state = 'walk'  # Set the state to walk
        self.general_timer = 0  # Set the timer to 0
        pygame.mixer.Sound.play(sounds['base_invaders_loading_sound'])

        # Set the scale for the animation and initialize the decal loop variable
        run_animation, decal_scale = True, 0.3

        while run_animation:
            # Increase the decal scale (gets bigger with every loop)
            decal_scale += 0.0038

            # Handle quit & timer event for this animation mini-loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(), quit()

                if event.type == pygame.USEREVENT:
                    self.general_timer += 0.01

            # Before the 6 second mark, display the temperature decal
            if round(self.general_timer, 2) < 6:
                decal_text = f"Heating... {round(50 + ((self.general_timer / 6) * 22))}°C"
            # If we're past the 6 second mark, display the count-in decal from the pause menu instead
            else:
                self.display_graphics(), self.pause_menu['pause_menu'].count_in(self.dis.copy())
                decal_text, run_animation = " ", False

            # Until the character is in the center of the screen, make them walk independent of time
            if not self.character.position_x > ((DISPLAY_X / 2) - (self.character.hit_box[3] / 2)):
                self.character.position_x += 5
            # When they get to the center, set them to idle mode instead
            else:
                self.character.state = 'idle'

            # Displaying all the graphics on the screen
            self.display_graphics()

            # Create an empty surface for the decal, scale the decal, blit the decal on that surface, blit the surface onto the display
            text_size = franklin_gothic_large_3.size(decal_text)  # Get the text size based on the text being displayed
            text_display = pygame.Surface(franklin_gothic_large_3.size(decal_text), pygame.SRCALPHA, 32).convert_alpha()  # Create the display from the text size
            text_display.blit(franklin_gothic_large_3.render(decal_text, True, COLOR_BGRD_BLUE_DARK), (0, 0))  # Render then blit the text onto the text display surface
            text_actual_size = (round(text_size[0] * decal_scale), (round(text_size[1] * decal_scale)))  # Get the dimensions for a scaled version of the text
            text_display = pygame.transform.smoothscale(text_display, text_actual_size)  # Scale the actual text based on the 'actual size' scaled dimensions

            self.dis.blit(text_display, (DISPLAY_X / 2 - text_actual_size[0] / 2, DISPLAY_Y / 3 - text_actual_size[1] / 2))  # Blit the text display on the real display

            # Flip the display & tick the clock
            pygame.display.flip()
            self.clock.tick(self.tick_speed)

        # Reset the general timer to 0 after the start animation as to not affect the game
        self.general_timer = 0

    @staticmethod
    def check_then_first_game_actions():
        """

        Check if it's their first game
            1. Open the json file, grab the data
            2. Check if the first_game value is set to True
            3. Run the tutorial if true:
                Tutorial -> Run the tutorial on the first game

        Fix the value to false
            1. Open the json file, take the cached data from before, edit the value to False from True
            2. Dump the data

        :return: No Returns
        """
        # Check if first game
        with open('./BaseInvaders/resources/user_data.json') as data:  # Open the json file in read mode
            user_data = json.load(data)  # Load the data as a dict

        # If it's their first game, run the tutorial
        if user_data.get('first_game') == "True":  # Get a value from the dict and run if the value is "True"
            Tutorial().run_menu()  # Run menu

        # Set the tutorial bool value to false since after this game they will have done their first game
        with open('./BaseInvaders/resources/user_data.json', 'w') as data:  # Open the json file in write mode
            user_data['first_game'] = "False"  # Change the local dictionary 'preferences' first_game value
            json.dump(user_data, data)  # Dump the new data in the json file


def game_loop(game_instance):
    """
    Run the main game loop

    Actions:
        1. While Loop

    While Loop:
        a) Handle events
        b) Handle collisions
        c) Display the graphics
        d) Update the display
        e) Tick the clock @ the clock speed

    :param game_instance: base_invaders game Object
    :return: False, always False as in order to stop the loop it must be False
    """

    # !!! MAIN GAME LOOP (ENTIRE GAME CONTROLLED THROUGH HERE) !!!
    while not game_instance.game_over[0]:
        game_instance.handle_events()  # Handle the events
        game_instance.handle_collisions()  # Handle the collisions
        game_instance.display_graphics()  # Display the graphics on the screen (all "dis.blit"'s in the game go here)
        pygame.display.flip()  # Update the display
        game_instance.clock.tick(game_instance.tick_speed)  # Tick the game clock at the game speed

    # Always returns False because the game is over
    return False


def base_invaders():
    """
    Main Base Invaders function, responsible for running the entire game

    Contains Loops:
        A) Start Menu Loop -> Run the entire start menu
        B) Main Game Loop -> Run the entire main game
        C) End Game Loop -> Run the end-game screen

    Actions:
        1. Initialize values
        2. Run start menu
        3. Set the character based on the start menu
        4. Check if first game then run the first game actions
        5. Do the start actions (in the game)
        6. Run the game loop
        7. Run the death actions if they died vs. quit on their own
        8. Insert stats into the database
        9. Run the end menu

    :return:
    """
    # Set to "While True" to allow for an infinite number of plays/loading

    while True:

        # Initialize new values for the game
        pygame.time.set_timer(pygame.USEREVENT, 10)  # 10ms
        game_instance = BaseInvaders()  # Initialize the game class
        game_instance.clock = pygame.time.Clock()  # Set the clock

        # !!! START MENU LOOP (Notice it's separate from the game and end screen loop) !!!
        while run_start_menu(game_instance.clock):
            pass

        # Set the character based on the start menu selection
        game_instance.character = game_instance.character.set_character()

        # If it's their first game, run the tutorial
        game_instance.check_then_first_game_actions()

        # Run the game start animation
        game_instance.start_actions()

        # Run the game loop until it's over
        while game_loop(game_instance):
            pass

        # If they specifically DIED and didn't quit the game, run the following
        if game_instance.game_over[1]: game_instance.death_actions()

        # Insert their stats into the database to run the end menu off of
        game_instance.db_gamestats_insert()

        # !!! END MENU LOOP (Notice it's separate from the game and start screen loop) !!!
        while run_end_menu():
            pass

        # Go back to the top after the end game menu and start a new game from the Menu

