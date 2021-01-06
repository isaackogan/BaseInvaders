import pygame

pygame.init()

DISPLAY_X, DISPLAY_Y = 1200, 900                                                # Display size (X & Y)
caption_image = pygame.image.load('BaseInvaders/resources/game_icon.png')       # Icon for physical game window

COLOR_LIGHT_BLUE = pygame.Color(81, 153, 194)  # Light blue colour
loading_screen_image = pygame.image.load('./BaseInvaders/resources/LoadingScreen.png')  # Loading screen image
