from typing import Any
import math
from pygame import Rect
from pygame.sprite import DirtySprite

from xretro.retroutility import consume
from xretro.retroimages import AnimSet
from xretro.retroimages import ImageSet
from xretro.retrogame import Game
from pygame.surface import Surface


class Actor(DirtySprite):
    DEFAULT = 99999999999999

    def __init__(self, game: Game, layer: int, x: int, y: int):
        super().__init__()
        game.add_actor(self, layer)
        self.game = game
        self.visible = False
        self.image = Surface((2, 2))
        self.animations: AnimSet = AnimSet()

        self.image_index = 0
        self.image_speed = 0.0
        self.image_angle = 0

        self.anim_index = 0

        self.rect = Rect(x, y, 0, 0)

        self.grav_vel = 0  # forca gravitacional
        self.grav_acel = 0  # aceleracao gravitacional
        self.grav_max = 10  # maxima da forca de gravidade

        self.angle = 0
        self.angle_speed = 0

        self.fric = 0  # atrito posta as forcas horizontais e verticais
        self.h_vel = 0  # vel horizontal
        self.v_vel = 0  # vel vertical

        self.ymax = Actor.DEFAULT
        self.ymin = Actor.DEFAULT

        self.xmax = Actor.DEFAULT
        self.xmin = Actor.DEFAULT

        self.ttl = 0

        self.on_animation_end = None
        self.on_destroy = None
        self.on_outofscreen = None

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)

        self.rect.move_ip(self.h_vel, self.v_vel)
        self.rect.move_ip(0, self.grav_vel)

        self.h_vel = consume(self.h_vel, self.fric)
        self.v_vel = consume(self.v_vel, self.fric)

        if self.grav_vel < self.grav_max:
            self.grav_vel += self.grav_acel

        # Handles on_outofscreen Event
        if self.on_outofscreen is not None:
            r = Rect(0, 0, self.game.w, self.game.h)
            if not r.contains(self.rect):
                self.on_outofscreen(self)

        # Handles angles
        # -----------------------------------------------------
        if self.angle_speed != 0:
            self.angle += self.angle_speed

        # Handles animations
        # -----------------------------------------------------
        if self.animations.count() > self.anim_index:
            imgs: ImageSet = self.animations.get(self.anim_index)

            if self.image_index < imgs.count():
                if self.angle_speed == 0:
                    img_single = imgs.get(math.floor(self.image_index))
                else:
                    img_single = imgs.get(math.floor(self.image_index)).rotate(self.angle)

                self.image = img_single.get_image()
                self.visible = True
                self.rect.w = self.image.get_rect().w
                self.rect.h = self.image.get_rect().h

                if self.image_speed != 0:
                    self.image_index += self.image_speed
                    if self.image_index > imgs.count() - 1:
                        if self.on_animation_end is not None:
                            self.on_animation_end(self)
                        self.image_index = 0
                    if self.image_index < 0:
                        self.image_index = imgs.count() - 1



        # Handles Max and Min constraints
        # -----------------------------------------------------
        if self.ymax != Actor.DEFAULT:
            if self.rect.bottom > self.ymax:
                self.rect.bottom = self.ymax
                self.grav_vel = 0
                self.v_vel = 0

        if self.ymin != Actor.DEFAULT:
            if self.rect.y < self.ymin:
                self.rect.y = self.ymin
                self.grav_vel = 0
                self.v_vel = 0

        if self.xmax != Actor.DEFAULT:
            if self.rect.right > self.xmax:
                self.rect.right = self.xmax
                self.h_vel = 0

        if self.xmin != Actor.DEFAULT:
            if self.rect.x < self.xmin:
                self.rect.x = self.xmin
                self.h_vel = 0

        # Time to live
        # ---------------------------------------------
        if self.ttl > 0:
            self.ttl -= 1
            if self.ttl <= 0:
                self.destroy()

    def set_x(self, x):
        self.rect.x = x
        return self

    def set_y(self, y):
        self.rect.y = y
        return self

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)
        return self

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_r(self):
        return self.rect

    def flip(self, hflip, vflip):
        if self.animations.count() > self.anim_index:
            imgs: ImageSet = self.animations.get(self.anim_index)
            imgs.flip(hflip, vflip)

    def destroy(self):
        self.kill()
        if self.on_destroy is not None:
            self.on_destroy(self)
