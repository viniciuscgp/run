# Run - Day of fury
import random

import pygame

from pygame.time import Clock
from pygame import Color

from xretro.retroactor import Actor
from xretro.retrogame import Game
from xretro.retrotext import Text
from xretro.retroimages import ImageSet
from xretro.retrosounds import SoundBox

from player import Player
from pygame import Surface
from enem3 import Enem3
from pygame.time import set_timer

import os
import glob

# Inicializa a pygame --------------------------
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Jogo -----------------------------------------
game = Game("Corra que o Zé vem ai!", glob.WIDTH, glob.HEIGHT)

# Prepara --------------------------------------
screen = pygame.display.set_mode([game.w, game.h])
clock = Clock()

pygame.display.set_caption(game.title)

# TITLE TEXTS ----------------------------------
txt_title = Text("Changa-VariableFont_wght.ttf", game.title, 60, Color(134, 240, 0)).set_bold(True).set_italic(True)
txt_title2 = Text("Changa-VariableFont_wght.ttf", game.title, 60, Color(67, 109, 27)).set_bold(True).set_italic(True)
txt_push = Text("Changa-VariableFont_wght.ttf", "Push space key", 40, Color("White")).set_bold(True).set_italic(True)

# HUD TEXTS ------------------------------------
txt_lives = Text("Changa-VariableFont_wght.ttf", "LIVES:", 30, Color("White")).set_bold(True)
txt_ammo = Text("Changa-VariableFont_wght.ttf", "AMMO:", 30, Color("White")).set_bold(True)
txt_score = Text("Changa-VariableFont_wght.ttf", "SCORE:", 30, Color("White")).set_bold(True)

txt_ammov = Text("Changa-VariableFont_wght.ttf", "000", 30, Color("#EDD400")).set_bold(True)
txt_scorev = Text("Changa-VariableFont_wght.ttf", "00000", 30, Color("#EDD400")).set_bold(True)

txt_debug = Text("Changa-VariableFont_wght.ttf", "00000", 30, Color("#EDD400")).set_bold(True)

# HUD LIVES ------------------------------------
heart_set = ImageSet()
heart_set.add(os.path.join("TokyioGeisha_Pixel Hearts", "PNGs", "0.bmp"))
heart_img = heart_set.get(0).get_image()
heart_img.set_colorkey(Color("white"))

buffer = Surface((glob.WIDTH, glob.HEIGHT))

lives = 3
ammo = 50
score = 0

music: SoundBox
state = glob.ST_TITLE


