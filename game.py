import pygame
import os
import time
import random
from classes.GameState import GameState
from classes.Ship import Ship
from classes.ships.Laser import Laser
from classes.ships.Enemy1 import Enemy1
from classes.ships.Enemy2 import Enemy2
from classes.ships.Enemy3 import Enemy3
from classes.ships.PlayerShip import Player, PLAYER_LIFE_IMG


# variables
WIDTH, HEIGHT = 1280, 720

# images
BG = pygame.transform.scale(pygame.image.load(os.path.join(
    "assets", "space_background.jpg")), (WIDTH, HEIGHT))

ENEMY_LASER_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join("assets\\ships\\PNG_Animations\\Shots\\Shot5", "shot5_5.png")), (20, 20)), 90)


# display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bam")


def main():
    clock = pygame.time.Clock()
    bgY = 0
    bgY2 = -BG.get_height()
    main_font = pygame.font.SysFont("roboto", 30, bold=False, italic=False)
    lost_font = pygame.font.SysFont("roboto", 70, bold=True, italic=False)

    # init game state
    gameState = GameState([], [])
    player = Player(WIDTH/2, HEIGHT-50)

    def enemy_shoot(enemy):
        if enemy.y > 0:
            rand = random.randrange(0, 100)
            if enemy.cooldown < enemy.shoot_timer:
                enemy.cooldown += 1
            if enemy.cooldown >= enemy.shoot_timer and rand > 95:
                enemy.cooldown = 0
                laser = Laser(enemy.x + 10, enemy.y + enemy.ship_img.get_height()-10, ENEMY_LASER_IMG,
                              enemy.laser_vel+enemy.ship_vel, 1, enemy.damage)
                gameState.lasers.append(laser)

    def stageHandler():
        if len(gameState.enemies) == 0:
            gameState.level += 1
            gameState.wave_length += 5
            enemy_dic = (Enemy1, Enemy2, Enemy3)
            for i in range(gameState.wave_length):
                enemy = random.choice(enemy_dic)
                gameState.enemies.append(enemy(random.randrange(100, WIDTH-100),
                                               random.randrange(-1500, -100)))
        else:
            # handles enemies
            for enemy in gameState.enemies:
                enemy.move()
                enemy_shoot(enemy)
                if(enemy.y >= HEIGHT or enemy.y > 0 and player.collide(enemy)):
                    gameState.enemies.remove(enemy)
                    enemy.death()
                    gameState.hit()

        # handles lasers
        if len(gameState.lasers):
            for laser in gameState.lasers:
                if laser.off_screen(HEIGHT):
                    gameState.lasers.remove(laser)
                elif player.collide(laser):
                    gameState.hit()
                    gameState.lasers.remove(laser)
                else:
                    move = True
                    for obj in (gameState.enemies):
                        if(laser.collision(obj)):
                            obj.Damage(laser.damage)
                            if obj.health <= 0:
                                gameState.enemies.remove(obj)
                            gameState.lasers.remove(laser)
                            move = False
                            continue
                    if(laser.collision(player)):
                        player.Damage(laser.damage)
                        gameState.lasers.remove(laser)
                        move = False
                        continue
                    if move:
                        laser.moveLaser()
        player.shot_counter()

    def deathHandler():
        # handles lost game timer
        if gameState.lives == 0:
            if(gameState.lost_counter == 0):
                player.death()
            gameState.lost = True
            gameState.lost_counter += 1

        # checks if lost the game
        if gameState.lost:
            if gameState.lost_counter > gameState.FPS*3:
                gameState.run = False
            else:
                return True

    def reRender():
        # background
        WIN.blit(BG, (0, bgY))
        WIN.blit(BG, (0, bgY2))

        # enemies
        for enemy in gameState.enemies:
            enemy.draw(WIN)

        # player
        player.draw(WIN)

        # lasers
        for laser in gameState.lasers:
            laser.draw(WIN)

        # render lost message
        if gameState.lost:
            lost_message = lost_font.render(
                "You Lost! Better Luck Next Time", 1, (255, 255, 255))
            WIN.blit(lost_message, (WIDTH/2-lost_message.get_width() /
                                    2, HEIGHT/2-lost_message.get_height()/2))

        # draw text
        level_label = main_font.render(
            f"Level: {gameState.level}", 1, (255, 255, 255))
        enemies_left = main_font.render(
            f"Enemies Left: {len(gameState.enemies)}", 1, (255, 255, 255))

        # render lives
        for i in range(gameState.lives):
            WIN.blit(PLAYER_LIFE_IMG, (10 +
                                       (i*PLAYER_LIFE_IMG.get_width())+5, 10))

        WIN.blit(level_label, (WIDTH-level_label.get_width()-10, 10))
        WIN.blit(enemies_left, (WIDTH-enemies_left.get_width() -
                                10, 20 + level_label.get_height()))
        pygame.display.update()

    while gameState.run:

        clock.tick(gameState.FPS)
        reRender()

        # handles death
        if(deathHandler()):
            continue

        # handle background repetition
        bgY += 0.8
        bgY2 += 0.8
        if bgY > BG.get_height():
            bgY = -BG.get_height()
        if bgY2 > BG.get_height():
            bgY2 = -BG.get_height()

        stageHandler()

        # handles pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState.run = False

        # track movment
        player.controles(WIDTH, HEIGHT, gameState.lasers)


main()
