import pygame.draw
from pygame import Rect
from pygame.surface import Surface
from xretro.retroparticles import ParticleController, Particle, Ptype


class Game:

    def __init__(self, title, w, h):
        self.title = title
        self.w = w
        self.h = h
        self.layers = {}
        self.__particle_control = ParticleController()

    def add_actor(self, actor, lay: int):
        if self.layers.get(lay) is None:
            self.layers[lay] = list()
        self.layers.get(lay).append(actor)
        actor.game = self

    def update_all(self):
        for la in self.layers:
            for actor in self.layers[la]:
                actor.update()
        self.__particle_control.update_all()

    def draw_all(self, surf: Surface):
        for la in self.layers:
            for actor in self.layers[la]:
                surf.blit(actor.image, actor.rect)
        self.__particle_control.draw_all(surf)

    def draw_all_debug(self, surf: Surface):
        for la in self.layers:
            for actor in self.layers[la]:
                surf.blit(actor.image, actor.rect)
                pygame.draw.rect(surf, (255, 255, 255), actor.rect, 3)
                pygame.draw.rect(surf, (55, 255, 255), actor.rect_c, 3)

    def kill_actor(self, actor):
        sprs: list = self.layers[actor.layer]
        try:
            sprs.remove(actor)
        except ValueError:
            pass

    def actor_count(self, layer: int = -1):
        total = 0
        for la in self.layers:
            if layer != -1:
                if la == layer:
                    sprs: list = self.layers[la]
                    total += len(sprs)
            else:
                sprs: list = self.layers[la]
                total += len(sprs)

        return total

    def is_colliding(self, actor, layer: int):
        collide_list = []
        try:
            sprs = self.layers[layer]
        except KeyError:
            return []

        for other in sprs:
            if actor.rect_c.colliderect(other.rect_c):
                collide_list.append(other)

        return collide_list

    def get_particles(self):
        return self.__particle_control

    @staticmethod
    def analise_atk(actor1, actor2):
        actor1.defense -= actor2.attack
        actor2.defense -= actor1.attack
        if actor1.defense <= 0:
            actor1.destroy()
        else:
            actor1.on_hit(actor2)

        if actor2.defense <= 0:
            actor2.kill()
        else:
            actor2.on_hit(actor1)

        return actor1.defense - actor2.defense

    @staticmethod
    def scale_rect(rect, amount: float = 1):
        c = rect.center
        w = rect.width * amount
        h = rect.height * amount
        new = Rect(0, 0, w, h)
        new.center = c
        return new
