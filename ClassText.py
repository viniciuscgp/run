import os

import pygame
import consts
from pygame import Rect
from pygame import Surface
from pygame import Color

class Text:
    def __init__(self, fontname: str, text: str, size: int, color: Color) -> None:
        self.file = os.path.join(consts.ROOT_FOLDER, "fonts", fontname)
        self.size = size
        self.color = color
        self.text = text
        self.font = pygame.font.Font(self.file, self.size)
        self.txt_surf = self.font.render(self.text, True, self.color)

    def draw(self, draw_surf: Surface, r: Rect):
        draw_surf.blit(self.txt_surf, r)

    def draw_xy(self, draw_surf: Surface, x: int, y: int):
        draw_surf.blit(self.txt_surf, Rect(x, y, 0, 0))

    def draw_xc(self, draw_surf: Surface, y: int):
        x = (draw_surf.get_width() - self.txt_surf.get_width()) // 2
        draw_surf.blit(self.txt_surf, Rect(x, y, 0, 0))

    def draw_yc(self, draw_surf: Surface, x: int):
        y = (draw_surf.get_height() - self.txt_surf.get_height()) // 2
        draw_surf.blit(self.txt_surf, Rect(x, y, 0, 0))

    def draw_c(self, draw_surf: Surface):
        x = (draw_surf.get_width() - self.txt_surf.get_width()) // 2
        y = (draw_surf.get_height() - self.txt_surf.get_height()) // 2
        draw_surf.blit(self.txt_surf, Rect(x, y, 0, 0))

    def set_text(self, newtext: str):
        self.txt_surf = self.font.render(newtext, True, self.color)
        return self

    def set_color(self, newcolor: Color):
        self.txt_surf = self.font.render(self.text, True, newcolor)
        return self

    def set_size(self, newsize: int):
        self.size = newsize
        self.font = pygame.font.Font(self.file, self.size)
        self.txt_surf = self.font.render(self.text, True, self.color)
        return self

    def set_bold(self, v: bool):
        self.font.set_bold(v)
        self.txt_surf = self.font.render(self.text, True, self.color)
        return self

    def set_italic(self, v: bool):
        self.font.set_bold(v)
        self.txt_surf = self.font.render(self.text, True, self.color)
        return self


