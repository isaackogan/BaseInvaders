from BaseInvaders.modules.objectives import *
from BaseInvaders.modules.characters import *
from BaseInvaders.modules.bases import *
from config import DISPLAY_X, DISPLAY_Y
from BaseInvaders.modules.neucleases import Nuclease
from main import *
from BaseInvaders.modules.background import *


class BaseInvaders:
    def __init__(self):
        self.display_x, self.display_y = DISPLAY_X, DISPLAY_Y
        self.background = pygame.transform.scale(pygame.image.load('./BaseInvaders/resources/BaseInvaders.png'), (self.display_x, self.display_y))
        self.clock = None
        self.character = Boy()
        self.level = LevelsSystem()
        self.speed = 30
        self.pressed_keys = pygame.key.get_pressed()
        self.general_timer = 0
        self.base_timer = 0
        self.bases = []
        self.points = 0
        self.last_spawn = Base()
        self.objective = None
        self.dis = dis
        self.current_animation = None
        self.nuclease = Nuclease()
        self.game_over = False

        pygame.time.set_timer(pygame.USEREVENT, 10)

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

                if self.general_timer % 2 == 0:
                    spawn = Base()
                    while spawn.type == self.last_spawn.type:
                        spawn = Base()
                    self.last_spawn = spawn
                    self.bases.append(spawn)

                # Every 15 seconds
                if self.general_timer % 15 == 0:
                    self.current_animation = choice([LargeTestTube(), BunsenBurner(), Microscope(), TestTubeRack()])  # 9 different animations

                # Switch the pos
                if self.general_timer % 0.5 == 0:
                    for item in self.bases:
                        item.state_pos += 0

                # Determines time left and runs checks
                self.objective.time_left = round(self.objective.time_per_base - self.base_timer, 2)
                if self.objective.time_left <= 0:
                    self.game_over = True

            if self.nuclease.regen_nuclease:
                self.nuclease = Nuclease()

        self.character.handle_movement()
        self.nuclease.handle_movement()

    def draw_graphics(self):
        self.dis.blit(self.background, (0, 0))

        # Level Display
        level_info = self.level.get_level()

        # self.dis.blit(level_font.render(level_info[0], 1, LEVEL_COLOUR), (DISPLAY_X / 2 - level_info[1][0] / 2, 255))  # Draw game over text

        if self.current_animation is not None:
            self.current_animation.get_image()
            self.dis.blit(self.current_animation.current_image, (self.current_animation.x, self.current_animation.y))

        self.character.update_image()

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
        self.handle_events()

        # If player hitbox is null cancel collision checks
        if None in self.character.hit_box:
            return

        character = pygame.Rect(self.character.hit_box[0], self.character.hit_box[1], self.character.hit_box[2], self.character.hit_box[3])
        nuclease_rect = pygame.Rect(self.nuclease.position_x, self.nuclease.position_y, nuclease_dimensions[0], nuclease_dimensions[1])

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
                    self.points += 1
                    self.level.bases -= 1
                    self.base_timer = 0 # Reset the base timer if they caught the right one

                item.remove_base = True

        # Nuclease Collision with Player
        if nuclease_rect.colliderect(character):
            print("COLLISION")
            self.game_over = True


def base_invaders():
    pygame.display.set_caption("Base Invaders"), pygame.display.set_icon(caption_image)  # Setting the caption & Icon
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 10)  # 10ms

    # Initial Values
    game_instance = BaseInvaders()
    game_instance.objective = BaseObjective()

    while True:
        game_instance.handle_collisions()
        game_instance.draw_graphics()

        pygame.display.flip()
        clock.tick(game_instance.speed)
