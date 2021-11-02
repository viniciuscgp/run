# Run - Day of fury
from random import random

import pygame

from xretro.ClassActor import Actor
from xretro.ClassGame import Game
from xretro.ClassPlayer import Player
from xretro.ClassText import Text
from pygame.time import Clock
from pygame.sprite import Group

RATIO = 1.777777778  # Exemplos que podemos usar ratios: 1.777777778 (1280x720) 1.333333333 (800x600) 1.6 (320x200)
HEIGHT = 600
WIDTH = HEIGHT * RATIO
FPS = 60

# Algumas cores utilizadas no jogo
FUNDO = (0, 0, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Inicializa a pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Jogo
game = Game("Corra que o Zé vem ai!", WIDTH, HEIGHT)

# Prepara
screen = pygame.display.set_mode([game.w, game.h])
clock = Clock()
stage = Group()

pygame.display.set_caption(game.title)

# -------------------TEXTOS-----------------------
title = Text("Changa-VariableFont_wght.ttf", game.title, 60, "Yellow").set_bold(True).set_italic(True)
push_space = Text("Changa-VariableFont_wght.ttf", "Push space key", 30, "White").set_bold(True).set_italic(True)

pygame.time.set_timer(pygame.USEREVENT, 300)


def state_title():
    running = True
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
                push_space.togle_visible()
                pygame.time.set_timer(pygame.USEREVENT, 300)

        screen.fill(FUNDO)

        title.draw_xc(screen, game.h // 2 - 200)
        push_space.draw_xc(screen, game.h // 2 + 30)

        pygame.display.flip()
        clock.tick(FPS)


def state_playing():
    running = True
    # -------------------JOGADOR----------------------
    player = Player(stage, 100, 100)
    player.load_imagem("jogador00.png")
    player.fric = 0.1
    player.grav = 1
    player.grav_acel = 0.1

    # -------------------INIMIGO----------------------
    enemy = Actor(stage, random() * WIDTH, random() * HEIGHT)
    enemy.load_imagem("jogador00.png")

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(FUNDO)

        stage.update()
        stage.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


def state_gameover():
    pass


state_title()
pygame.quit()
exit()
