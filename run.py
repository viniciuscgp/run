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
from ammo import Ammo

import os
import glob
import math

# Inicializa a pygame --------------------------
os.environ["PYGAME_BLEND_ALPHA_SDL2"] = "1"
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Jogo -----------------------------------------
game = Game("Corra que o Zé vem ai!", glob.WIDTH, glob.HEIGHT)

# Prepara --------------------------------------
screen = pygame.display.set_mode([game.w, game.h], flags=pygame.SCALED, vsync=1)
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

# buffer = Surface((glob.WIDTH, glob.HEIGHT))

snd_get_ammo = SoundBox(os.path.join("weapload.wav")).set_volume(glob.vol_effects * 3)

music: SoundBox
state = glob.ST_TITLE

game.lives = 0
game.ammo = 0
game.score = 0
game.alc = 0

# BACKGROUNDS
# -----------------------------------------
bk = ImageSet()
bk.add("patcheshugh_backgrnd-3.png")
rb1 = bk.get(0).get_image().get_rect()
rb2 = bk.get(0).get_image().get_rect()
rb1.left = 0
rb2.left = rb1.right


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

    game.reset()

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

        screen.blit(background.get(0).get_image(), pygame.Rect(0, 0, 0, 0))
        screen.blit(ze.get(0).get_image(), pygame.Rect(470, 220, 0, 0))

        txt_title.draw_xc(screen, game.h // 2 - 265)
        txt_title2.draw_xc(screen, game.h // 2 - 260)

        txt_push.draw_xc(screen, game.h // 2 + 40)

        screen.blit(screen, (0, 0))
        pygame.display.flip()
        clock.tick(glob.FPS)


def state_playing():
    global state
    global music

    game.lives = 3
    game.ammo = 50
    game.score = 0

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

    music = SoundBox("public_domain_upbeatoverworld.wav").loop_music().set_volume(glob.vol_music)

    # PLAYER
    # -----------------------------------------
    player = Player(game, glob.LAYER_PLAYER, glob.WIDTH // 2 - 80, 100)

    # ESPECIAL ACTOR TO CAPTURE PLAYER MOVMENT
    # -----------------------------------------
    mv = Actor(game, 0, 0, 0)

    # AMMOS
    # -----------------------------------------
    ammo_positions = [3500, 4500, 7500, 10000, 11000, 13000]
    for p in ammo_positions:
        ammo = Ammo(game, glob.LAYER_DROPS, p, 300)
        ammo.parent = mv

    # ------------------------------------------

    pygame.time.set_timer(glob.EV_SCORE, 300, 1)
    pygame.time.set_timer(glob.EV_NEW_ENEMY, 2000, 1)

    level = 1
    time_passed = 0
    time_level = 1500

    game.alc = 0

    running = True

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
                    player.destroy()
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player.image_index += 1

            if event.type == glob.EV_SCORE:
                game.score += 1
                set_timer(glob.EV_SCORE, 300, True)

            if event.type == glob.EV_NEW_ENEMY:
                set_timer(glob.EV_NEW_ENEMY, 2000, True)
                if level == 1:
                    make_enemy_level1()
                if level == 2:
                    make_enemy_level2()
                if level > 2:
                    make_enemy_level3()

            if event.type == glob.EV_PLAYER_DIE:
                print("EV_PLAYER_DIE")
                game.lives -= 1
                if game.lives > 0:
                    player = Player(game, glob.LAYER_PLAYER, glob.WIDTH // 2 - 80, 100)
                else:
                    state = glob.ST_GAME_OVER
                    return

            if event.type == glob.EV_PLAYER_FLASH:
                player.visible = not player.visible
                if player.tag < 15:
                    pygame.time.set_timer(glob.EV_PLAYER_FLASH, 100, 1)
                    player.tag += 1
                else:
                    player.visible = True
                    player.ghost = False

            if event.type == glob.EV_PLAYER_GET_AMMO:
                game.ammo += 50
                snd_get_ammo.play()

            if event.type == glob.EV_PLAYER_SCORE:
                game.score += event.value

        mv.h_speed = -player.h_speed
        mv.v_speed = -player.v_speed

        game.alc += player.h_speed

        screen.blit(bk.get(0).get_image(), rb1)
        screen.blit(bk.get(0).get_image(), rb2)

        rb1.left += math.trunc(mv.h_speed)
        rb2.left += math.trunc(mv.h_speed)

        if player.h_speed < 0:
            if rb1.left > 0:
                rb2.right = rb1.left

            if rb2.left > 0:
                rb1.right = rb2.left
        else:
            if rb2.right < game.w:
                rb1.left = rb2.right
            if rb1.right < game.w:
                rb2.left = rb1.right

        game.update_all()
        game.draw_all(screen)

        draw_hud(screen)

        pygame.display.flip()

        time_passed += 1
        if time_passed > time_level:
            time_level += 1000
            level += 1

        clock.tick(glob.FPS)


def draw_hud(surface: Surface):

    base = 50
    txt_lives.draw_xy(surface, base + 100, game.h - 70)
    w = heart_img.get_width()
    for live in range(1, game.lives + 1):
        x = (base + 100 + 60) + live * (w + 4)
        y = glob.HEIGHT - 55
        surface.blit(heart_img, (x, y))

    txt_ammo.draw_xy(surface, base + 400, game.h - 70)
    txt_ammov.set_text(str.format("{0:05d}", game.ammo))
    txt_ammov.draw_xy(surface, base + 520, game.h - 70)

    txt_score.draw_xy(surface, base + 680, game.h - 70)
    txt_scorev.set_text(str.format("{0:05d}", game.score))
    txt_scorev.draw_xy(surface, base + 800, game.h - 70)

    txt_debug.set_text(str.format("OBJ: {0:03.2f}", game.actor_count()))
    txt_debug.draw_xy(surface, 30, 30)

    txt_debug.set_text(str.format("FPS: {0:03.2f}", clock.get_fps()))
    txt_debug.draw_xy(surface, 200, 30)

    txt_debug.set_text(str.format("PT: {0:05f}", game.get_particles().count()))
    txt_debug.draw_xy(surface, 400, 30)

    txt_debug.set_text(str.format("ALC: {0:05f}", game.alc))
    txt_debug.draw_xy(surface, 600, 30)


def state_gameover():
    global state
    global music

    music = SoundBox(os.path.join("Music_by_Cleyton_Kauffman", "Farewell_mp3.mp3")).loop_music().set_volume(glob.vol_music)
    txt_gameover = Text("Changa-VariableFont_wght.ttf", "GAME OVER", 90, Color(255, 10, 67)).set_bold(True)
    game.reset()
    pygame.time.set_timer(glob.EV_GAME_OVER_RETURN, 10000, 1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    music.fadeout(1500)
                    state = glob.ST_TITLE
                    return
            if event.type == glob.EV_GAME_OVER_RETURN:
                music.fadeout(1500)
                state = glob.ST_TITLE
                return

        screen.blit(bk.get(0).get_image(), rb1)
        screen.blit(bk.get(0).get_image(), rb2)

        txt_gameover.draw_xc(screen, game.h // 2 - txt_gameover.txt_surf.get_height() // 2)
        draw_hud(screen)

        screen.blit(screen, (0, 0))
        pygame.display.flip()

        clock.tick(glob.FPS)


def finish():
    global music
    music.unload()
    pygame.quit()
    exit()


manage_states()
