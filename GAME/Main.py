from Consts import *
from Character import *
from BattleGround import *
from Statics import *
import pygame
import os
import sys
import csv


def re_layered(board, c1, c2):
    if c1.y > c2.y:
        board.change_layer(c2, 4)
        board.change_layer(c1, 5)
    else:
        board.change_layer(c1, 4)
        board.change_layer(c2, 5)


pygame.init()
size = WINDOW_W, WINDOW_H
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ToGetHer')

single_screen = True
running = True

screen.fill(BACKGROUND_COLOR)

board_center = Board('l2/l2.csv', (0 - CELL_SIZE[0], 0), 1920 + CELL_SIZE[0], CENTER)
board_left = Board('l2/l2.csv', (0 - CELL_SIZE[0], 0), (WINDOW_W + CELL_SIZE[0]) // 2, CENTER_LEFT)
board_right = Board('l2/l2.csv', ((WINDOW_W - CELL_SIZE[0]) // 2, 0),
                    (WINDOW_W + CELL_SIZE[0]) // 2 + CELL_SIZE[0], CENTER_RIGHT)

spawnPositions = [list(map(int, el.split())) for el in
                  open("../resources/levels/l2/chr.csv").read().strip().split("\n")]

chrc_1_center = Chrc(player_data1, *spawnPositions[0], board_center)
chrc_2_center = Chrc(player_data2, *spawnPositions[1], board_center)

chrc_1_left = Chrc(player_data1, *spawnPositions[0], board_left)
chrc_2_left = Chrc(player_data2, *spawnPositions[1], board_left)

chrc_1_right = Chrc(player_data1, *spawnPositions[0], board_right)
chrc_2_right = Chrc(player_data2, *spawnPositions[1], board_right)

board_center.add(chrc_1_center, layer=CHARACTERS_LAYER)
board_center.add(chrc_2_center, layer=CHARACTERS_LAYER)

board_left.add(chrc_1_left, layer=CHARACTERS_LAYER)
board_left.add(chrc_2_left, layer=CHARACTERS_LAYER)

board_right.add(chrc_1_right, layer=CHARACTERS_LAYER)
board_right.add(chrc_2_right, layer=CHARACTERS_LAYER)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            pygame.display.iconify()
        for chrc in characters:
            chrc_1_center.updateState(event)
            chrc_2_center.updateState(event)
            chrc_1_left.updateState(event)
            chrc_2_left.updateState(event)
            chrc_1_right.updateState(event)
            chrc_2_right.updateState(event)
    r = (chrc_1_center.x - chrc_2_center.x) ** 2 + (chrc_1_center.y - chrc_2_center.y) ** 2
    if r > MIN:
        single_screen = False
    else:
        single_screen = True
    screen.fill(BACKGROUND_COLOR)
    if single_screen:
        re_layered(board_center, chrc_1_center, chrc_2_center)
        characters.update()
        board_center.toStartForm()
        board_center.update()
        red_point = ((chrc_1_center.x + chrc_2_center.x) / 2 + PLAYER_SIZE[0] / 2,
                     (chrc_1_center.y + chrc_2_center.y) / 2 + PLAYER_SIZE[1] / 2)
        board_center.updateToRedPoint(red_point)

        board_center.draw(screen)
    else:
        wall_group = pygame.sprite.Group()
        
        wall = pygame.sprite.Sprite(wall_group)
        wall.image = pygame.Surface((CELL_SIZE[0], 1080))
        wall.rect = pygame.Rect(CENTER[0] - CELL_SIZE[0] // 2, 0, CELL_SIZE[0], 1080)
        pygame.draw.rect(wall.image, (100, 100, 100), (0, 0, wall.rect.w, wall.rect.h))

        re_layered(board_left, chrc_1_left, chrc_2_left)
        re_layered(board_right, chrc_1_right, chrc_2_right)
        characters.update()

        red_point = (chrc_1_left.x + PLAYER_SIZE[0] // 2, chrc_1_left.y + PLAYER_SIZE[1] // 2)
        board_left.toStartForm()
        board_left.update()
        board_left.updateToRedPoint(red_point)
        board_left.draw(screen)

        red_point = (chrc_2_right.x + PLAYER_SIZE[0] // 2, chrc_2_right.y + PLAYER_SIZE[1] // 2)
        board_right.toStartForm()
        board_right.update()
        board_right.updateToRedPoint(red_point)
        board_right.draw(screen)

        wall_group.draw(screen)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
