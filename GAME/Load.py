from Statics import *
from Consts import *
class Loading(pygame.sprite.Sprite):
    def __init__(self):
        self.index = 0
        self.anim = loading
        self.image = loading[self.index % len(loading)]
        self.rect = self.image.get_rect()
        self.rect.x = CENTER[0] - self.image.get_width()
        self.rect.y = CENTER[1] - self.image.get_height()

    def update(self):
        self.index += 1
        self.image = loading[self.index % len(loading)]