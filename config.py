import pygame
pygame.font.init()

DISPLAY_X, DISPLAY_Y = 1200, 900

# Colours (Global)
COLOR_BURLYWOOD = (220, 163, 93)  # Border Colour
COLOR_BURLYWOOD_DARK = (204, 151, 86)


COLOR_TAN = (225, 180, 128)  # Middle colour
COLOR_TAN_DARK = (196, 157, 112)

COLOR_BROWN = (88, 47, 12)  # Text Colour
COLOR_BROWN_DARK = (69, 37, 9)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_WHITE_DARK = (163, 163, 163)
COLOR_BGRD_BLUE_DARK = (99, 125, 144)

bahnschrift_font = pygame.font.Font("./BaseInvaders/resources/fonts/bahnschrift.ttf", 50)

franklin_gothic_small = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 40)
franklin_gothic_large = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 270)
franklin_gothic_medium = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 53)

franklin_gothic_medium_2 = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 50)
franklin_gothic_large_2 = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 140)

caption_image = pygame.image.load('./BaseInvaders/resources/icon.png')