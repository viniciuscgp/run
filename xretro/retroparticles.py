import pygame
import math
import random
from pygame import Surface
import pygame.gfxdraw
from xretro.retroconsts import Ptype
from xretro.retroutility import increment
from xretro.retroconsts import DEFAULT


class Particle(object):

    def __draw_dot(self, surf: Surface):
        surf.set_at((int(self.x), int(self.y)), self.color)
        pass

    def __draw_square(self, surf: Surface):
        pass

    def __draw_square_fill(self, surf: Surface):
        pass

    def __draw_circle(self, surf: Surface):
        pygame.gfxdraw.circle(surf, self.x, self.y, self.size, self.color)
        # pygame.draw.circle(surf, self.color, (self.x, self.y), self.size, 1)
        pass

    def __draw_circle_fill(self, surf: Surface):
        pygame.gfxdraw.filled_circle(surf, int(self.x), int(self.y), int(self.size), self.color)
        #  pygame.draw.circle(surf, self.color, (self.x, self.y), self.size, 0)
        pass

    def __draw_image(self, surf: Surface):
        pass

    def __init__(self, x, y, size, color: pygame.Color, ptype: Ptype):
        self.x = x
        self.y = y
        self.xold = self.x
        self.yold = self.y
        self.color = color
        self.type = ptype
        self.image = None
        self.controller = None

        self.xmax = DEFAULT
        self.xmin = DEFAULT
        self.ymax = DEFAULT
        self.ymin = DEFAULT

        # gravity
        self.grav = 0
        self.grav_inc = 0
        self.grav_min = DEFAULT
        self.grav_max = DEFAULT

        # size
        self.size = size
        self.size_min = DEFAULT
        self.size_max = DEFAULT
        self.size_inc = 0

        # life
        self.life = 0
        self.life_min = DEFAULT
        self.life_max = DEFAULT

        # speed
        self.speed = 0
        self.speed_min = DEFAULT
        self.speed_max = DEFAULT
        self.speed_inc = 0

        # direction 0..360
        self.dir = 0
        self.dir_min = DEFAULT
        self.dir_max = DEFAULT
        self.dir_inc = 0

        # alpha 0..255 max
        self.alpha_min = DEFAULT
        self.alpha_max = DEFAULT
        self.alpha_inc = 0

        self.draw = None

        if self.type == Ptype.PT_DOT:
            self.draw = Particle.__draw_dot

        elif self.type == Ptype.PT_SQUARE:
            self.draw = Particle.__draw_square

        elif self.type == Ptype.PT_SQUAREF:
            self.draw = Particle.__draw_square_fill

        elif self.type == Ptype.PT_CIRCLE:
            self.draw = Particle.__draw_circle

        elif self.type == Ptype.PT_CIRCLEF:
            self.draw = Particle.__draw_circle_fill

        else:
            self.draw = Particle.__draw_image

    def set_size(self, smin, smax, sinc):
        self.size_min = smin
        self.size_max = smax
        self.speed_inc = sinc
        self.size = random.randint(self.size_min, self.size_max)
        return self

    def set_life(self, lmin, lmax):
        self.life_min = lmin
        self.life_max = lmax
        self.life = random.randint(self.life_min, self.life_max)
        return self

    def set_speed(self, smin, smax, sinc):
        self.speed_min = smin
        self.speed_max = smax
        self.speed_inc = sinc
        self.speed = random.uniform(self.speed_min, self.speed_max)
        return self

    def set_dir(self, dmin, dmax, dinc):
        self.dir_min = dmin
        self.dir_max = dmax
        self.dir_inc = dinc
        self.dir = random.uniform(self.dir_min, self.dir_max)
        return self

    def set_alpha(self, amin, amax, ainc):
        # alpha 0..255
        self.alpha_min = amin
        self.alpha_max = amax
        self.alpha_inc = ainc
        self.color.a = random.randint(self.alpha_min, self.alpha_max)
        return self

    def set_gravity(self, gmin, gmax, ginc):
        self.grav_min = gmin
        self.grav_max = gmax
        self.grav_inc = ginc
        return self

    def set_xmax(self, xm):
        self.xmax = xm
        return self

    def set_xmin(self, xm):
        self.xmin = xm
        return self

    def set_ymax(self, ym):
        self.ymax = ym
        return self

    def set_ymin(self, ym):
        self.ymin = ym
        return self

    def update(self):

        self.xold = self.x
        self.yold = self.y

        self.x = self.x + math.cos(math.radians(self.dir)) * self.speed
        self.y = self.y - math.sin(math.radians(self.dir)) * self.speed
        self.y += self.grav

        if self.xmin != DEFAULT:
            if self.x < self.xmin:
                self.x = self.xold

        if self.xmax != DEFAULT:
            if self.x > self.xmax:
                self.x = self.xold

        if self.ymin != DEFAULT:
            if self.y < self.ymin:
                self.y = self.yold

        if self.ymax != DEFAULT:
            if self.y > self.ymax:
                self.y = self.yold

        if self.grav_inc != 0:
            self.grav = increment(self.grav, self.grav_inc, self.grav_min, self.grav_max)

        if self.speed_inc != 0:
            self.speed = increment(self.speed, self.speed_inc, self.speed_min, self.speed_max)

        if self.dir_inc != 0:
            self.dir = increment(self.dir, self.dir_inc, self.dir_min, self.dir_max)

        if self.alpha_inc != 0:
            self.color.a = increment(self.color.a, self.alpha_inc, 0, 255)

        if self.size_inc != 0:
            self.size = increment(self.size, self.size_inc, self.size_min, self.size_max)

        self.life -= 1

        if self.life <= 0:
            self.kill()

    def kill(self):
        self.controller.kill(self)


class ParticleController(object):
    def __init__(self):
        self.__particle_list = []
        pass

    def add(self, particle: Particle):
        particle.controller = self
        self.__particle_list.append(particle)

    def draw_all(self, surf: Surface):
        for p in self.__particle_list:
            p.draw(p, surf)

    def update_all(self):
        for p in self.__particle_list:
            p.update()

    def add_bulk(self, particle: Particle, number):
        for i in range(1, number):
            self.add(particle)

    def count(self):
        return len(self.__particle_list)

    def kill(self, particle: Particle):
        self.on_die()
        self.__particle_list.remove(particle)

    def on_die(self):
        pass
