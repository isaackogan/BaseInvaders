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

pause_menu_font = pygame.font.Font("./BaseInvaders/resources/fonts/bahnschrift.ttf", 50)
scoreboard_font = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 40)
pause_button_font = pygame.font.Font("./BaseInvaders/resources/fonts/Franklin Gothic.ttf", 53)