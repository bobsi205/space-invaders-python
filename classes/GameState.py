import pygame
import os
import time
import random


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
