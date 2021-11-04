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
from pygame import Surface
import os
import ftplib

RATIO = 1.777777778  # Exemplos que podemos usar ratios: 1.777777778 (1280x720) 1.333333333 (800x600) 1.6 (320x200)
HEIGHT = 600
WIDTH = math.floor(HEIGHT * RATIO)
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

# -------------- TITLE TEXTS-----------------
txt_title = Text("Changa-VariableFont_wght.ttf", game.title, 60, Color(134, 240, 0)).set_bold(True).set_italic(True)
txt_title2 = Text("Changa-VariableFont_wght.ttf", game.title, 60, Color(67, 109, 27)).set_bold(True).set_italic(True)
txt_push = Text("Changa-VariableFont_wght.ttf", "Push space key", 30, Color("White")).set_bold(True).set_italic(True)

# -------------- HUD TEXTS -------------------
txt_lives = Text("Changa-VariableFont_wght.ttf", "LIVES:", 30, Color("White")).set_bold(True)
txt_ammo = Text("Changa-VariableFont_wght.ttf", "AMMO:", 30, Color("White")).set_bold(True)
txt_score = Text("Changa-VariableFont_wght.ttf", "SCORE:", 30, Color("White")).set_bold(True)

txt_ammov = Text("Changa-VariableFont_wght.ttf", "000", 30, Color("#EDD400")).set_bold(True)
txt_scorev = Text("Changa-VariableFont_wght.ttf", "00000", 30, Color("#EDD400")).set_bold(True)

pygame.time.set_timer(pygame.USEREVENT, 300)

buffer = Surface((WIDTH, HEIGHT))

lives = 3
ammo = 50
score = 0


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

        buffer.blit(images.get(0).get_image(), pygame.Rect(0, 0, 0, 0))

        txt_title.draw_xc(buffer, game.h // 2 - 195)
        txt_title2.draw_xc(buffer, game.h // 2 - 200)

        txt_push.draw_xc(buffer, game.h // 2 + 30)

        screen.blit(buffer, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


# GAME STATE----------------------------------------------------------------------------------
def state_playing():
    global score

    stage = Group()
    running = True


    # -------------------PLAYER ANIMATIONS----------------------
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
    player.xmin = 200
    player.xmax = WIDTH - 200
    player.image_speed = 0.15

    # ----------------- BACKGROUNDS ------------------
    bk = ImageSet()
    bk.add("patcheshugh_backgrnd-2.png")
    rb1 = bk.get(0).get_image().get_rect()
    rb2 = bk.get(0).get_image().get_rect()
    rb1.left = 0
    rb2.left = rb1.right

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

        buffer.blit(bk.get(0).get_image(), rb1)
        buffer.blit(bk.get(0).get_image(), rb2)

        rb1.left += player.h_vel * -1
        rb2.left += player.h_vel * -1

        if rb1.left > 0:
            rb1.left = 0
            rb2.left = rb1.right

        if rb2.right <= WIDTH:
            rb1.left = rb2.left
            rb2.left = rb1.right
        score += 1

        stage.update()
        stage.draw(buffer)

        draw_hud(buffer)

        screen.blit(buffer, (0, 0))
        pygame.display.flip()

        clock.tick(FPS)


def draw_hud(surface: Surface):
    global score
    global lives

    base = 50
    txt_lives.draw_xy(surface, base + 100, HEIGHT - 70)

    txt_ammo.draw_xy(surface, base + 400, HEIGHT - 70)
    txt_ammov.draw_xy(surface, base + 520, HEIGHT - 70)

    txt_score.draw_xy(surface, base + 680, HEIGHT - 70)
    txt_scorev.set_text(str.format("{0:05n}", score))
    txt_scorev.draw_xy(surface, base + 800, HEIGHT - 70)

    pass


# GAME OVER STATE----------------------------------------------------------------------------------
def state_gameover():
    pass




state_title()
pygame.quit()
exit()
