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


def re_layered(board, c1, c2):
    if c1.y > c2.y:
        board.change_layer(c2, 4)
        board.change_layer(c1, 5)
    else:
        board.change_layer(c1, 4)
        board.change_layer(c2, 5)


def changeSize(obj, size):
    obj.image = pygame.transform.scale(obj.image, size)
    # obj.rect.y = obj.y - size[1] + CELL_SIZE[1]


def rebase(board1, board2, c1, c2, single_screen):
    if single_screen:
        if c1.x > c2.x and board1.x == 0 - CELL_SIZE[0]:
            board1.x, board2.x, board1.center, board2.center = board2.x, board1.x, board2.center, board1.center
            board1.width, board2.width = board2.width, board1.width
        elif c1.x < c2.x and board1.x == (WINDOW_W - CELL_SIZE[0]) // 2:
            board1.x, board2.x, board1.center, board2.center = board2.x, board1.x, board2.center, board1.center
            board1.width, board2.width = board2.width, board1.width


def cut_sheet(data):
    sheet, columns, rows = data[0], data[1], data[2]
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames


ticks = 0
clock = pygame.time.Clock()
characters = pygame.sprite.Group()

player_data1 = [pygame.image.load("../resources/img/characters/1/idle.png"), pygame.image.load(
    "../resources/img/characters/1/idleUp.png"), pygame.image.load("../resources/img/characters/1/idleDown.png"),
                [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], [pygame.image.load(
        "../resources/img/characters/1/up.png"), 1, 4],
                [pygame.image.load("../resources/img/characters/1/down.png"), 1, 4], [pygame.image.load(
        "../resources/img/characters/1/leftRight.png"), 4, 1]]
player_data2 = [pygame.image.load("../resources/img/characters/2/idle.png"), pygame.image.load(
    "../resources/img/characters/2/idleUp.png"), pygame.image.load("../resources/img/characters/2/idleDown.png"),
                [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], [pygame.image.load(
        "../resources/img/characters/2/up.png"), 1, 4],
                [pygame.image.load("../resources/img/characters/2/down.png"), 1, 4], [pygame.image.load(
        "../resources/img/characters/2/leftRight.png"), 4, 1]]
loading = cut_sheet([pygame.image.load("../resources/img/loading.png"), 9, 1])
background = pygame.image.load("../resources/img/background.jpg")
intro = cut_sheet([pygame.image.load("../resources/intro/merge.jpg"), 9, 3])
shadow = pygame.image.load("../resources/img/characters/shadow.png")
