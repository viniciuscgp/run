from typing import Any
from xretro.retroimages import ImageSet
from xretro.retroactor import Actor
from xretro.retrogame import Game
import os


class Shell(Actor):
    def __init__(self, game: Game, layer: int, x, y):
        super().__init__(game, layer, x, y)

        bullet_set = ImageSet()
        for i in range(0, 1):
            bullet_set.add(os.path.join("guns_gameassets", "PNG", "small_bullet4.png"))
        bullet_set.zoom(0.4)
        self.animations.add(bullet_set)
        self.fric = 0.1
        self.grav_vel = 2.0
        self.grav_acel = 2
        self.ymax = 450
        self.angle_speed = 15

    def update(self, *args: Any, **kwargs: Any):
        super().update(*args, **kwargs)

        if self.rect.right < 0 or self.rect.left > self.game.w:
            self.destroy()
