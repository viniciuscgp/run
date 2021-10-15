# The Gunman - Day of fury
from random import random

import pygame

from ClasseAtor import Ator
from ClasseJogador import Jogador
from ClassePalco import Palco

# Exemplos que podemos usar ratios: 1.777777778 (1280x720) 1.333333333 (800x600) 1.6 (320x200)
RATIO = 1.777777778
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
palco = Palco()

pygame.display.set_caption("Gunman - Dia de Fúria")

# Adiciona o Jogador no Palco
jogador = Jogador(100, 100)
jogador.carrega_imagem("jogador00.png")
jogador.atrito = 0.1
jogador.gravidade = 1
jogador.gravidade_acel = 0.1

palco.adicionaAtor(jogador)

# Inimigo exemplo
inimigo = Ator(random() * WIDTH, random() * HEIGHT)
inimigo.carrega_imagem("jogador00.png")
palco.adicionaAtor(inimigo)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(FUNDO)

    palco.atualizaTudo()
    palco.desenhaTudo(screen)

    pygame.display.flip()

pygame.quit()
