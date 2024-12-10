import pygame
import os

os.system("amixer sset Master 70%")
pygame.init()

dice_number = 6

my_sound = pygame.mixer.Sound('audio_files/dice_'+str(dice_number)+'.mp3')
playing = my_sound.play()
while playing.get_busy():
    pygame.time.delay(100)