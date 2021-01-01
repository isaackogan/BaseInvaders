import pygame
from BaseInvaders.resources.characters.load_characters import *
from BaseInvaders.modules.resourcetools import load_anim_images

ground = 700

base_dimensions = 116, 350
base_dimensions = (round(base_dimensions[0] / 4), round(base_dimensions[1] / 4))

bases = {
    'adenine': load_anim_images('./BaseInvaders/resources/bases/adenine/Adenine (<>).png', 1, 4),
    'thymine': load_anim_images('./BaseInvaders/resources/bases/thymine/Thymine (<>).png', 1, 4),
    'cytosine': load_anim_images('./BaseInvaders/resources/bases/cytosine/Cytosine (<>).png', 1, 4),
    'guanine': load_anim_images('./BaseInvaders/resources/bases/guanine/Guanine (<>).png', 1, 4)
}

nuclease_dimensions = 640, 640
nuclease_division_amount = 6.8
nuclease_dimensions = (round(nuclease_dimensions[0] / nuclease_division_amount), round(nuclease_dimensions[1] / nuclease_division_amount))
nuclease = load_anim_images('./BaseInvaders/resources/nuclease/Nuclease (<>).png', 1, 14)

pygame.font.init()

game_over = pygame.image.load('./BaseInvaders/resources/GameOver.png')

xp_increase_amount = 10

