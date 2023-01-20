import csv

import pygame.draw
from Consts import *


class Minimap:
    def __init__(self, file, size, pos, chrc1, chrc2, startCell, ends):
        self.ends = ends
        self.startCell = startCell
        self.chrc1, self.chrc2 = chrc1, chrc2
        self.hideable = False
        with open(f'''../resources/levels/{file}''', encoding='utf8', mode='r') as csvfile:
            reader = list(list(map(lambda n: int(n) if n != '' else 0, i))
                          for i in list(csv.reader(csvfile, delimiter=';')))
        self.field = list()
        for i in range(len(reader)):
            self.field.append(list())
            for j in range(len(reader[i])):
                self.field[i].append(0 if reader[i][j] in [0] else 1)
        self.size = size
        self.pos = pos

    def draw(self, screen):
        if self.hideable:
            return
        width = self.size[0] / len(self.field[0])
        height = self.size[1] / len(self.field)
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if self.field[i][j]:
                    pygame.draw.rect(screen, pygame.Color("White"), (self.pos[0] + j * width , self.pos[1] + i * height, width, height))
                else:
                    pygame.draw.rect(screen, pygame.Color("Gray"), (self.pos[0] + j * width , self.pos[1] + i * height, width, height))
        for end in self.ends:
            pygame.draw.rect(screen, pygame.Color("Pink"), (self.pos[0] + end[1] * width , self.pos[1] + end[0] * height, width, height))
        if self.chrc1.collider.y < self.chrc2.collider.y:
            pygame.draw.rect(screen, pygame.Color("Blue"),
                             (self.pos[0] + abs(self.startCell.x - self.chrc1.collider.x + 40) / CELL_SIZE[0] * width, self.pos[1] + abs(self.startCell.y - self.chrc1.collider.y + 30) / CELL_SIZE[1] * height, width, height))
            pygame.draw.rect(screen, (162, 141, 37),
                             (self.pos[0] + abs(self.startCell.x - self.chrc2.collider.x + 40) / CELL_SIZE[0] * width,
                              self.pos[1] + abs(self.startCell.y - self.chrc2.collider.y + 30) / CELL_SIZE[1] * height,
                              width, height))
        else:
            pygame.draw.rect(screen, (162, 141, 37),
                             (self.pos[0] + abs(self.startCell.x - self.chrc2.collider.x + 40) / CELL_SIZE[0] * width,
                              self.pos[1] + abs(self.startCell.y - self.chrc2.collider.y + 30) / CELL_SIZE[1] * height,
                              width, height))
            pygame.draw.rect(screen, pygame.Color("Blue"),
                             (self.pos[0] + abs(self.startCell.x - self.chrc1.collider.x + 40) / CELL_SIZE[0] * width,
                              self.pos[1] + abs(self.startCell.y - self.chrc1.collider.y + 30) / CELL_SIZE[1] * height,
                              width, height))

    def hide(self, hide):
        self.hideable = hide