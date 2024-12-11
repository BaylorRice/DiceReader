import pygame
import os

os.system("amixer sset Master 50%")
pygame.init()

my_sound = pygame.mixer.Sound('audio_files/finished_startup.wav')
playing = my_sound.play()
while playing.get_busy():
    pygame.time.delay(100)