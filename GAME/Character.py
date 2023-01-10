from Consts import *
from Statics import *

class Chrc(pygame.sprite.Sprite):
    def __init__(self, data, row, column):
        self.x = row
        self.y = column
        super().__init__(characters)
        self.animations = [[data[0]], [data[1]], [data[2]]]
        self.cut_sheet(data[3:])
        self.cur_frame = 0
        self.image = data[0]
        self.anim = self.animations[0]
        self.rect = self.rect.move(self.x, self.y)

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
        global ticks
        keys = pygame.key.get_pressed()
        leftRight = 0
        upDown = 0
        if keys[pygame.K_a]:
            leftRight += 1
        if keys[pygame.K_d]:
            leftRight += 1
        if keys[pygame.K_w]:
            upDown += 1
        if keys[pygame.K_s]:
            upDown += 1
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_a):
                ticks = 0
                self.cur_frame = 0
                self.anim = self.animations[5]
            elif (event.key == pygame.K_d):
                ticks = 0
                self.cur_frame = 0
                self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[5]]
            elif (event.key == pygame.K_w):
                ticks = 0
                self.cur_frame = 0
                self.anim = self.animations[3]
            elif (event.key == pygame.K_s):
                ticks = 0
                self.cur_frame = 0
                self.anim = self.animations[4]
            if (leftRight == 2 and upDown != 1) or (leftRight != 1 and upDown == 2):
                ticks = 0
                self.cur_frame = 0
                if (event.key == pygame.K_w):
                    self.anim = self.animations[1]
                if (event.key == pygame.K_a):
                    self.anim = self.animations[0]
                if (event.key == pygame.K_d):
                    self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[0]]
                if (event.key == pygame.K_s):
                    self.anim = self.animations[2]
        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s):
                ticks = 0
                self.cur_frame = 0
                if (event.key == pygame.K_w):
                    self.anim = self.animations[1]
                if (event.key == pygame.K_a):
                    self.anim = self.animations[0]
                if (event.key == pygame.K_d):
                    self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[0]]
                if (event.key == pygame.K_s):
                    self.anim = self.animations[2]
            if leftRight == 1:
                ticks = 0
                self.cur_frame = 0
                if (keys[pygame.K_a]):
                    self.anim = self.animations[5]
                if (keys[pygame.K_d]):
                    self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[5]]
            if upDown == 1:
                ticks = 0
                self.cur_frame = 0
                if (keys[pygame.K_w]):
                    self.anim = self.animations[3]
                if (keys[pygame.K_s]):
                    self.anim = self.animations[4]

    def update(self):
        global ticks
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a]):
            self.x -= SPEED / FPS
        if (keys[pygame.K_d]):
            self.x += SPEED / FPS
        if (keys[pygame.K_w]):
            self.y -= SPEED / FPS
        if (keys[pygame.K_s]):
            self.y += SPEED / FPS
        if (ticks % (FPS // 6) == 0):
            self.cur_frame = (self.cur_frame + 1) % len(self.anim)
        self.rect = pygame.rect.Rect(self.x, self.y, self.rect[2], self.rect[3])
        self.image = self.anim[self.cur_frame]
        changeSize(self, PLAYER_SIZE)
        ticks += 1
