from typing import Any

import pygame

from xretro.ClassActor import Actor


class Player(Actor):
    RIGHT = 3
    LEFT = 7

    def __init__(self, group, x, y):
        super().__init__(group, x, y)
        self.facing = 0
        self.onfloor = False

    def update(self, *args: Any, **kwargs: Any):

        super().update(*args, **kwargs)

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            if self.facing != Player.LEFT or self.anim_index != 1:
                self.image_speed = 0.25
                self.image_index = 0
                self.facing = Player.LEFT
                if self.onfloor:
                    self.anim_index = 1
            self.h_vel = -3

        if teclas[pygame.K_RIGHT]:
            if self.facing != Player.RIGHT or self.anim_index != 1:
                self.image_speed = 0.25
                self.image_index = 0
                self.facing = Player.RIGHT
                if self.onfloor:
                    self.anim_index = 1
            self.h_vel = 3

        if teclas[pygame.K_UP] and self.onfloor:
            self.grav_vel = -8
            self.anim_index = 2
            self.image_index = 0
            self.onfloor = False

        if self.h_vel == 0 and self.onfloor:
            self.anim_index = 0
            self.image_speed = 0.15

        if self.rect.bottom >= self.ymax:
            self.onfloor = True

        if self.facing == Player.RIGHT:
            self.flip(False, False)
        else:
            self.flip(True, False)
