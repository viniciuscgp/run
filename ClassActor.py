from typing import Any
import pygame
from pygame import Rect, sprite

import consts
from utility import consume
import os
import utility


class Actor(sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.grp = group
        self.rect = Rect(x, y, 0, 0)

        self.grav = 0  # forca gravitacional
        self.grav_acel = 0  # aceleracao gravitacional
        self.grav_max = 6  # maxima da forca de gravidade

        self.fric = 0  # atrito posta as forcas horizontais e verticais
        self.h_vel = 0  # vel horizontal
        self.v_vel = 0  # vel vertical

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.h_vel, self.v_vel)
        self.rect.move_ip(0, self.grav)

        self.h_vel = consume(self.h_vel, self.fric)
        self.v_vel = consume(self.h_vel, self.fric)

        if self.grav < self.grav_max:
            self.grav += self.grav_acel

        super().update(*args, **kwargs)

    def set_x(self, x):
        self.rect.x = x

    def set_y(self, y):
        self.rect.y = y

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def load_imagem(self, arquivo):
        self.image = pygame.image.load(os.path.join(consts.ROOT_FOLDER, "images", arquivo))
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
