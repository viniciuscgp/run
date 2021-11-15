from xretro.retroactor import Actor
from xretro.retrogame import Game
from xretro.retroimages import ImageSet
from pygame.event import Event
import pygame
import glob
import os


class Ammo(Actor):
    def __init__(self, game: Game, layer: int, x, y):
        super().__init__(game, layer, x, y)

        ammo_image = ImageSet()
        ammo_image.add(os.path.join("guns_gameassets", "PNG", "ammobox.png"))
        ammo_image.zoom(0.3)

        self.animations.add(ammo_image)
        self.grav_speed = 2.8
        self.grav_acel = 0.45
        self.fric = 0
        self.ymax = 450
        self.defense = 0
        self.attack = 0

    def on_killed(self):
        pygame.event.post(Event(glob.EV_PLAYER_GET_AMMO))


