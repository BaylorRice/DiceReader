import pygame
import os

os.system("amixer sset Master 50%")
pygame.init()

my_sound = pygame.mixer.Sound('audio-testing/dice_1.mp3')
playing = my_sound.play()
while playing.get_busy():
    pygame.time.delay(100)