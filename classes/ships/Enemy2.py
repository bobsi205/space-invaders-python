import pygame
import os

from classes.Ship import Ship
from classes.Sound import HIT_SOUND, ENEMY_DEATH_SOUND


ENEMY_2_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(
    "assets\\ships", "enemy2.png")), (50, 50)), 180)


class Enemy2(Ship):
    def __init__(self, x, y, health=2,  ship_vel=1, laser_vel=2, cooldown=0, shoot_timer=150, damage=1):
        super().__init__(x, y, health, ship_vel, laser_vel, cooldown, shoot_timer, damage)
        self.ship_img = ENEMY_2_IMG
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.hitSound = HIT_SOUND
        self.deathSound = ENEMY_DEATH_SOUND

    def move(self):
        self.y += self.ship_vel
