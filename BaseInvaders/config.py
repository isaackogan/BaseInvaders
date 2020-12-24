import pygame
from BaseInvaders.resources.characters.load_characters import *
from BaseInvaders.modules.resourcetools import load_anim_images

caption_image = pygame.image.load('./BaseInvaders/resources/icon.png')
ground = 700

base_dimensions = 116, 350
base_dimensions = (round(base_dimensions[0] / 4), round(base_dimensions[1] / 4))

bases = {
    'adenine': load_anim_images('./BaseInvaders/resources/bases/adenine/Adenine (<>).png', 1, 4),
    'thymine': load_anim_images('./BaseInvaders/resources/bases/thymine/Thymine (<>).png', 1, 4),
    'cytosine': load_anim_images('./BaseInvaders/resources/bases/cytosine/Cytosine (<>).png', 1, 4),
    'guanine': load_anim_images('./BaseInvaders/resources/bases/guanine/Guanine (<>).png', 1, 4)
}

pow_dimensions = 300, 279
pow_dimensions = (round(pow_dimensions[0]/2), round(pow_dimensions[1]/2))

pow = pygame.transform.scale(pygame.image.load('./BaseInvaders/resources/Pow.png'), pow_dimensions),

pygame.font.init()

# Colours
LEVEL_COLOUR = (99, 125, 144)
level_font = pygame.font.SysFont('Filicudi', 110)
