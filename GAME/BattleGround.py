import os
import sys
import sqlite3
import csv
from Statics import *
from Character import Chrc
from Consts import *
import pygame

"""
Класс для описания игрового поял в целом
"""
class Board(pygame.sprite.LayeredUpdates):
    def __init__(self, file, pos, width, center, offset):
        super().__init__()
        self.center = center
        self.x, self.y = pos
        self.offset = offset
        self.width = width
        self.players_list = []
        # отерываем csv файл, в котором описан уровень
        with open(f'''../resources/levels/{file}''', encoding='utf8', mode='r') as csvfile:
            reader = list(list(map(int, i)) for i in list(csv.reader(csvfile, delimiter=';')))
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

    def updateToRedPoint(self, point):
        move_x, move_y = self.center[0] - point[0], self.center[1] - point[1]
        for i in self.sprites():
            i.x += move_x
            i.y += move_y
            if i.x > self.x + self.width:
                i.collided = False
                i.rect.x = i.x + self.offset
            elif i.x < self.x:
                i.collided = False
                i.rect.x = i.x - self.offset
            else:
                i.collided = True
                i.rect.x = i.x
            i.rect.y = i.y

    def toStartForm(self):
        for i in list(filter(lambda n: n.__class__ == Cell, self.sprites())):
            if i.cur_frame == 1:
                i.image = i.frames[0]
                i.cur_frame = 0

    def update(self):
        for i in self.players_list:
            obj = [j for j in self if j.rect.colliderect(i.collider)]
            for j in obj:
                if j.__class__ == Cell and j.type == 2:
                    j.cur_frame = 1
                    j.image = j.frames[j.cur_frame]
                    for m in list(filter(lambda n: n.__class__ == Cell and n.type == 3 and n.ID == j.act_obj, self.sprites())):
                        m.cur_frame = 1
                        m.image = m.frames[m.cur_frame]

    def copyFrom(self, board):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.field[i][j].__class__ == Cell and self.field[i][j].frames_count == 2:
                    self.field[i][j].cur_frame = board.field[i][j].cur_frame
                    self.field[i][j].image = self.field[i][j].frames[self.field[i][j].cur_frame]
                    self.field[i][j].cur_frame = board.field[i][j].cur_frame



    def appendPlayer(self, player):
        self.players_list.append(player)


class Cell(pygame.sprite.Sprite):
    def __init__(self, board, ID, x, y):
        super().__init__(board)
        self.board = board
        self.frames = []
        self.collided = True
        con = sqlite3.connect("../resources/id.db")
        result = list(con.cursor().execute(f"""SELECT "Активная форма", "Тип", "Объект", "Слой" FROM ObjectID
            WHERE ID = {ID} """).fetchall()[0])
        if result[2] != 0:
            self.act_obj = result[2]
        self.obj_layer = result[3]
        self.type = result[1]
        self.frames_count = result[0]
        self.ID = ID
        self.x = x
        self.y = y
        if self.type == 3:
            Cell(board, 1, x, y)
            self.cutFrames(load_image(f'cells/{self.ID}.png'), self.frames_count)
            self.y -= DOOR_SIZE[1] - CELL_SIZE[1] + 10
        else:
            self.cutFrames(load_image(f'cells/{self.ID}.jpg'), self.frames_count)
        board.change_layer(self, self.obj_layer)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.x = self.x
        self.rect.y = self.y

    def cutFrames(self, sheet, count):
        w = DOOR_SIZE[1] if self.type == 3 else CELL_SIZE[1]
        self.rect = pygame.Rect(0, 0, CELL_SIZE[0], w)
        sheet = pygame.transform.scale(sheet, (CELL_SIZE[0] * count, w))
        for i in range(count):
            frame_location = (self.rect.w * i, 0)
            #print(frame_location, sheet.get_width(), sheet.get_height(), self.rect.size)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))


class Wall(pygame.sprite.Sprite):
    def __init__(self, board, x, y):
        super().__init__(board)
        self.image = load_image(f'cells/21.png')
        self.image = pygame.transform.scale(self.image, WALL_SIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y - WALL_SIZE[1] + 90 + CELL_SIZE[1]
        self.rect.x = self.x
        self.type = 5
        self.rect.y = self.y
        board.change_layer(self, 2)