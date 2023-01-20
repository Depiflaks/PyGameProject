import os
import sys
import sqlite3
import csv

from Character import *
from Statics import *
from Consts import *
import pygame

"""
Класс для описания игрового поял в целом
"""

class Board(pygame.sprite.LayeredUpdates):
    def __init__(self, file, pos, width, center, offset):
        super().__init__()
        self.center = center
        self.tick = 0
        self.ost_x, self.ost_y = 0, 0
        self.x, self.y = pos
        self.offset = offset
        self.width = width
        self.players_list = []
        # отерываем csv файл, в котором описан уровень
        with open(f'''../resources/levels/{file}''', encoding='utf8', mode='r') as csvfile:
            reader = list(list(map(lambda n: int(n) if n != '' else 0, i))
                          for i in list(csv.reader(csvfile, delimiter=';')))
        self.field = list()
        self.walls = list()
        # цикл по созданию поля из данных из файла
        for i in range(len(reader)):
            self.field.append(list())
            for j in range(len(reader[i])):
                # self.field - двумерный список, в котором записаны все ячейки класса cells
                # сделано, чтобы можно было быстрее обращаться и ориентироваться
                self.field[i].append(Cell(self, reader[i][j], j * CELL_SIZE[0] + pos[0], i * CELL_SIZE[1] + pos[1]))
        self.drawWalls()

    # процедура которая, после прорисовки пола, рисует стены
    def drawWalls(self):
        for i in range(len(self.field) - 1):
            for j in range(len(self.field[i])):
                if self.field[i][j].ID == 0 and self.field[i + 1][j].ID != 0:
                    self.walls.append(Wall(self, self.field[i][j].rect.x, self.field[i][j].rect.y))

    def updateToRedPoint(self, point, main=False):
        move_x, move_y = self.center[0] - point[0], self.center[1] - point[1]
        v_x, v_y = move_x / (TIME_STEP * FPS), move_y / (TIME_STEP * FPS)
        if abs(move_x) > max(3, abs(v_x)):
            move_x, self.ost_x = v_x, move_x - v_x
        if abs(move_y) > max(3, abs(v_y)):
            move_y, self.ost_y = v_y, move_y - v_y
        for i in self.sprites():
            i.x += move_x
            i.y += move_y
            if not main and i.__class__ != Chrc:
                if i.x > self.x + self.width:
                    i.drawful = False
                elif i.x < self.x:
                    i.drawful = False
                else:
                    i.drawful = True
            i.rect.x = i.x
            i.rect.y = i.y
            if i.__class__ == Cell and i.type == 6:
                 i.collider = pygame.rect.Rect(i.rect[0], i.rect[1] + CELL_SIZE[1] * 2, i.rect[2],
                                              i.rect[3] / 3 + 10)
            elif i.__class__ == Cell and i.type == 2:
                 i.collider = pygame.rect.Rect(i.rect[0] + 40, i.rect[1] + 17, i.rect[2] - 80,
                                              i.rect[3] - 39)
            elif i.__class__ == Cell and i.type == 3:
                i.collider = pygame.rect.Rect(i.rect[0] + 46, i.rect[1], i.rect[2] - 92,
                                              i.rect[3])
            elif i.__class__ != Chrc:
                i.collider = i.rect.copy()

    def toStartForm(self):
        for i in list(filter(lambda n: n.__class__ == Cell, self.sprites())):
            i.cur_layer = i.obj_layer
            self.change_layer(i, i.cur_layer)
            if i.cur_frame != i.first_frame:
                i.cur_frame = i.first_frame
                i.image = i.frames[i.cur_frame]

    def update(self):
        c = 0
        for i in self.players_list:
            obj = [j for j in self if j.rect.colliderect(i.collider)]
            for j in obj:
                if j.__class__ == Cell and j.type == 2:
                    if j.act_obj == 777:
                        c += 1
                        if c == 2:
                            return True
                    elif j.collider.colliderect(i.collider):
                        j.cur_frame = abs(j.first_frame - 1)
                        j.image = j.frames[j.cur_frame]
                        for m in list(filter(lambda n: n.__class__ == Cell and (n.type == 3 or n.type == 6) and
                                                       (n.img_ID == j.ID + 5 or n.img_ID == j.ID + 8), self.sprites())):
                            m.cur_frame = abs(m.first_frame - 1)
                            m.image = m.frames[m.cur_frame]
                if j.__class__ == Cell and j.type == 6:
                    j.cur_layer = 6
                    self.change_layer(j, j.cur_layer)

    def copyFrom(self, board):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.field[i][j].__class__ == Cell and self.field[i][j].frames_count == 2:
                    self.field[i][j].cur_frame = board.field[i][j].cur_frame
                    self.field[i][j].image = self.field[i][j].frames[self.field[i][j].cur_frame]
                    self.change_layer(self.field[i][j], board.field[i][j].cur_layer)
                    self.field[i][j].cur_layer = board.field[i][j].cur_layer
                    #self.field[i][j].cur_frame = board.field[i][j].cur_frame

    def appendPlayer(self, player):
        self.players_list.append(player)

    def Draw(self, screen):
        for spr in self.sprites():
            try:
                spr.draw(screen)
            except Exception:
                pass


    def createMinimap(self, size):
        for sprite in self.sprites():
            changeSize(sprite, (size[0] / len(self.field[0]), size[1] / len(self.field)))

    def drawMinimap(self, screen):
        for sprite in self.sprites():
            try:
                if sprite.type != 2 and sprite.type != 8:
                    sprite.draw(screen)
            except Exception:
                pass


