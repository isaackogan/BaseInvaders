
import pygame
from BaseInvaders.modules.resource_tools import load_anim_images

pygame.init()

"""

STANDARD

"""

# Boy States
boy_division_amount = 2.8  # How much to divide the picture size by when scaling

boy_states = {      # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/standard/boy/dead/Dead (<>).png', 1, 15, (614 / boy_division_amount, 564 / boy_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/standard/boy/idle/Idle (<>).png', 1, 15, (614 / boy_division_amount, 564 / boy_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/standard/boy/run/Run (<>).png', 1, 15, (614 / boy_division_amount, 564 / boy_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/standard/boy/walk/Walk (<>).png', 1, 15, (614 / boy_division_amount, 564 / boy_division_amount)),
}

# Girl States
girl_division_amount = 3  # How much to divide by

girl_states = {     # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/standard/girl/dead/Dead (<>).png', 1, 30, (601 / girl_division_amount, 502 / girl_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/standard/girl/idle/Idle (<>).png', 1, 16, (416 / girl_division_amount, 454 / girl_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/standard/girl/run/Run (<>).png', 1, 20, (416 / girl_division_amount, 454 / girl_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/standard/girl/walk/Walk (<>).png', 1, 20, (416 / girl_division_amount, 454 / girl_division_amount)),
}

"""

#ZOMBIE

"""

zombie_division_amount = 3  # How much to divide the picture size by when scaling

# Boy Zombie States
boy_zombie_states = {       # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/zombie/zombieboy/dead/Dead (<>).png', 1, 12, (629 / zombie_division_amount, 526 / zombie_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/zombie/zombieboy/idle/Idle (<>).png', 1, 15, (430 / zombie_division_amount, 519 / zombie_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/zombie/zombieboy/run/Run (<>).png', 1, 10, (430 / zombie_division_amount, 519 / zombie_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/zombie/zombieboy/walk/Walk (<>).png', 1, 10, (430 / zombie_division_amount, 519 / zombie_division_amount)),
}

# Girl Zombie States
girl_zombie_states = {      # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/zombie/zombiegirl/dead/Dead (<>).png', 1, 12, (684 / zombie_division_amount, 627 / zombie_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/zombie/zombiegirl/idle/Idle (<>).png', 1, 15, (521 / zombie_division_amount, 576 / zombie_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/zombie/zombiegirl/run/Run (<>).png', 1, 10, (521 / zombie_division_amount, 576 / zombie_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/zombie/zombiegirl/walk/Walk (<>).png', 1, 10, (521 / zombie_division_amount, 576 / zombie_division_amount)),
}

"""

#NINJA

"""

# Boy Ninja States
ninja_boy_division_amount = 2.8  # How much to divide the picture size by when scaling
boy_ninja_states = {    # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/ninja/ninjaboy/dead/Dead__00<>.png', 0, 9, (482 / ninja_boy_division_amount, 498 / ninja_boy_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/ninja/ninjaboy/idle/Idle__00<>.png', 0, 9, (232 / ninja_boy_division_amount, 439 / ninja_boy_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/ninja/ninjaboy/run/Run__00<>.png', 0, 9, (363 / ninja_boy_division_amount, 458 / ninja_boy_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/ninja/ninjaboy/walk/Walk__00<>.png', 0, 9, (363 / ninja_boy_division_amount, 458 / ninja_boy_division_amount)),
}

# Girl Ninja States
ninja_girl_division_amount = 3.2
girl_ninja_states = {       # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/ninja/ninjagirl/dead/Dead__00<>.png', 0, 9, (578 / ninja_girl_division_amount, 599 / ninja_girl_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/ninja/ninjagirl/idle/Idle__00<>.png', 0, 9, (290 / ninja_girl_division_amount, 500 / ninja_girl_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/ninja/ninjagirl/run/Run__00<>.png', 0, 9, (376 / ninja_girl_division_amount, 520 / ninja_girl_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/ninja/ninjagirl/walk/Walk__00<>.png', 0, 9, (376 / ninja_girl_division_amount, 520 / ninja_girl_division_amount)),
}


"""

#ADVENTURE

"""

