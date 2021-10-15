from typing import Any

import pygame

from ClasseAtor import Ator


class Jogador(Ator):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, *args: Any, **kwargs: Any):

        super().update(*args, **kwargs)

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            self.h_forca = -4

        if teclas[pygame.K_RIGHT]:
            self.h_forca = 4

        if teclas[pygame.K_UP]:
            self.v_forca = -10

        if teclas[pygame.K_DOWN]:
            self.v_forca = 4

        lista_colisoes = pygame.sprite.spritecollide(
            self, self.group, False, None)

        for sprite in lista_colisoes:
            if self != sprite:
                sprite.kill()
