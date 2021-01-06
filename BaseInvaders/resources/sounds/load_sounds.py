from BaseInvaders.config import music_volume
import pygame

pygame.init()

filepath = "./BaseInvaders/resources/sounds/"  # File path for the sound resources

# Sounds

sounds = {
    'base_invaders_loading_sound': pygame.mixer.Sound(filepath + "base_invaders_loading.wav"),      # I would comment them, but it's literally in the Key name, so...
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
    """
    Set the music based off of pre-defined options

    :param option: (string) -> Set the music to a specific track
    :return: No returns

    """

    # If the pick is menu_game_music, play the menu game music wav file @ filepath
    if option == 'menu_game_music':
        pygame.mixer.music.load(filepath + "menu_game_music.wav")

    # If the pick is projector_sound_music, play the projector sound music wav file @ filepath
    if option == 'projector_sound_music':
        pygame.mixer.music.load(filepath + "projector_sound.wav")

    # If the pick is game_music, play the game music wav file @ filepath
    if option == 'game_music':
        pygame.mixer.music.load(filepath + "game_music.wav")

    # Set the volume to the required volume for the track
    pygame.mixer.music.set_volume(music_volume)



