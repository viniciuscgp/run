# Run - Day of fury
from random import random

import pygame

from ClassActor import Actor
from ClassGame import Game
from ClassPlayer import Player
from ClassText import Text
from pygame.time import Clock
from pygame.sprite import Group
from pygame import Rect

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

# --------------------JOGADOR----------------------
player = Player(stage, 100, 100)
player.load_imagem("jogador00.png")
player.fric = 0.1
player.grav = 1
player.grav_acel = 0.1

# -------------------INIMIGO-----------------------
enemy = Actor(stage, random() * WIDTH, random() * HEIGHT)
enemy.load_imagem("jogador00.png")

# -------------------TEXTOS------------------------
title = Text("Changa-VariableFont_wght.ttf", game.title, 60, "Yellow").set_bold(False)
title2 = Text("Changa-VariableFont_wght.ttf", game.title, 60, "Yellow").set_bold(True)


def state_title():
    running = True
    seconds = 15
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state_playing()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        screen.fill(FUNDO)
        title.draw_c(screen)
        title2.draw_xc(screen, 10)

        pygame.display.flip()
        clock.tick(FPS)


def state_gameover():
    pass


def state_playing():
    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(FUNDO)

        stage.update()
        stage.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


state_title()

pygame.quit()
