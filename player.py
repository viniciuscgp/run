from typing import Any

import pygame

from xretro.retroactor import Actor
from bullet import Bullet


class Player(Actor):
    RIGHT = 3
    LEFT = 7

    def shot_finished(self: Actor):
        if self.anim_index == 3:
            self.shoting = False

    def bullet_outofscreen(self: Actor):
        self.kill()

    def __init__(self, group, game, x, y):
        super().__init__(group, game, x, y)
        self.facing = Player.RIGHT
        self.onfloor = False
        self.shoting = False
        self.on_animation_end = Player.shot_finished

    def update(self, *args: Any, **kwargs: Any):

        super().update(*args, **kwargs)

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] and not self.shoting:
            if self.facing != Player.LEFT or self.anim_index != 1:
                self.image_speed = 0.25
                self.image_index = 0
                self.facing = Player.LEFT
                if self.onfloor:
                    self.anim_index = 1
            self.h_vel = -3

        if teclas[pygame.K_RIGHT] and not self.shoting:
            if self.facing != Player.RIGHT or self.anim_index != 1:
                self.image_speed = 0.25
                self.image_index = 0
                self.facing = Player.RIGHT
                if self.onfloor:
                    self.anim_index = 1
            self.h_vel = 3

        if teclas[pygame.K_UP] and self.onfloor and not self.shoting:
            self.grav_vel = -8
            self.anim_index = 2
            self.image_index = 0
            self.onfloor = False

        if teclas[pygame.K_SPACE] and not self.shoting:
            self.anim_index = 3
            self.image_index = 0
            self.image_speed = 0.50
            self.shoting = True
            bullet = Bullet(self.grp, self.game, 0, self.get_y() + self.rect.height // 2 + 12)
            if self.facing == Player.LEFT:
                bullet.h_vel = -10
                bullet.set_x(self.get_x() - 10)
            else:
                bullet.h_vel = 10
                bullet.set_x(self.get_x() + 130)

        if self.rect.bottom >= self.ymax:
            self.onfloor = True

        if self.h_vel == 0 and self.v_vel == 0 and self.onfloor and not self.shoting:
            self.anim_index = 0
            self.image_speed = 0.15

        if self.facing == Player.RIGHT:
            self.flip(False, False)
        else:
            self.flip(True, False)

