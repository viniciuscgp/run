# The Gunman - Day of fury
from random import random

import pygame

from ClasseAtor import Ator
from ClasseJogador import Jogador
from ClasseGrupo import Grupo


RATIO = 1.777777778 # Exemplos que podemos usar ratios: 1.777777778 (1280x720) 1.333333333 (800x600) 1.6 (320x200)
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
grupo = Grupo()

pygame.display.set_caption("Gunman - Dia de Fúria")

#--------------------JOGADOR----------------------
jogador = Jogador(100, 100)
jogador.carrega_imagem("jogador00.png")
jogador.atrito = 0.1
jogador.gravidade = 1
jogador.gravidade_acel = 0.1

grupo.adicionaAtor(jogador)

#-------------------INIMIGO-----------------------
inimigo = Ator(random() * WIDTH, random() * HEIGHT)
inimigo.carrega_imagem("jogador00.png")
grupo.adicionaAtor(inimigo)

#-------------------
cidade = Ator(0, 0)
cidade.carrega_imagem("city_alucard.svg")
grupo.adicionaAtor(cidade)
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(FUNDO)

    grupo.atualizaTudo()
    grupo.desenhaTudo(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
