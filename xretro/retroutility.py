# Pastas importantes
import os

import xretro.retroconsts


def get_root():
    filepath = os.path.dirname(__file__)
    return os.path.join(filepath, "..")


def images_folder():
    return os.path.join(get_root(), "images")


def sounds_folder():
    return os.path.join(get_root(), "sounds")


def fonts_folder():
    return os.path.join(get_root(), "fonts")


def signal(valor):
    if valor < 0:
        return -1
    elif valor == 0:
        return 0
    else:
        return 1


def consume(valor, fric):
    if fric == 0:
        return valor

    sinal = signal(valor)
    valor = abs(valor)

    if abs(valor) > 0:
        valor -= fric
        if valor < 0:
            valor = 0
    return valor * sinal


def increment(v, inc, vmin, vmax):
    old = v
    v += inc
    if vmin != xretro.retroconsts.DEFAULT:
        if v < vmin:
            return old
    if vmax != xretro.retroconsts.DEFAULT:
        if v > vmax:
            return old
    return v
