import pygame
import os
import time
import random

pygame.mixer.init()
LASER_SOUND = pygame.mixer.Sound(os.path.join("assets\\sound", "laser.ogg"))
pygame.mixer.music.load(os.path.join("assets\\sound", "music.ogg"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
ENEMY_DEATH_SOUND = pygame.mixer.Sound(
    os.path.join("assets\\sound", "enemy_death.ogg"))
PLAYER_DEATH_SOUND = pygame.mixer.Sound(
    os.path.join("assets\\sound", "player_death.ogg"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("assets\\sound", "hit.ogg"))

PLAYER_SHIP_IMG = pygame.transform.scale(pygame.image.load(os.path.join(
    "assets\\200ships\\Shaded", "ship_0.png")), (50, 50))

PLAYER_LIFE_IMG = pygame.transform.scale(pygame.image.load(os.path.join(
    "assets\\200ships\\Shaded", "ship_0.png")), (25, 25))


ENEMY_1_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(
    "assets\\200ships\\Shaded", "ship_130.png")), (50, 50)), 180)

ENEMY_2_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(
    "assets\\200ships\\Shaded", "ship_145.png")), (50, 50)), 180)

ENEMY_3_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(
    "assets\\200ships\\Shaded", "ship_167.png")), (50, 50)), 180)

PLAYER_LASER_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join("assets\\ships\\PNG_Animations\\Shots\\Shot1", "shot1_4.png")), (20, 20)), 90)


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


class Enemy1(Ship):
    def __init__(self, x, y, health=1,  ship_vel=1, laser_vel=2, cooldown=0, shoot_timer=200, damage=1):
        super().__init__(x, y, health, ship_vel, laser_vel, cooldown, shoot_timer, damage)
        self.ship_img = ENEMY_1_IMG
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.hitSound = HIT_SOUND
        self.deathSound = ENEMY_DEATH_SOUND

    def move(self):
        self.y += self.ship_vel


class Enemy2(Ship):
    def __init__(self, x, y, health=2,  ship_vel=1, laser_vel=2, cooldown=0, shoot_timer=150, damage=1):
        super().__init__(x, y, health, ship_vel, laser_vel, cooldown, shoot_timer, damage)
        self.ship_img = ENEMY_2_IMG
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.hitSound = HIT_SOUND
        self.deathSound = ENEMY_DEATH_SOUND

    def move(self):
        self.y += self.ship_vel


class Enemy3(Ship):
    def __init__(self, x, y, health=3,  ship_vel=1, laser_vel=2, cooldown=0, shoot_timer=100, damage=1):
        super().__init__(x, y, health, ship_vel, laser_vel, cooldown, shoot_timer, damage)
        self.ship_img = ENEMY_3_IMG
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.hitSound = HIT_SOUND
        self.deathSound = ENEMY_DEATH_SOUND

    def move(self):
        self.y += self.ship_vel


class GameState:
    def __init__(self, lasers, enemies, score=0, run=True, FPS=60, level=0, lives=3, lost=False, lost_counter=0, wave_length=5):
        self.FPS = FPS
        self.level = level
        self.lives = lives
        self.lost = lost
        self.lost_counter = lost_counter
        self.enemies = enemies
        self.wave_length = wave_length
        self.lasers = lasers
        self.run = run
        self.score = score
