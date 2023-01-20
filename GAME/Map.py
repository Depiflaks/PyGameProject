import csv

import pygame.draw


class Minimap:
    def __init__(self, file, size, pos):
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

    def hide(self, hide):
        self.hideable = hide