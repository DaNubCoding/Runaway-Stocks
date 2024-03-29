from pathlib import Path
from enum import Enum
import pygame
import os

_pair = tuple[int, int]
_color = tuple[int, int, int]
_font = pygame.font.FontType

FPS = float("inf")
VEC = pygame.math.Vector2
WIDTH, HEIGHT = 828, 512
BULL_COLOR = (21, 153, 53)
BEAR_COLOR = (214, 73, 73)
BG_BULL_COLOR = (11, 93, 23)
BG_BEAR_COLOR = (134, 33, 33)
CENTER = VEC(WIDTH // 2, HEIGHT // 2)
GRID_SPACE = VEC(48, 30)
BG_GRID_SPACE = GRID_SPACE * 0.78
BG_PARALLAX = 0.85
SHADOW_OFFSET = VEC(3, 4)
MUSIC_VOLUME = 0.08
MIN_BLUR_THRESHOLD = 0.5

DATA_DIR = os.path.join(str(Path.home()), ".runawaystocks")
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
HIGHSCORE_FILE = os.path.join(DATA_DIR, "highscore.txt")

class Dir(Enum):
    UP = -1
    DOWN = 1

class Anchors(Enum):
    TOP = VEC(0, -1)
    BOTTOM = VEC(0, 1)
    LEFT = VEC(-1, 0)
    RIGHT = VEC(1, 0)
    CENTER = VEC(0, 0)
    TOPLEFT = VEC(-1, -1)
    TOPRIGHT = VEC(1, -1)
    BOTTOMLEFT = VEC(-1, 1)
    BOTTOMRIGHT = VEC(1, 1)

pygame.font.init()
FONTS = [pygame.font.SysFont("centurygothic", size) for size in range(1, 121)]
BOLD_FONTS = [pygame.font.SysFont("centurygothic", size, True) for size in range(1, 121)]