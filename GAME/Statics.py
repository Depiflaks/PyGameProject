import pygame
import os
import sys
from Consts import *

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


def changeSize(obj, size):
    obj.image = pygame.transform.scale(obj.image, size)
    #obj.rect.y = obj.y - size[1] + CELL_SIZE[1]

ticks = 0
clock = pygame.time.Clock()
characters = pygame.sprite.Group()

player_data1 = [pygame.image.load("../resources/img/characters/1/idle.png"), pygame.image.load(
    "../resources/img/characters/1/idleUp.png"), pygame.image.load("../resources/img/characters/1/idleDown.png"), [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], [pygame.image.load(
    "../resources/img/characters/1/up.png"), 1, 4],
                [pygame.image.load("../resources/img/characters/1/down.png"), 1, 4], [pygame.image.load(
        "../resources/img/characters/1/leftRight.png"), 4, 1]]
player_data2 = [pygame.image.load("../resources/img/characters/2/idle.png"), pygame.image.load(
    "../resources/img/characters/2/idleUp.png"), pygame.image.load("../resources/img/characters/2/idleDown.png"), [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], [pygame.image.load(
    "../resources/img/characters/2/up.png"), 1, 4],
                [pygame.image.load("../resources/img/characters/2/down.png"), 1, 4], [pygame.image.load(
        "../resources/img/characters/2/leftRight.png"), 4, 1]]
