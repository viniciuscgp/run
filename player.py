import random

import pygame
import os
from typing import Any
from xretro.retroactor import Actor
from xretro.retroimages import ImageSet
from xretro.retrogame import Game
from xretro.retrosounds import SoundBox
import glob
from bullet import Bullet
from shell import Shell


class Player(Actor):
    RIGHT = 3
    LEFT = 7

    def shot_finished(self: Actor):
        if self.anim_index == 3:
            self.shoting = False

    def bullet_outofscreen(self: Actor):
        self.kill()

    def __init__(self, game: Game, layer: int, x, y):
        super().__init__(game, layer, x, y)
        self.facing = Player.RIGHT
        self.onfloor = False
        self.shoting = False
        self.on_animation_end = Player.shot_finished

        # PLAYER ANIMATIONS-----------------------------
        player_idle = ImageSet()
        for i in range(0, 10):
            player_idle.add(os.path.join("Soldier-Guy", "_Mode-Gun", "01-Idle", "E_E_Gun__Idle_{0:03n}.png".format(i)))
        player_idle.zoom(0.3)

        player_run = ImageSet()
        for i in range(0, 10):
            player_run.add(os.path.join("Soldier-Guy", "_Mode-Gun", "02-Run", "E_E_Gun__Run_000_{0:03n}.png".format(i)))
        player_run.zoom(0.3)

        player_jump = ImageSet()
        for i in range(0, 1):
            player_jump.add(os.path.join("Soldier-Guy", "_Mode-Gun", "05-Jump", "E_E_Gun__Jump_{0:03n}.png".format(i)))
        player_jump.zoom(0.3)

        player_shot = ImageSet()
        for i in range(0, 10):
            player_shot.add(
                os.path.join("Soldier-Guy", "_Mode-Gun", "03-Shot", "E_E_Gun__Attack_{0:03n}.png".format(i)))
        player_shot.zoom(0.3)

        self.animations.add(player_idle)
        self.animations.add(player_run)
        self.animations.add(player_jump)
        self.animations.add(player_shot)

        self.fric = 0.2
        self.grav_vel = 2.8
        self.grav_acel = 0.45
        self.ymax = 450
        self.xmin = 200
        self.xmax = game.w - 200
        self.image_speed = 0.15

        self.shoot = SoundBox(os.path.join("q009", "shotgun.ogg")).set_volume(glob.vol_effects)
        self.jump = SoundBox(os.path.join("public_domain_Jump2.wav")).set_volume(glob.vol_effects)

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
            self.jump.play()

        if teclas[pygame.K_SPACE] and not self.shoting:
            self.anim_index = 3
            self.image_index = 0
            self.image_speed = 0.50
            self.shoting = True
            bullet = Bullet(self.game, 0, 0, self.get_y() + self.rect.height // 2 + 12)
            shell = Shell(self.game, 0, 0, self.get_y() + self.rect.height // 2 + 12)

            if self.facing == Player.LEFT:
                bullet.h_vel = -10
                bullet.set_x(self.get_x() - 10)
                shell.set_x(self.get_x() + 50)
                shell.animations.get(shell.anim_index).rotate(90)
                shell.h_vel = random.choice([3, 4, 5])
            else:
                bullet.h_vel = 10
                bullet.set_x(self.get_x() + 130)
                shell.set_x(self.get_x() + 80)
                shell.animations.get(shell.anim_index).rotate(-90)
                shell.h_vel = -random.choice([3, 4, 5])

            shell.ttl = 60
            shell.v_vel = -8

            self.shoot.play()

        if self.rect.bottom >= self.ymax:
            self.onfloor = True

        if self.h_vel == 0 and self.v_vel == 0 and self.onfloor and not self.shoting:
            self.anim_index = 0
            self.image_speed = 0.15

        if self.facing == Player.RIGHT:
            self.flip(False, False)
        else:
            self.flip(True, False)
