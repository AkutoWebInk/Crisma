import pygame

def play(sound):
    pygame.mixer.init()
    path=f"{sound}"
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
