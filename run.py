# The Gunman - Day of fury
from random import random

import pygame

from ClassActor import Actor
from ClassPlayer import Player

RATIO = 1.777777778  # Exemplos que podemos usar ratios: 1.777777778 (1280x720) 1.333333333 (800x600) 1.6 (320x200)
HEIGHT = 600
WIDTH = HEIGHT * RATIO
FPS = 60

# Algumas cores utilizadas no jogo
FUNDO = (45, 66, 178)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Inicializa a pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Prepara
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
stage = pygame.sprite.Group()

pygame.display.set_caption("Corre Zé, corre!")

# --------------------JOGADOR----------------------
player = Player(stage, 100, 100)
player.load_imagem("jogador00.png")
player.fric = 0.1
player.grav = 1
player.grav_acel = 0.1

# -------------------INIMIGO-----------------------
enemy = Actor(stage, random() * WIDTH, random() * HEIGHT)
enemy.load_imagem("jogador00.png")

# -------------------

# -------------------
font1 = pygame.font.Font("./fontes/Changa-VariableFont_wght.ttf", 50)
title_text = font1.render("Corre Zé, corre!", True, "White")
title_rect = title_text.get_rect(centerx=WIDTH / 2, centery=HEIGHT / 2)


def state_title():
    running = True
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

        screen.fill((156, 150, 20))

        screen.blit(title_text, title_rect.midtop)

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

        screen.blit(title_text, (30, 30))

        pygame.display.flip()

        clock.tick(FPS)


state_title()

pygame.quit()
