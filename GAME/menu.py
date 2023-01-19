import pygame
from Load import *

class Menu(pygame.sprite.Group):
    def __init__(self, screen, indicator):
        super().__init__()
        self.screen = screen
        self.indicator = indicator
        self.draw_obj()

    def draw_obj(self, way=0):
        self.bcgr = pygame.sprite.Sprite(self)
        self.bcgr.image = load_image(f'background.jpg')
        self.bcgr.rect = self.bcgr.image.get_rect()
        self.bcgr.x, self.bcgr.y = 0, 0
        x = CENTER[0] - BUTTON_SIZE[0] // 2
        self.start_button = Button(self, self.screen, load_image(f'menu/start.jpg'), 3, x, 300)
        self.settings_button = Button(self, self.screen, load_image(f'menu/set.jpg'), 2, x, 500)
        self.exit_button = Button(self, self.screen, load_image(f'menu/exit.jpg'), 2, x, 700)

    def update_forms(self, event):
        if event.type == pygame.MOUSEMOTION:
            for i in filter(lambda n: n.__class__ == Button, self.sprites()):
                if i.rect.collidepoint(event.pos[0], event.pos[1]):
                    i.image = i.frames[1]
                else:
                    i.image = i.frames[0]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.rect.collidepoint(event.pos[0], event.pos[1]):
                self.indicator = False
            if self.exit_button.rect.collidepoint(event.pos[0], event.pos[1]):
                return True
            return False


class Button(pygame.sprite.Sprite):
    def __init__(self, group, screen, img, count, x, y):
        super().__init__(group)
        self.frames = list()
        self.screen = screen
        self.cutFrames(img, count)
        self.image = self.frames[0]
        self.rect.x = x
        self.rect.y = y

    def cutFrames(self, sheet, count):
        self.rect = pygame.Rect(0, 0, BUTTON_SIZE[0], BUTTON_SIZE[1])
        sheet = pygame.transform.scale(sheet, (BUTTON_SIZE[0] * count, BUTTON_SIZE[1]))
        for i in range(count):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))