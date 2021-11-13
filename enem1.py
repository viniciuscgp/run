import math
import random
from typing import Any
from xretro.retroimages import ImageSet
from xretro.retroactor import Actor
from xretro.retrogame import Game
import os


class Enem1(Actor):
    def __init__(self, game: Game, layer: int, x, y):
        super().__init__(game, layer, x, y)

        img_set = ImageSet()
        for i in range(1, 7):
            img_set.add(os.path.join("enemy", "enem2", "frame{}.png").format(i))

        img_set.zoom(0.1)
        self.animations.add(img_set)
        self.h_speed = random.choice((-2, -3, -4))
        self.image_speed = abs(self.h_speed) / 10

    def update(self, *args: Any, **kwargs: Any):
        super().update(*args, **kwargs)
        if self.rect.right < 0 or self.rect.left > self.game.w:
            self.destroy()


