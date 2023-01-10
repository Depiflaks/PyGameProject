from Consts import *
from Statics import *

class Chrc(pygame.sprite.Sprite):
    def __init__(self, data, x, y):
        self.keys = pygame.key.get_pressed()
        self.x = x
        self.y = y
        super().__init__(all_sprites)
        self.animations = [[data[0]], [data[1]], [data[2]]]
        self.cut_sheet(data[3:])
        self.cur_frame = 0
        self.image = data[0]
        self.anim = self.animations[0]
        self.rect = self.rect.move(x, y)

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
        self.keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_a):
                ticks = 0
                cur_frame = 0
                self.anim = self.animations[5]
            elif (event.key == pygame.K_d):
                ticks = 0
                cur_frame = 0
                self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[5]]
            elif (event.key == pygame.K_w):
                ticks = 0
                cur_frame = 0
                self.anim = self.animations[3]
            elif (event.key == pygame.K_s):
                ticks = 0
                cur_frame = 0
                self.anim = self.animations[4]
        if (event.type == pygame.KEYUP and not (self.keys[pygame.K_a] or self.keys[pygame.K_d] or self.keys[pygame.K_w] or self.keys[pygame.K_s])):
            ticks = 0
            cur_frame = 0
            if (event.key == pygame.K_w):
                self.anim = self.animations[1]
            if (event.key == pygame.K_a):
                self.anim = self.animations[0]
            if (event.key == pygame.K_d):
                self.anim = [pygame.transform.flip(el, True, False) for el in self.animations[0]]
            if (event.key == pygame.K_s):
                self.anim = self.animations[2]

    def update(self):
        global ticks
        self.keys = pygame.key.get_pressed()
        if (self.keys[pygame.K_a]):
            self.x -= SPEED / FPS
        if (self.keys[pygame.K_d]):
            self.x += SPEED / FPS
        if (self.keys[pygame.K_w]):
            self.y -= SPEED / FPS
        if (self.keys[pygame.K_s]):
            self.y += SPEED / FPS
        if (ticks % (FPS // 4) == 0):
            self.cur_frame = (self.cur_frame + 1) % len(self.anim)
        self.rect = pygame.rect.Rect(self.x, self.y, self.rect[2], self.rect[3])
        self.image = self.anim[self.cur_frame]
        changeSize(self, PLAYER_SIZE)
        ticks += 1