adventure_division_amount = 3  # How much to divide the picture size by when scaling

# Boy Adventure States
boy_adventure_states = {        # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/adventure/adventureboy/dead/Dead__00<>.png', 0, 9, (588 / adventure_division_amount, 600 / adventure_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/adventure/adventureboy/idle/Idle__00<>.png', 0, 9, (319 / adventure_division_amount, 486 / adventure_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/adventure/adventureboy/run/Run__00<>.png', 0, 9, (415 / adventure_division_amount, 507 / adventure_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/adventure/adventureboy/walk/Walk__00<>.png', 0, 9, (415 / adventure_division_amount, 507 / adventure_division_amount)),
}

# Girl Adventure States
girl_adventure_states = {       # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/adventure/adventuregirl/dead/Dead (<>).png', 1, 10, (605 / adventure_division_amount, 604 / adventure_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/adventure/adventuregirl/idle/Idle (<>).png', 1, 10, (641 / adventure_division_amount, 542 / adventure_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/adventure/adventuregirl/run/Run (<>).png', 1, 8, (641 / adventure_division_amount, 542 / adventure_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/adventure/adventuregirl/walk/Walk (<>).png', 1, 8, (641 / adventure_division_amount, 542 / adventure_division_amount)),
}

"""

#ANIMAL

"""

animal_division_amount = 2.8  # How much to divide the picture size by when scaling

# Cat States
cat_animal_states = {       # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/animal/cat/dead/Dead (<>).png', 1, 10, (556 / animal_division_amount, 504 / animal_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/animal/cat/idle/Idle (<>).png', 1, 10, (542 / animal_division_amount, 474 / animal_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/animal/cat/run/Run (<>).png', 1, 8, (542 / animal_division_amount, 474 / animal_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/animal/cat/walk/Walk (<>).png', 1, 10, (542 / animal_division_amount, 474 / animal_division_amount)),
}

# Dog States
dog_animal_states = {       # Create a dictionary of all states of the sprite
    'dead': load_anim_images('./BaseInvaders/resources/characters/animal/dog/dead/Dead (<>).png', 1, 10, (580 / animal_division_amount, 510 / animal_division_amount)),
    'idle': load_anim_images('./BaseInvaders/resources/characters/animal/dog/idle/Idle (<>).png', 1, 10, (547 / animal_division_amount, 481 / animal_division_amount)),
    'run': load_anim_images('./BaseInvaders/resources/characters/animal/dog/run/Run (<>).png', 1, 8, (547 / animal_division_amount, 481 / animal_division_amount)),
    'walk': load_anim_images('./BaseInvaders/resources/characters/animal/dog/walk/Walk (<>).png', 1, 10, (547 / animal_division_amount, 481 / animal_division_amount)),
}

"""

ALL CHARACTER CHOICES (FOR MAIN MENU)

"""

character_choices = {
    'standard_boy': pygame.image.load('./BaseInvaders/resources/characters/standard/boy/idle/Idle (1).png'),
    'standard_girl': pygame.image.load('./BaseInvaders/resources/characters/standard/girl/idle/Idle (1).png'),
    'zombie_boy': pygame.image.load('./BaseInvaders/resources/characters/zombie/zombieboy/idle/Idle (1).png'),
    'zombie_girl': pygame.image.load('./BaseInvaders/resources/characters/zombie/zombiegirl/idle/Idle (1).png'),
    'ninja_boy': pygame.image.load('./BaseInvaders/resources/characters/ninja/ninjaboy/idle/Idle__000.png'),
    'ninja_girl': pygame.image.load('./BaseInvaders/resources/characters/ninja/ninjagirl/idle/Idle__000.png'),
    'cat_animal': pygame.image.load('./BaseInvaders/resources/characters/animal/cat/idle/Idle (1).png'),
    'dog_animal': pygame.image.load('./BaseInvaders/resources/characters/animal/dog/idle/Idle (1).png'),
    'adventure_boy': pygame.image.load('./BaseInvaders/resources/characters/adventure/adventureboy/idle/Idle__000.png'),
    'adventure_girl': pygame.image.load('./BaseInvaders/resources/characters/adventure/adventuregirl/idle/Idle (1).png')
}
