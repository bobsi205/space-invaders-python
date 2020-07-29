import pygame
import os

# player
PLAYER_DEATH_SOUND = pygame.mixer.Sound(
    os.path.join("assets\\sound", "player_death.ogg"))

#player and enemy
HIT_SOUND = pygame.mixer.Sound(os.path.join("assets\\sound", "hit.ogg"))

# enemys
ENEMY_DEATH_SOUND = pygame.mixer.Sound(
    os.path.join("assets\\sound", "enemy_death.ogg"))

# weapon sound
LASER_SOUND = pygame.mixer.Sound(os.path.join("assets\\sound", "laser.ogg"))

# music
pygame.mixer.music.load(os.path.join("assets\\sound", "music.ogg"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
