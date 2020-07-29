import pygame
import os
import time
import random
from classes.Ship import Ship
from classes.ships.Laser import Laser
from classes.Sound import PLAYER_DEATH_SOUND, HIT_SOUND


PLAYER_SHIP_IMG = pygame.transform.scale(pygame.image.load(os.path.join(
    "assets\\200ships\\Shaded", "ship_0.png")), (50, 50))

PLAYER_LIFE_IMG = pygame.transform.scale(pygame.image.load(os.path.join(
    "assets\\200ships\\Shaded", "ship_0.png")), (25, 25))
PLAYER_LASER_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join("assets\\ships\\PNG_Animations\\Shots\\Shot1", "shot1_4.png")), (20, 20)), 90)


class Player(Ship):
    def __init__(self, x, y, health=5,  ship_vel=5, laser_vel=2, cooldown=0, shoot_timer=30, damage=1):
        super().__init__(x, y, health, ship_vel, laser_vel, cooldown, shoot_timer, damage)
        self.ship_img = PLAYER_SHIP_IMG
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.hitSound = HIT_SOUND
        self.deathSound = PLAYER_DEATH_SOUND

    def controles(self, width, height, lasers):
        keys = pygame.key.get_pressed()
        # movment
        if keys[pygame.K_LEFT] and self.x - self.ship_vel >= 0:
            self.x -= self.ship_vel
        if keys[pygame.K_RIGHT] and self.x + self.ship_vel + self.get_width() <= width:
            self.x += self.ship_vel
        if keys[pygame.K_UP] and self.y - self.ship_vel >= 0:
            self.y -= self.ship_vel
        if keys[pygame.K_DOWN] and self.y + self.ship_vel + self.get_height() <= height:
            self.y += self.ship_vel
        # shoot
        if keys[pygame.K_SPACE]:
            if(self.cooldown >=
               self.shoot_timer):
                laser = Laser(self.x+15, self.y-15, PLAYER_LASER_IMG,
                              self.laser_vel+self.ship_vel, -1, self.damage)
                lasers.append(laser)
                self.cooldown = 0

    def collide(self, obj):
        offsetX = int(obj.x - self.x)
        offsetY = int(obj.y - self.y)
        return self.mask.overlap(obj.mask, (offsetX, offsetY)) != None
