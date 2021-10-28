from typing import Any

import pygame

from ClassActor import Actor


class Player(Actor):
    def __init__(self, group, x, y):
        super().__init__(group, x, y)

    def update(self, *args: Any, **kwargs: Any):

        super().update(*args, **kwargs)

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            self.h_vel = -4

        if teclas[pygame.K_RIGHT]:
            self.h_vel = 4

        if teclas[pygame.K_UP]:
            self.grav = -5


        collision_list = pygame.sprite.spritecollide(
            self, self.grp, False, None)

        for sprite in collision_list:
            if self != sprite:
                sprite.kill()
