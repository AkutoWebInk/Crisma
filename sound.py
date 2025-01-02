from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

def play(sound):
    pygame.mixer.init()
    path=f"{sound}"
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
