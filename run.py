# Run - Day of fury
import math
from random import random

import pygame

from pygame.time import Clock
from pygame.sprite import Group
from pygame import Color
from xretro.retrogame import Game
from xretro.retrotext import Text
from xretro.retroimages import ImageSet
from xretro.retroimages import AnimSet
from xretro.retrosounds import SoundBox

from player import Player
from pygame import Surface
import os

RATIO = 1.777777778  # Exemplos que podemos usar ratios: 1.777777778 (1280x720) 1.333333333 (800x600) 1.6 (320x200)
HEIGHT = 600
WIDTH = math.floor(HEIGHT * RATIO)
FPS = 60

ST_TITLE = 1
ST_PLAYING = 2
ST_GAME_OVER = 3
ST_CREDITS = 4

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

# --------------- HUD LIVES -------------------
heart_set = ImageSet()
heart_set.add(os.path.join("TokyioGeisha_Pixel Hearts", "PNGs", "0.bmp"))
heart_img = heart_set.get(0).get_image()
heart_img.set_colorkey(Color("white"))

# -------------------PLAYER ANIMATIONS----------------------
player_idle = ImageSet()
for i in range(0, 10):
    player_idle.add(os.path.join("Soldier-Guy", "_Mode-Gun", "01-Idle", "E_E_Gun__Idle_{0:03n}.png".format(i)))
player_idle.zoom(0.3)

player_run = ImageSet()
for i in range(0, 10):
    player_run.add(os.path.join("Soldier-Guy", "_Mode-Gun", "02-Run", "E_E_Gun__Run_000_{0:03n}.png".format(i)))
player_run.zoom(0.3)

player_jump = ImageSet()
for i in range(0, 1):
    player_jump.add(os.path.join("Soldier-Guy", "_Mode-Gun", "05-Jump", "E_E_Gun__Jump_{0:03n}.png".format(i)))
player_jump.zoom(0.3)

player_shot = ImageSet()
for i in range(0, 10):
    player_shot.add(os.path.join("Soldier-Guy", "_Mode-Gun", "03-Shot", "E_E_Gun__Attack_{0:03n}.png".format(i)))
player_shot.zoom(0.3)

buffer = Surface((WIDTH, HEIGHT))

lives = 3
ammo = 50
score = 0
music: SoundBox
state = ST_TITLE


def manage_states():
    global state

    while True:
        if state == ST_TITLE:
            state_title()

        if state == ST_PLAYING:
            state_playing()

        if state == ST_CREDITS:
            pass

        if state == ST_GAME_OVER:
            state_gameover()


def state_title():
    global music
    global state
    running = True

    background = ImageSet()
    background.add("patcheshugh_backgrnd-3.png")
    background.zoom(1.8)

    ze = ImageSet()
    ze.add(os.path.join("Soldier-Guy", "_Mode-Gun", "03-Shot", "E_E_Gun__Attack_000.png"))
    ze.zoom(0.3)

    music = SoundBox("SpringSpring_CC0_short theme melon no pwm.ogg").play_music()

    pygame.time.set_timer(pygame.USEREVENT, 300, True)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music.fadeout(1500)
                    state = ST_PLAYING
                    return

                if event.key == pygame.K_ESCAPE:
                    finish()

            if event.type == pygame.USEREVENT:
                txt_push.togle_visible()
                pygame.time.set_timer(pygame.USEREVENT, 300, True)

        buffer.blit(background.get(0).get_image(), pygame.Rect(0, 0, 0, 0))
        buffer.blit(ze.get(0).get_image(), pygame.Rect(250, 220, 0, 0))

        txt_title.draw_xc(buffer, game.h // 2 - 195)
        txt_title2.draw_xc(buffer, game.h // 2 - 200)

        txt_push.draw_xc(buffer, game.h // 2 + 30)

        screen.blit(buffer, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


def state_playing():
    global score
    global state
    global music

    stage = Group()
    running = True

    music = SoundBox("public_domain_upbeatoverworld.wav").play_music()

    player = Player(stage, game, WIDTH // 2 - 80, 100)

    player.animations.add(player_idle)
    player.animations.add(player_run)
    player.animations.add(player_jump)
    player.animations.add(player_shot)

    player.fric = 0.2
    player.grav_vel = 2.8
    player.grav_acel = 0.45
    player.ymax = 450
    player.xmin = 200
    player.xmax = WIDTH - 200
    player.image_speed = 0.15

    # ----------------- BACKGROUNDS ------------------
    bk = ImageSet()
    bk.add("patcheshugh_backgrnd-3.png")
    rb1 = bk.get(0).get_image().get_rect()
    rb2 = bk.get(0).get_image().get_rect()
    rb1.left = 0
    rb2.left = rb1.right

    EV_SCORE = pygame.USEREVENT + 10
    pygame.time.set_timer(EV_SCORE, 300, False)

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                music.unload()
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    music.fadeout(1500)
                    state = ST_TITLE
                    return

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
    w = heart_img.get_width()
    for i in range(1, lives + 1):
        x = (base + 100 + 60) + i * (w + 4)
        y = HEIGHT - 55
        surface.blit(heart_img, (x, y))

    txt_ammo.draw_xy(surface, base + 400, HEIGHT - 70)
    txt_ammov.draw_xy(surface, base + 520, HEIGHT - 70)

    txt_score.draw_xy(surface, base + 680, HEIGHT - 70)
    txt_scorev.set_text(str.format("{0:05n}", score))
    txt_scorev.draw_xy(surface, base + 800, HEIGHT - 70)


def state_gameover():
    global state

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music.fadeout(1500)
                state = ST_PLAYING
                return


def finish():
    global music
    music.unload()
    pygame.quit()
    exit()


manage_states()
