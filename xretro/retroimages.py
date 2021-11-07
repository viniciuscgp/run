import pygame
import os
from xretro import retroutility
from pygame import Surface


class ImageSingle(object):
    def __init__(self, img: Surface):
        self.img: Surface = img
        self.img_copy: Surface = img.copy()
        self.aspect = self.img.get_height() / self.img.get_width()
        self.hflip = False
        self.vflip = False

    def get_image(self):
        return self.img

    def scale(self, w: int, h: int):
        self.img = pygame.transform.scale(self.img, (w, h))
        self.img_copy = self.img.copy()

    def scale_nice(self, w: int):
        self.img = pygame.transform.scale(self.img, (w, w * self.aspect))
        self.img_copy = self.img.copy()

    def zoom(self, z: float):
        w = self.img.get_width()
        h = self.img.get_height()
        self.img = pygame.transform.scale(self.img, (w * z, h * z))
        self.img_copy = self.img.copy()

    def flip(self, hflip, vflip):
        if self.hflip != hflip or self.vflip != vflip:
            self.img = self.img_copy.copy()
            self.img = pygame.transform.flip(self.img, hflip, vflip)
            self.hflip = hflip
            self.vflip = vflip

    def copy_from(self, surf: Surface):
        self.img = surf.copy()


class ImageSet(object):
    def __init__(self):
        self.images = []  # a list of ImageSingle objects

    def add(self, file):
        img = pygame.image.load(os.path.join(retroutility.images_folder(), file))
        image_single = ImageSingle(img)
        self.images.append(image_single)

    def get(self, index: int) -> ImageSingle:
        return self.images[index]

    def remove(self, index: int):
        self.images.pop(index)

    def count(self):
        return len(self.images)

    def copy_from(self, index: int, surf: Surface):
        self.images[index].copy_from(surf)

    def zoom(self, z: float):
        for img in self.images:
            img.zoom(z)

    def flip(self, hflip, vflip):
        for img in self.images:
            img.flip(hflip, vflip)


class AnimSet(object):
    def __init__(self):
        self.sets = []

    def add(self, imgset: ImageSet):
        self.sets.append(imgset)

    def get(self, index: int) -> ImageSet:
        return self.sets[index]

    def remove(self, index: int):
        self.sets.pop(index)

    def count(self):
        return len(self.sets)
