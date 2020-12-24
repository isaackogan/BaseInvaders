from BaseInvaders.modules.objectives import *
from BaseInvaders.modules.characters import *
from BaseInvaders.modules.bases import *
from config import DISPLAY_X, DISPLAY_Y
from main import *
from BaseInvaders.modules.backgroundanims import *

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
        self.bases = []
        self.points = 0
        self.last_spawn = Base()
        self.obj = None
        self.dis = dis
        self.current_animation = None

        pygame.time.set_timer(pygame.USEREVENT, 10)

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), exit()

            if event.type == pygame.USEREVENT:
                self.general_timer += 0.01
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

                self.obj.rotation -= 0.1

        self.character.handle_movement()

    def draw_graphics(self):
        self.dis.blit(self.background, (0, 0))

        # Level Display
        level_info = self.level.get_level()

        self.dis.blit(level_font.render(level_info[0], 1, LEVEL_COLOUR), (DISPLAY_X / 2 - level_info[1][0] / 2, 255))  # Draw game over text

        if self.current_animation is not None:
            self.current_animation.get_image()
            self.dis.blit(self.current_animation.current_image, (self.current_animation.x, self.current_animation.y))

        self.character.update_image()

        # pygame.draw.rect(self.dis, (0, 0, 0), (self.character.hit_box[0], self.character.hit_box[1], self.character.hit_box[2], self.character.hit_box[3]))
        self.dis.blit(self.character.display_image, (self.character.position_x - self.character.flip_offset, self.character.position_y))
        self.dis.blit(self.obj.get_image()[0], self.obj.get_image()[1])

        for item in self.bases:
            self.dis.blit(item.get_image(), (item.position_x, item.position_y))

    def handle_collisions(self):
        self.handle_events()

        for item in self.bases:
            r = pygame.Rect(item.position_x, item.position_y, base_dimensions[0], base_dimensions[1])
            o = pygame.Rect(self.character.hit_box[0], self.character.hit_box[1], self.character.hit_box[2], self.character.hit_box[3])
            if r.colliderect(o):
                print(self.points)
                got_base = self.obj.handle_collisions(item.type)

                if got_base:
                    self.points += 1
                    self.level.bases -= 1

                item.remove_base = True


def base_invaders():
    pygame.display.set_caption("Base Invaders"), pygame.display.set_icon(caption_image)  # Setting the caption & Icon
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 10)  # 10ms

    # Initial Values
    game_instance = BaseInvaders()
    game_instance.obj = BaseObjective()

    while True:
        game_instance.handle_collisions()
        game_instance.draw_graphics()

        pygame.display.flip()
        clock.tick(game_instance.speed)
