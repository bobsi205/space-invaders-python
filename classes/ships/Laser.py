import pygame
import os
import time
import random

LASER_SOUND = pygame.mixer.Sound(os.path.join("assets\\sound", "laser.ogg"))


class Laser:
    def __init__(self, x, y, img, vel, direction, damage):
        self.x = x
        self.y = y
        self.img = img
        self.vel = vel
        self.direction = direction
        self.damage = damage
        self.mask = pygame.mask.from_surface(self.img)
        LASER_SOUND.play()

    def moveLaser(self):
        # moves the laser to the wanted diraction
        self.y = self.y + (self.direction * self.vel)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def off_screen(self, height):
        if self.direction > 0:
            if self.y > height:
                return True
        else:
            if self.y - self.img.get_height() < 0:
                return True
        return False

    def collision(self, obj):
        offset_x = int(obj.x-self.x)
        offset_y = int(obj.y-self.y)
        return self.mask.overlap(obj.mask, (offset_x, offset_y)) != None
