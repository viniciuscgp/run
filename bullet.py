from typing import Any

import glob
import xretro.retroutility
from xretro.retroimages import ImageSet
from xretro.retroactor import Actor
from xretro.retrogame import Game
import os


class Bullet(Actor):
    def __init__(self, game: Game, layer: int, x, y):
        super().__init__(game, layer, x, y)

        bullet_set = ImageSet()
        for i in range(0, 1):
            bullet_set.add(os.path.join("Soldier-Guy", "_Weapon", "Bullet.png"))
        bullet_set.zoom(0.3)
        bullet_set.get(0).get_image().set_colorkey(0)
        self.animations.add(bullet_set)
        self.attack = 3

    def update(self, *args: Any, **kwargs: Any):
        super().update(*args, **kwargs)
        if self.rect.right < 0 or self.rect.left > self.game.w:
            self.destroy()

        lscoll = self.game.is_colliding(self, glob.LAYER_INIM)
        for ac in lscoll:
            self.game.analise_atk(self, ac)

    def on_outofscreen(self):
        self.kill()

