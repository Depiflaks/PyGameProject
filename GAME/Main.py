from Consts import *
from Character import *
from BattleGround import *
from Statics import *
import pygame
import os
import sys
import csv


pygame.init()
size = WINDOW_W, WINDOW_H
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ToGetHer')

running = True

screen.fill(BACKGROUND_COLOR)

board = Board('l2/l2.csv')
spawnPositions = [list(map(int, el.split())) for el in open("../resources/levels/l2/chr.csv").read().strip().split("\n")]
chrc1 = Chrc(player_data1, *spawnPositions[0], board)
chrc2 = Chrc(player_data2, *spawnPositions[1], board)
board.add(chrc1, layer=CHARACTERS_LAYER)
board.add(chrc2, layer=CHARACTERS_LAYER)
#board.updateToRedPoint((chrc1.x, chrc1.y))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False
        for chrc in characters:
            chrc1.updateState(event)
            chrc2.updateState(event)
    characters.update()
    board.toStartForm()
    board.update()
    board.updateToRedPoint(((chrc1.x + chrc2.x) / 2 + PLAYER_SIZE[0] / 2, (chrc1.y + chrc2.y) / 2 + PLAYER_SIZE[1] / 2))
    screen.fill(BACKGROUND_COLOR)
    board.draw(screen)
    # all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
