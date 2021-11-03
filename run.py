# Run - Day of fury
import math
from random import random

import pygame

from pygame.time import Clock
from pygame.sprite import Group
from pygame import Color
from xretro.ClassGame import Game
from xretro.ClassText import Text
from xretro.ClassImageWorks import ImageSet
from xretro.ClassImageWorks import AnimSet
from ClassPlayer import Player
import os

RATIO = 1.777777778  # Exemplos que podemos usar ratios: 1.777777778 (1280x720) 1.333333333 (800x600) 1.6 (320x200)
HEIGHT = 600
WIDTH = HEIGHT * RATIO
FPS = 60

# Inicializa a pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Jogo
game = Game("Corra que o Zé vem ai!", WIDTH, HEIGHT)

# Prepara
screen = pygame.display.set_mode([game.w, game.h])
clock = Clock()

pygame.display.set_caption(game.title)

# -------------------TEXTOS-----------------------
txt_title = Text("Changa-VariableFont_wght.ttf", game.title, 60, Color("Yellow")).set_bold(True).set_italic(True)
txt_push = Text("Changa-VariableFont_wght.ttf", "Push space key", 30, Color("White")).set_bold(True).set_italic(True)

pygame.time.set_timer(pygame.USEREVENT, 300)


# TITLE STATE ----------------------------------------------------------------------------------
def state_title():
    running = True

    images = ImageSet()
    images.add("patcheshugh_backgrnd-2.png")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state_playing()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.USEREVENT:
                txt_push.togle_visible()
                pygame.time.set_timer(pygame.USEREVENT, 300)

        screen.blit(images.get(0).get_image(), pygame.Rect(0, 0, 0, 0))

        txt_title.draw_xc(screen, game.h // 2 - 200)
        txt_push.draw_xc(screen, game.h // 2 + 30)

        pygame.display.flip()
        clock.tick(FPS)


# GAME STATE----------------------------------------------------------------------------------
def state_playing():
    stage = Group()
    running = True

    # -------------------JOGADOR----------------------
    player_idle = ImageSet()
    for i in range(0, 9):
        player_idle.add(os.path.join("Soldier-Guy", "_Mode-Gun", "01-Idle", "E_E_Gun__Idle_{0:03n}.png".format(i)))
    player_idle.zoom(0.3)

    player_run = ImageSet()
    for i in range(0, 9):
        player_run.add(os.path.join("Soldier-Guy", "_Mode-Gun", "02-Run", "E_E_Gun__Run_000_{0:03n}.png".format(i)))
    player_run.zoom(0.3)

    player_jump = ImageSet()
    for i in range(0, 0):
        player_jump.add(os.path.join("Soldier-Guy", "_Mode-Gun", "05-Jump", "E_E_Gun__Jump_000_{0:03n}.png".format(i)))
    player_jump.zoom(0.3)

    player = Player(stage, WIDTH / 2 - 80, 100)

    player.animations = AnimSet()
    player.animations.add(player_idle)
    player.animations.add(player_run)
    player.animations.add(player_jump)

    player.fric = 0.2
    player.grav_vel = 2.8
    player.grav_acel = 0.45
    player.ymax = 450
    player.xmin = 180
    player.xmax = WIDTH - 180
    player.image_speed = 0.15

    # ----------------- BACKGROUNDS ------------------
    bk = ImageSet()
    bk.add("patcheshugh_backgrnd-2.png")
    imw = bk.get(0).get_image().get_width()
    xb1 = 0
    xb2 = imw + 1

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player.image_index += 1

        screen.blit(bk.get(0).get_image(), pygame.Rect(xb1, 0, 0, 0))
        screen.blit(bk.get(0).get_image(), pygame.Rect(xb2, 0, 0, 0))

        xb1 -= player.h_vel
        xb2 -= player.h_vel

        if xb1 > 0:
            xb1 = 0
            xb2 = xb1 + imw + 1

        if xb2 + imw <= WIDTH:
            xb1 = 0
            xb2 = imw + 1

        stage.update()
        stage.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


# GAME OVER STATE----------------------------------------------------------------------------------
def state_gameover():
    pass


state_title()
pygame.quit()
exit()
