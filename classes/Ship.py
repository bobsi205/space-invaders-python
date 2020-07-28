import pygame
import os
import time
import random


class Ship:
    def __init__(self, x, y, health,  ship_vel, laser_vel, cooldown, shoot_timer, damage):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_vel = laser_vel
        self.ship_vel = ship_vel
        self.cooldown = cooldown
        self.shoot_timer = shoot_timer
        self.hitSound = None
        self.deathSound = None
        self.damage = damage

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def shot_counter(self):
        if self.cooldown < self.shoot_timer:
            self.cooldown += 1

    def death(self):
        self.deathSound.play()

    def hit(self):
        self.hitSound.play()

    def Damage(self, damage_value):
        self.health -= damage_value
        if(self.health > 0):
            self.hitSound.play()
        else:
            self.deathSound.play()
