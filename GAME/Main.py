#import sys
#import ctypes
#import pygame
#import os.path, inspect
#import io
#from Levels import *
#from Menu import *
from LowestPriorityStatics import *

pygame.init()

pygame.display.set_caption('ToGetHer')
icon_surf = load_image(f'i.ico')
pygame.display.set_icon(load_image(icon_surf))
running = True
screen.fill((10, 255, 10))

ind = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or ind:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
            if event.key == pygame.K_c:
                pygame.display.iconify()
        if menu.indicator:
            ind = menu.update_forms(event)
        elif end.indicator:
            end.update_forms(event)
        else:
            levelManager.level.updateStates(event)
    if menu.indicator:
        menu.draw(screen)
    elif end.indicator:
        end.draw(screen)
    else:
        levelManager.next(levelManager.level.update())
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()
