from typing import Sequence, Union

import pygame
from pygame import Surface
from pygame.sprite import Sprite


class Grupo(pygame.sprite.Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]):
        super().__init__(*sprites)

    def adicionaAtor(self, ator):
        self.add(ator)
        ator.group = self
        pass

    def desenhaTudo(self, surface: Surface):
        self.draw(surface)

    def atualizaTudo(self, *args, **kwargs):
        self.update(self, args, kwargs)
