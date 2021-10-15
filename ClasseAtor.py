from typing import Any

import pygame

from pygame import Rect, sprite

from utilitarios import gasta_forca

import os

# Pastas importantes
pasta_jogo = os.path.dirname(__file__)
pasta_img = os.path.join(pasta_jogo, "imagens")


class Ator(sprite.Sprite):
    def __init__(self, x, y):
        super(Ator, self).__init__()
        self.rect = Rect(x, y, 10, 10)

        self.gravidade = 0  # forca gravitacional
        self.gravidade_acel = 0  # aceleracao gravitacional
        self.gravidade_max = 6  # maxima da forca de gravidade

        self.atrito = 0  # forca posta as forcas horizontais e verticais
        self.h_forca = 0  # forca horizontal
        self.v_forca = 0  # forca vertical
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.h_forca, self.v_forca)
        self.rect.move_ip(0, self.gravidade)

        self.h_forca = gasta_forca(self.h_forca, self.atrito)
        self.v_forca = gasta_forca(self.v_forca, self.atrito)

        if self.gravidade < self.gravidade_max:
            self.gravidade += self.gravidade_acel

        super().update(*args, **kwargs)

    def carrega_imagem(self, arquivo):
        self.image = pygame.image.load(os.path.join(pasta_img, arquivo))
        # self.image.set_colorkey((1, 1, 1))
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
