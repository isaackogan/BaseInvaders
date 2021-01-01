import pygame

pygame.init()

loading_screen_image = pygame.image.load('./BaseInvaders/resources/LoadingScreen.png')


def loading_screen(dis, percent_loaded):
    full = 548
    if percent_loaded > 100: percent_loaded = 100
    percent_loaded /= 100
    percent_loaded_pixels = percent_loaded * full

    dis.blit(loading_screen_image, (0, 0))
    pygame.draw.rect(dis, (0, 0, 0), (331, 351, percent_loaded_pixels, 34))
