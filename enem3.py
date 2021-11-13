import math
import random
from typing import Any
from xretro.retroimages import ImageSet
from xretro.retroactor import Actor
from xretro.retrogame import Game
from xretro.retroparticles import Particle
from xretro.retroconsts import Ptype
from xretro.retrosounds import SoundBox
import glob
from pygame import Color
import os


class Enem3(Actor):
    def __init__(self, game: Game, layer: int, x, y):
        super().__init__(game, layer, x, y)

        img_set = ImageSet()
        for i in range(1, 11):
            img_set.add(os.path.join("enemy", "enem3", "EnemyPlatform{:02d}.png").format(i))

        self.snd_hit = SoundBox(os.path.join("80-CC0-creature-SFX", "ooh.ogg"))
        self.snd_die = SoundBox(os.path.join("80-CC0-creature-SFX", "burble_01.ogg"))

        self.animations.add(img_set)
        self.grav_vel = 2.0
        self.grav_acel = 2
        self.ymax = 450
        self.collision_scale = 0.6

    def diff1(self):
        self.h_speed = -6
        self.image_speed = 0.6
        self.defense = 2
        self.animations.get(0).zoom(0.1)

    def diff2(self):
        self.h_speed = -5
        self.image_speed = 0.4
        self.defense = 3
        self.animations.get(0).zoom(0.2)

    def diff3(self):
        self.h_speed = -4
        self.image_speed = 0.2
        self.defense = 4
        self.animations.get(0).zoom(0.3)

    def update(self, *args: Any, **kwargs: Any):
        super().update(*args, **kwargs)
        if self.rect.right < 0 or self.rect.left > self.game.w:
            self.destroy()

    def on_hit(self, other):
        self.add_x(other.h_speed * 3)
        self.snd_hit.play()

    def on_killed(self):
        self.snd_die.play()
        z = 1 + self.animations.get(0).get(0).get_zoom()
        for i in range(1, int(50 * z)):
            x = self.get_x() + self.rect.w // 2
            y = self.get_y() + self.rect.h // 2
            self.game.get_particles().add(Particle(x, y, 5, Color(255, 40, 33), Ptype.PT_CIRCLEF)
                   .set_life(10, 30)
                   .set_dir(0, 360, 1)
                   .set_speed(1, 2, 0.3)
                   .set_size(int(z * 2), int(z * 6), 1)
                   .set_alpha(100, 200, -1)
                   .set_gravity(1, 3, 2)
                   .set_ymax(455))



