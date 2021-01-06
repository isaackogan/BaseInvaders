from config import *
from BaseInvaders.modules.resource_tools import load_anim_images

pygame.init()

# Game Settings (Constants)

ground = 700                                                            # Pixel location of the ground (game functions around this value)
music_volume = 0.3
max_leaderboard_number = 100

# Resource Settings (Constants)

base_dimensions = 116, 350                                              # Dimensions of Default Base Images (A, T, C, G)
base_dimensions = (                                                     # Scaling size of the base dimensions (how much to reduce to)
    round(base_dimensions[0] / 4),
    round(base_dimensions[1] / 4)
)

nuclease_dimensions, nuclease_division_scale = (640, 640), 6.8      # Dimensions of default nuclease image and how much to divide by
nuclease_dimensions = (                                             # Scaling size of the base dimensions (what it gets reduced to)
    round(nuclease_dimensions[0] / nuclease_division_scale),
    round(nuclease_dimensions[1] / nuclease_division_scale)
)

# General Resource Loading (Surface Objects)

bases = {
    'adenine': pygame.image.load('./BaseInvaders/resources/bases/Adenine (1).png'),       # Dictionary containing all images for bases
    'thymine': pygame.image.load('./BaseInvaders/resources/bases/Thymine (1).png'),
    'cytosine': pygame.image.load('./BaseInvaders/resources/bases/Cytosine (1).png'),
    'guanine': pygame.image.load('./BaseInvaders/resources/bases/Guanine (1).png'),
}
nuclease = load_anim_images('./BaseInvaders/resources/nuclease/Nuclease (<>).png', 1, 14)    # Dictionary containing all images/frames for Nuclease animation
tutorial = load_anim_images('./BaseInvaders/resources/tutorial/Tutorial (<>).png', 1, 10)    # Dictionary containing all images/frames for Tutorial animation

background = pygame.transform.scale(pygame.image.load('./BaseInvaders/resources/BaseInvaders.png'), (DISPLAY_X, DISPLAY_Y))     # Game Background
background_timer_red = pygame.image.load('./BaseInvaders/resources/TimerRedBackground.png')                                     # Background but with a red timer
game_over = pygame.image.load('./BaseInvaders/resources/GameOver.png')                                                          # Game Over Decal
end_game_menu = pygame.image.load('./BaseInvaders/resources/EndGameMenu.png')                                                   # End Game Menu Page
statistics_menu = pygame.image.load('./BaseInvaders/resources/StatisticsMenu.png')                                              # Statistics Page
menu_screen_image = pygame.image.load('./BaseInvaders/resources/MenuScreen.png')                                                # Menu screen image

# Game Colours (Colour Objects)

COLOR_BURLYWOOD = pygame.Color(220, 163, 93)                                                  # Brownish Tan
COLOR_BURLYWOOD_DARK = pygame.Color(204, 151, 86)                                             # Darker Brownish Tan
COLOR_TAN = pygame.Color(225, 180, 128)                                                       # Tan
COLOR_TAN_DARK = pygame.Color(196, 157, 112)                                                  # Darker Tan
COLOR_BROWN = pygame.Color(88, 47, 12)                                                        # Classic Brown
COLOR_BROWN_DARK = pygame.Color(69, 37, 9)                                                    # Darker Classic Brown
COLOR_BLACK = pygame.Color(0, 0, 0)                                                           # Black
COLOR_WHITE = pygame.Color(255, 255, 255)                                                     # White
COLOR_WHITE_DARK = pygame.Color(163, 163, 163)                                                # Darker White
COLOR_WHITE_SEMI_DARK = pygame.Color(224, 224, 224)                                           # Between Darker and Even Darker White
COLOR_WHITE_SEMI_DARK_ALT = pygame.Color(110, 110, 110)                                       # Even Darker White
COLOR_BGRD_BLUE_DARK = pygame.Color(99, 125, 144)                                             # Game Background Colour (Teal/Turquoise Blue)

# Game Fonts (Font Objects)

bahnschrift_font = pygame.font.Font("./BaseInvaders/resources/fonts/bahnschrift.ttf", 50)               # Bahnschrift Large
bahnschrift_font_small = pygame.font.Font("./BaseInvaders/resources/fonts/bahnschrift.ttf", 25)         # Bahnschrift Small


franklin_gothic_large = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 270)     # Franklin Gothic Large
franklin_gothic_large_2 = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 140)   # Franklin Gothic Large-Small
franklin_gothic_large_3 = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 95)    # Franklin Gothic Large-Small-Small
franklin_gothic_medium = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 53)     # Franklin Gothic Medium
franklin_gothic_medium_2 = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 50)   # Franklin Gothic Medium-Small
franklin_gothic_small = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 40)      # Franklin Gothic Small

# Character Positions

character_positions = {
    'standard_boy': (310, 437),
    'standard_girl': (255, 455),
    'zombie_boy': (280, 422),
    'zombie_girl': (232, 407),
    'ninja_boy': (320, 470),
    'ninja_girl': (295, 437),
    'cat_animal': (240, 450),
    'dog_animal': (239, 448),
    'adventure_boy': (290, 450),
    'adventure_girl': (222, 433),
}