def manage_states():
    global state

    while True:
        if state == glob.ST_TITLE:
            state_title()

        if state == glob.ST_PLAYING:
            state_playing()

        if state == glob.ST_CREDITS:
            pass

        if state == glob.ST_GAME_OVER:
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

    music = SoundBox("SpringSpring_CC0_short theme melon no pwm.ogg").loop_music().set_volume(glob.vol_music)

    set_timer(glob.EV_PUSH, 300, True)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music.fadeout(1500)
                    state = glob.ST_PLAYING
                    return

                if event.key == pygame.K_ESCAPE:
                    finish()

            if event.type == glob.EV_PUSH:
                txt_push.togle_visible()
                set_timer(glob.EV_PUSH, 300, True)

        buffer.blit(background.get(0).get_image(), pygame.Rect(0, 0, 0, 0))
        buffer.blit(ze.get(0).get_image(), pygame.Rect(470, 220, 0, 0))

        txt_title.draw_xc(buffer, game.h // 2 - 265)
        txt_title2.draw_xc(buffer, game.h // 2 - 260)

        txt_push.draw_xc(buffer, game.h // 2 + 40)

        screen.blit(buffer, (0, 0))
        pygame.display.flip()
        clock.tick(glob.FPS)


def state_playing():
    global score
    global state
    global music

    def make_enemy_level1():
        ex = game.w - 50
        ey = game.h - 300
        en = Enem3(game, glob.LAYER_INIM, ex, ey)
        en.parent = mv
        en.diff1()

    def make_enemy_level2():
        if random.randint(1, 100) < 50:
            ex = game.w - 50
            ey = game.h - 300
            en = Enem3(game, glob.LAYER_INIM, ex, ey)
            en.diff1()
            en.parent = mv
        else:
            ex = 0
            ey = game.h - 300
            en = Enem3(game, glob.LAYER_INIM, ex, ey)
            en.diff2()
            en.parent = mv
            en.flip(True, False)
            en.h_speed *= -1

    def make_enemy_level3():
        if random.randint(1, 100) < 50:
            ex = game.w - 50
            ey = game.h - 300
            en = Enem3(game, glob.LAYER_INIM, ex, ey)
            en.diff2()
            en.parent = mv
        else:
            ex = 0
            ey = game.h - 300
            en = Enem3(game, glob.LAYER_INIM, ex, ey)
            en.diff3()
            en.parent = mv
            en.flip(True, False)
            en.h_speed *= -1

    running = True

    music = SoundBox("public_domain_upbeatoverworld.wav").loop_music().set_volume(glob.vol_music)

    # PLAYER
    # -----------------------------------------
    player = Player(game, glob.LAYER_PLAYER, glob.WIDTH // 2 - 80, 100)

    # BACKGROUNDS
    # -----------------------------------------
    bk = ImageSet()
    bk.add("patcheshugh_backgrnd-3.png")
    rb1 = bk.get(0).get_image().get_rect()
    rb2 = bk.get(0).get_image().get_rect()
    rb1.left = 0
    rb2.left = rb1.right

    # ESPECIAL ACTOR TO CAPTURE PLAYER MOVMENT
    # -----------------------------------------
    mv = Actor(game, 0, 0, 0)

    pygame.time.set_timer(glob.EV_SCORE, 300, True)
    pygame.time.set_timer(glob.EV_NEW_ENEMY, 2000, True)

    level = 1
    time_passed = 0
    time_level = 1000

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
                    state = glob.ST_TITLE
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player.image_index += 1

            if event.type == glob.EV_SCORE:
                score += 1
                set_timer(glob.EV_SCORE, 300, True)

            if event.type == glob.EV_NEW_ENEMY:
                set_timer(glob.EV_NEW_ENEMY, 5000, True)
                if level == 1:
                    make_enemy_level1()
                if level == 2:
                    make_enemy_level2()
                if level > 2:
                    make_enemy_level3()

        mv.h_speed = -player.h_speed
        mv.v_speed = -player.v_speed

        buffer.blit(bk.get(0).get_image(), rb1)
        buffer.blit(bk.get(0).get_image(), rb2)

        rb1.left -= mv.h_speed * -1
        rb2.left -= mv.h_speed * -1

        if rb1.left > 0:
            rb1.left = 0
            mv.h_speed = 0
            rb2.left = rb1.right

        if rb2.right <= glob.WIDTH:
            mv.h_speed = 0
            rb1.left = rb2.left
            rb2.left = rb1.right

        game.update_all()
        game.draw_all(buffer)

        draw_hud(buffer)

        screen.blit(buffer, (0, 0))
        pygame.display.flip()

        time_passed += 1
        if time_passed > time_level:
            time_level += 1000
            level += 1

        clock.tick(glob.FPS)


def draw_hud(surface: Surface):
    global score
    global lives

    base = 50
    txt_lives.draw_xy(surface, base + 100, game.h - 70)
    w = heart_img.get_width()
    for live in range(1, lives + 1):
        x = (base + 100 + 60) + live * (w + 4)
        y = glob.HEIGHT - 55
        surface.blit(heart_img, (x, y))

    txt_ammo.draw_xy(surface, base + 400, game.h - 70)
    txt_ammov.draw_xy(surface, base + 520, game.h - 70)

    txt_score.draw_xy(surface, base + 680, game.h - 70)
    txt_scorev.set_text(str.format("{0:05d}", score))
    txt_scorev.draw_xy(surface, base + 800, game.h - 70)

    txt_debug.set_text(str.format("{0:03.2f}", clock.get_fps()))
    txt_debug.draw_xy(surface, base + 0, game.h - 70)


def state_gameover():
    global state

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music.fadeout(1500)
                state = glob.ST_PLAYING
                return


def finish():
    global music
    music.unload()
    pygame.quit()
    exit()


manage_states()
