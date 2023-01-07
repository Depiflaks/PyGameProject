import pygame
import os
import sys

def load_image(name, colorkey=None):
    fullname = os.path.join('..', 'resources', 'img', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    player_data = [load_image("characters/idle.png"), [load_image("characters/up.png"), 1, 2],
                   [load_image("characters/leftRight.png"), 2, 1]]
