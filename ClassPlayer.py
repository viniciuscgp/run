from typing import Any

import pygame

from xretro.ClassActor import Actor


class Player(Actor):
    def __init__(self, group, x, y):
        super().__init__(group, x, y)

    def update(self, *args: Any, **kwargs: Any):

        super().update(*args, **kwargs)

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            self.h_vel = -4
            self.flip(True, False)
            self.anim_index = 1
            self.image_speed = 0.25

        if teclas[pygame.K_RIGHT]:
            self.h_vel = 4
            self.flip(False, False)
            self.anim_index = 1
            self.image_speed = 0.25

        if self.h_vel == 0:
            self.anim_index = 0
            self.image_speed = 0.15

        if teclas[pygame.K_UP] and self.get_r().bottom == self.ymax:
            self.grav_vel = -8

        collision_list = pygame.sprite.spritecollide(
            self, self.grp, False, None)

        for sprite in collision_list:
            if self != sprite:
                sprite.kill()
