import pygame

pygame.init()

filepath = "./BaseInvaders/resources/sounds/"

# Sounds

sounds = {
    'base_invaders_loading_sound': pygame.mixer.Sound(filepath + "base_invaders_loading.wav"),
    'base_pickup_success_sound': pygame.mixer.Sound(filepath + "base_pickup_success.wav"),
    'base_pickup_fail_sound': pygame.mixer.Sound(filepath + "base_pickup_fail.wav"),
    'button_click_sound': pygame.mixer.Sound(filepath + "button_click.wav"),
    'level_up_sound': pygame.mixer.Sound(filepath + "level_up_sound.wav"),
    'next_slide_sound': pygame.mixer.Sound(filepath + "next_slide.wav"),
    'game_over': pygame.mixer.Sound(filepath + "game_over.wav"),
    'timer_alarm_sound': pygame.mixer.Sound(filepath + "timer_alarm.wav"),
    'player_crash_sound': pygame.mixer.Sound(filepath + "player_crash.wav"),
}

# Music


def set_music(option):
    if option == 'menu_game_music':
        pygame.mixer.music.load(filepath + "menu_game_music.wav")
    if option == 'projector_sound_music':
        pygame.mixer.music.load(filepath + "projector_sound.wav")
    if option == 'game_music':
        pygame.mixer.music.load(filepath + "game_music.wav")

    pygame.mixer.music.set_volume(0.3)



