from BaseInvaders.modules.background import *
from BaseInvaders.modules.scoreboard import *
from BaseInvaders.modules.pausemenu import *
from BaseInvaders.modules.mainmenu.menuscreen import run_start_menu
import json
from BaseInvaders.modules.resourcetools import parse_time
from time import strftime
from BaseInvaders.modules.endmenu import *
from BaseInvaders.modules.characters import *
from BaseInvaders.modules.bases import *
from BaseInvaders.modules.objectives import *
from BaseInvaders.modules.neucleases import *


class BaseInvaders:
    def __init__(self):
        self.display_x, self.display_y = DISPLAY_X, DISPLAY_Y
        self.background = pygame.transform.scale(pygame.image.load('./BaseInvaders/resources/BaseInvaders.png'), (self.display_x, self.display_y))
        self.clock = None
        self.character = self.set_character()
        self.speed = 30
        self.pressed_keys = pygame.key.get_pressed()
        self.general_timer = 0
        self.base_timer = 0
        self.bases = []
        self.last_spawn = Base()
        self.objective = None
        self.dis = dis
        self.current_animation = None

        self.game_over = False, False
        self.levelsystem = LevelsSystem()

        self.score_scoreboard = ScoreSB()
        self.levels_scoreboard = LevelSB()
        self.experience_scoreboard = ExperienceSB()

        self.pause_menu = PauseMenu()
        self.pause_button = PauseButton()

        self.experience = 0

        self.base_spawnrate = 2

        self.nuclease_speed = [2, 3]
        self.nuclease_size_modifier = 1
        self.nuclease = Nuclease(self.nuclease_speed)

        pygame.time.set_timer(pygame.USEREVENT, 10)

        self.slide_iterator = 0

        self.collisions = 0

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), exit()

            if event.type == pygame.USEREVENT:
                self.general_timer += 0.01
                self.base_timer += 0.01

                self.base_timer = round(self.base_timer, 2)
                self.general_timer = round(self.general_timer, 2)

                for idx, item in enumerate(self.bases):
                    item.handle_movement()
                    if item.remove_base:
                        self.bases.remove(item)

                if self.general_timer % self.base_spawnrate == 0:
                    spawn = Base()
                    while spawn.type == self.last_spawn.type:
                        spawn = Base()
                    self.last_spawn = spawn
                    self.bases.append(spawn)

                # Every 15 seconds
                if self.general_timer % 15 == 0:
                    self.current_animation = LargeTestTube()  # choice([LargeTestTube(), BunsenBurner(), Microscope(), TestTubeRack()])  # 9 different animations

                # Switch the pos
                if self.general_timer % 0.5 == 0:
                    for item in self.bases:
                        item.state_pos += 0

                # Determines time left and runs checks
                self.objective.time_left = round(self.objective.time_per_base - self.base_timer, 2)
                if self.objective.time_left <= 0:
                    self.game_over = True, True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pause_menu.run_menu() is True:
                        self.game_over = True, False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_button.mouse_on_button():
                    if self.pause_menu.run_menu() is True:
                        self.game_over = True, False

        # Update Scoreboard
        self.score_scoreboard.set_display_string(
            (self.levelsystem.bases - self.levelsystem.bases_at_level(self.levelsystem.level),
             (self.levelsystem.bases_at_level(self.levelsystem.level + 1) - self.levelsystem.bases_at_level(self.levelsystem.level)))
        )
        self.experience_scoreboard.set_display_string(self.experience)
        self.levels_scoreboard.set_display_string(self.levelsystem.level)

        # Other Tasks
        if self.nuclease.regen_nuclease: self.nuclease = Nuclease(self.nuclease_speed, self.nuclease_size_modifier)
        self.nuclease.handle_movement()

        if self.character.handle_movement():
            self.slide_iterator = 10
            moving = True
        else:
            moving = False

        # If user slide and not running
        if not moving and self.slide_iterator:
            self.character.slide(self.slide_iterator)
            self.slide_iterator -= 1

    def draw_graphics(self, increment_character_state=True):
        self.dis.blit(self.background, (0, 0))

        # Scoreboard Items
        self.dis.blit(self.score_scoreboard.get_image(), (self.score_scoreboard.rect_x, self.score_scoreboard.rect_y))  # Score
        self.dis.blit(self.levels_scoreboard.get_image(), (self.levels_scoreboard.rect_x, self.levels_scoreboard.rect_y))  # Levels
        self.dis.blit(self.experience_scoreboard.get_image(), (self.experience_scoreboard.rect_x, self.experience_scoreboard.rect_y))  # Levels

        # Pause Button
        self.dis.blit(self.pause_button.get_image(), (self.pause_button.rect_x, self.pause_button.rect_y))

        if self.current_animation is not None:
            self.current_animation.get_image()
            self.dis.blit(self.current_animation.current_image, (self.current_animation.x, self.current_animation.y))

        self.character.update_image(increment_character_state)

        # pygame.draw.rect(self.dis, (0, 0, 0), (self.character.hit_box[0], self.character.hit_box[1], self.character.hit_box[2], self.character.hit_box[3]))
        self.dis.blit(self.character.display_image, (self.character.position_x - self.character.flip_offset, self.character.position_y))

        # Calculate base timer
        base_timer = self.objective.get_image()
        self.dis.blit(base_timer[0], base_timer[1])

        # Bases
        for item in self.bases:
            self.dis.blit(item.get_image(), (item.position_x, item.position_y))

        # Nuclease
        self.dis.blit(self.nuclease.get_image(), (self.nuclease.position_x, self.nuclease.position_y))

    def handle_collisions(self):
        # If player hitbox is null cancel collision checks
        if None in self.character.hit_box:
            return

        character = pygame.Rect(self.character.hit_box[0], self.character.hit_box[1], self.character.hit_box[2], self.character.hit_box[3])

        nuclease_rect = pygame.Rect(
            self.nuclease.position_x,
            self.nuclease.position_y,
            nuclease_dimensions[0] * self.nuclease_size_modifier,
            nuclease_dimensions[1] * self.nuclease_size_modifier
        )

        # Base Collisions
        for item in self.bases:
            base_rect = pygame.Rect(item.position_x, item.position_y, base_dimensions[0], base_dimensions[1])

            # Base Collision with Base
            for more in self.bases:
                more_rect = pygame.Rect(more.position_x, more.position_y, base_dimensions[0], base_dimensions[1])

                # Switch direction on collision
                if base_rect.colliderect(more_rect) and base_rect != more_rect:
                    item.direction = not item.direction

                    # Prevent glitchy position changing (getting stuck in a loop of collisions and switching directions when the y values are equal)
                    if item.position_y > more.position_y:
                        item.position_y += 2

            # Base Collision with Character
            if base_rect.colliderect(character):
                got_base = self.objective.handle_collisions(item.type)

                if got_base:
                    self.experience += xp_increase_amount
                    self.levelsystem.bases += 1

                    result = self.levelsystem.update_level()

                    # Increase difficulty @ certain level intervals
                    if result:
                        self.increase_difficulty()

                    self.base_timer = 0  # Reset the base timer if they caught the right one

                item.remove_base = True

        # Nuclease Collision with Player
        if nuclease_rect.colliderect(character):
            print("COLLISION")

            self.collisions += 1
            if self.collisions >= 10:
                self.game_over = True, True

    def increase_difficulty(self):
        # Increase the nuclease speed every level
        if self.nuclease_speed[0] < 20 and self.nuclease_speed[1] < 20:
            self.nuclease_speed[0] += 0.2
            self.nuclease_speed[1] += 0.1

        # Every 25 levels, make bases spawn slightly lower (Level 100 = 4 seconds)
        if self.levelsystem.level % 25 == 0:
            self.base_spawnrate += 0.5

        # Every 10 levels decrement the amount of time per base (Level 100 = 15 seconds)
        if self.levelsystem.level % 10 == 0:
            self.objective.time_per_base -= 1

        # Every level increase the size of the nuclease (Level 100 = Massive -- but fair)
        self.nuclease_size_modifier += 0.1

    def set_character(self):
        character_choices = {
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
        with open('./BaseInvaders/preferences.json') as data:
            preferences = json.load(data)

        character = preferences.get('preferences').get('character')

        return character_choices[character]

    def death_actions(self, clock):
        self.character.state = 'dead'
        self.character.state_pos = 1

        death_actions = True
        death_menu_time = 0

        while death_actions:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(), exit()
                if event.type == pygame.USEREVENT:
                    death_menu_time += 0.01
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                        death_actions = False

            self.draw_graphics()

            if (1 < round(death_menu_time, 2) < 2) or (3 < round(death_menu_time, 2) < 4) or 5 < round(death_menu_time, 2) < 6:
                self.dis.blit(
                    game_over, (DISPLAY_X / 2 - 320, 270)
                )

            if round(death_menu_time, 2) > 7:
                death_actions = False

            pygame.display.flip()
            clock.tick(self.speed)

    def db_gamestats_insert(self):

        # Open Connection
        connect_db = sqlite3.connect('./BaseInvaders/statistics.db')
        cursor_db = connect_db.cursor()

        cursor_db.execute(f"INSERT INTO statistics VALUES (:bases, :xp, :level, :time, :date)",
                          {
                              'bases': self.levelsystem.bases,
                              'xp': self.experience,
                              'level': self.levelsystem.level,
                              'time': parse_time(self.general_timer),
                              'date': strftime("%D")
                          }
                          )

        connect_db.commit(), connect_db.close()


def base_invaders():
    pygame.display.set_caption("Base Invaders")  # Setting the Caption

    while True:
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 10)  # 10ms

        # Initial Values
        game_instance = BaseInvaders()
        game_instance.objective = BaseObjective()

        while run_start_menu():
            pass

        while not game_instance.game_over[0]:
            game_instance.handle_events()
            game_instance.handle_collisions()
            game_instance.draw_graphics()
            pygame.display.flip()
            clock.tick(game_instance.speed)

        # Stuff to do if they died regularly (didn't choose to quit)
        if game_instance.game_over[1]:  game_instance.death_actions(clock)
        game_instance.db_gamestats_insert()

        while run_end_menu():
            pass
