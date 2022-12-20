import os
import sys
import pygame

CELL_SIZE = 150, 100
WALL_SIZE = 150, 300
CHAR_W = 200
CHAR_H = 200
FPS = 30
SPEED = 50
WINDOW_W = 1920
WINDOW_H = 1080
BACKGROUND_COLOR = (10, 10, 10)


def load_image(name, colorkey=None):
    fullname = os.path.join('..', 'resources', 'img', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image