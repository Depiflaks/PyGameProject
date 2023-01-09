import os
import sys
import csv
from Statics import *
from Character import Chrc
from Consts import *
import pygame

"""
Класс для описания игрового поял в целом
"""
class Board(pygame.sprite.Group):
    def __init__(self, file):
        super().__init__()
        # отерываем csv файл, в котором описан уровень
        with open(f'''../resources/levels/{file}''', encoding='utf8', mode='r') as csvfile:
            reader = list(list(map(int, i)) for i in list(csv.reader(csvfile, delimiter=';')))
        self.field = list()
        self.layerGroup = pygame.sprite.LayeredUpdates()

        # цикл по созданию поля из данных из файла
        for i in range(len(reader)):
            self.field.append(list())
            for j in range(len(reader[i])):
                # self.field - двумерный список, в котором записаны все ячейки класса cells
                # сделано, чтобы можно было быстрее обращаться и ориентироваться
                self.field[i].append(Cell(self, reader[i][j], j * CELL_SIZE[0], i * CELL_SIZE[1]))
                self.layerGroup.add(self.fie )
        self.drawWalls()

    # процедура которая, после прорисовки пола, рисует стены
    def drawWalls(self):
        for i in range(len(self.field) - 1):
            for j in range(len(self.field[i])):
                if self.field[i][j].ID == 0 and self.field[i + 1][j].ID != 0:
                    Wall(self, self.field[i][j].rect.x, self.field[i][j].rect.y)

    def updateToRedPoint(self, point):
        move_x, move_y = CENTER[0] - point[0], CENTER[1] - point[1]
        for i in self.sprites():
            i.rect.x += move_x
            i.rect.y += move_y


class Cell(pygame.sprite.Sprite):
    def __init__(self, board, ID, x, y):
        super().__init__(board)
        self.ID = ID
        if self.ID == 0:
            self.image = pygame.Surface((CELL_SIZE[0], CELL_SIZE[1]), pygame.SRCALPHA, 32)
            self.rect = pygame.Rect(x, y, CELL_SIZE[0], CELL_SIZE[1])
            pygame.draw.rect(self.image, BACKGROUND_COLOR, (0, 0, CELL_SIZE[0], CELL_SIZE[1]))
        elif self.ID == 10 or self.ID == 11:
            self.image = load_image(f'cells/{self.ID}.png')
            self.image = pygame.transform.scale(self.image, DOOR_SIZE)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - DOOR_SIZE[1] + CELL_SIZE[1]
        else:
            self.image = load_image(f'cells/{self.ID}.jpg')
            self.image = pygame.transform.scale(self.image, CELL_SIZE)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


class Wall(pygame.sprite.Sprite):
    def __init__(self, board, x, y):
        super().__init__(board)
        self.image = load_image(f'cells/14.png')
        self.image = pygame.transform.scale(self.image, WALL_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - WALL_SIZE[1] + 90 + CELL_SIZE[1]


if __name__ == '__main__':
    pygame.init()
    size = WINDOW_W, WINDOW_H
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption('ToGetHer')

    running = True
    clock = pygame.time.Clock()

    screen.fill(BACKGROUND_COLOR)

    board = Board('l2.csv')
    #board.updateToRedPoint((300, 300))
    board.draw(screen)

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
    pygame.quit()