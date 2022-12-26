from Consts import *
from Statics import *
import pygame

class Chrc(pygame.sprite.Sprite):
    def __init__(self, data, x, y):
        self.x = x
        self.y = y
        super().__init__(all_sprites)
        self.animations = []
        self.cut_sheet(data[1:])
        self.cur_frame = 0
        self.image = data[0]
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

    def update(self, event):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_d]):
            cur_frame = 0
            anim = self.animations[1]
        if (keys[pygame.K_w] or keys[pygame.K_s]):
            cur_frame = 0
            anim = self.animations[0]
        self.cur_frame = (self.cur_frame + 1) % len(anim)
        self.image = anim[self.cur_frame]