class Cell(pygame.sprite.Sprite):
    def __init__(self, board, ID, x, y):
        super().__init__(board)
        self.drawful = True
        self.board = board
        self.frames = []
        self.collided = True
        con = sqlite3.connect("../resources/id.db")
        result = list(con.cursor().execute(
            f"""SELECT "Кол. форм", "Тип", "Объект", "Слой", "Изображение", "Первая форма" FROM ObjectID WHERE ID = {ID} """
        ).fetchall()[0])
        if result[2] != 0:
            self.act_obj = result[2]
        self.obj_layer = result[3]
        self.type = result[1]
        self.frames_count = result[0]
        self.ID = ID
        self.img_ID = result[4]
        self.first_frame = result[5]
        self.cur_layer = self.obj_layer
        self.x = x
        self.y = y
        if self.type == 3:
            Cell(board, 1, x, y)
            self.cutFrames(load_image(f'cells/{self.img_ID}.png'), self.frames_count)
            self.y -= DOOR_SIZE[1] - CELL_SIZE[1] + 10
        elif self.type == 6:
            Cell(board, 1, x, y)
            self.cutFrames(load_image(f'cells/{self.img_ID}.png'), self.frames_count)
            self.y -= WALL_SIZE[1] - CELL_SIZE[1] - 110
        else:
            self.cutFrames(load_image(f'cells/{self.img_ID}.jpg'), self.frames_count)
        board.change_layer(self, self.cur_layer)
        self.cur_frame = self.first_frame
        self.image = self.frames[self.cur_frame]
        self.rect.x = self.x
        self.rect.y = self.y
        self.collider = self.rect.copy()

    def cutFrames(self, sheet, count):
        if self.type == 3:
            h = DOOR_SIZE[1]
        elif self.type == 6:
            h = WALL_SIZE[1] - 110
        else:
            h = CELL_SIZE[1]
        self.rect = pygame.Rect(0, 0, CELL_SIZE[0], h)
        sheet = pygame.transform.scale(sheet, (CELL_SIZE[0] * count, h))
        for i in range(count):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def draw(self, screen):
        if self.drawful:
            screen.blit(self.image, self.rect)


class Wall(pygame.sprite.Sprite):
    def __init__(self, board, x, y):
        super().__init__(board)
        self.drawful = True
        self.image = load_image(f'cells/21.png')
        self.image = pygame.transform.scale(self.image, WALL_SIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y - WALL_SIZE[1] + 100 + CELL_SIZE[1]
        self.rect.x = self.x
        self.type = 5
        self.rect.y = self.y
        self.collider = self.rect.copy()
        board.change_layer(self, 2)

    def draw(self, screen):
        if self.drawful:
            screen.blit(self.image, self.rect)
