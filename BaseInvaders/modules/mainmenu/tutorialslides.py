import pygame
from BaseInvaders.config import tutorial
from main import dis
from BaseInvaders.modules.sounds import *

class Tutorial:
    def __init__(self):
        self.slide = 1
        self.slides = tutorial
        self.stop_menu = False
        self.dis = dis

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), quit()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.Sound.play(sounds['next_slide_sound'])
                if event.key in [pygame.K_SPACE, ord("w"), ord("d"), pygame.K_UP, pygame.K_RIGHT]:
                    self.slide += 1
                if event.key in [ord("a"), ord("s"), pygame.K_DOWN, pygame.K_LEFT]:
                    self.slide -= 1
                if event.key == pygame.K_ESCAPE:
                    self.stop_menu = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(sounds['next_slide_sound'])
                if event.button == 1:
                    self.slide += 1
                if event.button == 3:
                    self.slide -= 1

    def draw_graphics(self):

        if self.slide < 1: self.slide = 1
        if self.slide > len(self.slides):
            self.stop_menu = True
            return

        self.dis.blit(self.slides[self.slide], (0, 0))

    def run_menu(self):
        set_music('projector_sound_music')
        pygame.mixer.music.play(-1)

        while not self.stop_menu:
            self.handle_events()
            self.draw_graphics()
            pygame.display.flip()

        pygame.mixer.music.stop()
