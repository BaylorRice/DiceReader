import pygame
import os

os.system("amixer sset Master 70%")
pygame.init()

my_sound = pygame.mixer.Sound('audio-testing/falling_funk.wav')
playing = my_sound.play()
while playing.get_busy():
    pygame.time.delay(100)