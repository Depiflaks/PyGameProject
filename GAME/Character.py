import pygame

from Consts import *
from Statics import *

class Chrc(pygame.sprite.Sprite):
    def __init__(self, data, row, column, board):
        self.ticks = 0
        self.board = board
        super().__init__(characters)
        self.keyUp, self.keyDown, self.keyLeft, self.keyRight = data[3]
        self.animations = [[data[0]], [data[1]], [data[2]]]
        self.cut_sheet(data[4:])
        self.cur_frame = 0
        self.image = data[0]
        self.anim = self.animations[0]
        self.x = board.field[column][row].x
        self.y = board.field[column][row].y - self.image.get_height() / 2 + 10
        self.rect = self.rect.move(self.x, self.y)
        self.collider = pygame.rect.Rect(self.x + 30, self.y + self.image.get_height() - 20, self.image.get_width() / 2, 20)
        board.appendPlayer(self)

    def cut_sheet(self, data):
        for el in data:
            sheet, columns, rows = el[0], el[1], el[2]
            self.frames = []
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))
            self.animations.append(self.frames)

    def updateState(self, event):
        keys = pygame.key.get_pressed()
        leftRight = 0
        upDown = 0
        if keys[self.keyLeft]:
            leftRight += 1
        if keys[self.keyRight]:
            leftRight += 1
        if keys[self.keyUp]:
            upDown += 1
        if keys[self.keyDown]:
            upDown += 1
        if event.type == pygame.KEYDOWN:
            if (event.key == self.keyLeft):
                self.ticks = 0
                self.cur_frame = 0
                self.anim = self.animations[5]
            elif (event.key == self.keyRight):
                self.ticks = 0
                self.cur_frame = 0
                self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[5]]
            elif (event.key == self.keyUp):
                self.ticks = 0
                self.cur_frame = 0
                self.anim = self.animations[3]
            elif (event.key == self.keyDown):
                self.ticks = 0
                self.cur_frame = 0
                self.anim = self.animations[4]
            if (leftRight == 2 and upDown != 1) or (leftRight != 1 and upDown == 2):
                self.ticks = 0
                self.cur_frame = 0
                if (event.key == self.keyUp):
                    self.anim = self.animations[1]
                if (event.key == self.keyLeft):
                    self.anim = self.animations[0]
                if (event.key == self.keyRight):
                    self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[0]]
                if (event.key == self.keyDown):
                    self.anim = self.animations[2]
        if (event.type == pygame.KEYUP):
            if (event.key == self.keyLeft or event.key == self.keyRight or event.key == self.keyUp or event.key == self.keyDown):
                self.ticks = 0
                self.cur_frame = 0
                if (event.key == self.keyUp):
                    self.anim = self.animations[1]
                if (event.key == self.keyLeft):
                    self.anim = self.animations[0]
                if (event.key == self.keyRight):
                    self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[0]]
                if (event.key == self.keyDown):
                    self.anim = self.animations[2]
            if leftRight == 1:
                self.ticks = 0
                self.cur_frame = 0
                if (keys[self.keyLeft]):
                    self.anim = self.animations[5]
                if (keys[self.keyRight]):
                    self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[5]]
            if upDown == 1:
                self.ticks = 0
                self.cur_frame = 0
                if (keys[self.keyUp]):
                    self.anim = self.animations[3]
                if (keys[self.keyDown]):
                    self.anim = self.animations[4]

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[self.keyLeft]):
            self.x -= SPEED / FPS
        if (keys[self.keyRight]):
            self.x += SPEED / FPS
        if (keys[self.keyUp]):
            self.y -= SPEED / FPS
        if (keys[self.keyDown]):
            self.y += SPEED / FPS
        if (self.ticks % (FPS // 6) == 0):
            self.cur_frame = (self.cur_frame + 1) % len(self.anim)
        self.rect = pygame.rect.Rect(self.x, self.y, self.rect[2], self.rect[3])
        self.image = self.anim[self.cur_frame]
        changeSize(self, PLAYER_SIZE)
        self.ticks += 1


class Collider(pygame.sprite.Sprite):
    def __init__(self):
        pass
