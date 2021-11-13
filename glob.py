from pygame import math
from pygame.draw_py import floor
from pygame import USEREVENT

RATIO = 1.777777778  # Exemplos que podemos usar ratios: 1.777777778 (1280x720) 1.333333333 (800x600) 1.6 (320x200)
HEIGHT = 600
WIDTH = floor(HEIGHT * RATIO)
FPS = 60

ST_TITLE = 1
ST_PLAYING = 2
ST_GAME_OVER = 3
ST_CREDITS = 4

EV_PUSH = USEREVENT
EV_SCORE = EV_PUSH + 1
EV_NEW_ENEMY = EV_SCORE + 1

LAYER_PLAYER = 0
LAYER_INIM = 1

vol_music = 0.06
vol_effects = 0.04
