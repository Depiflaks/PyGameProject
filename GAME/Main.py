import pygame

from Levels import *
from Menu import *

pygame.init()
size = WINDOW_W, WINDOW_H
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ToGetHer')
running = True

screen.fill((10, 255, 10))

menu = Menu(screen, True)

levelManager = LevelManager("l4", "l2", "l3", screen=screen)
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
        else:
            levelManager.level.updateStates(event)
    if menu.indicator:
        menu.draw(screen)
    else:
        levelManager.next(levelManager.level.update())
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
