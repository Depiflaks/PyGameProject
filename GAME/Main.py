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
clock = pygame.time.Clock()

screen.fill(BACKGROUND_COLOR)

board = Board('l1.csv')
chrc1 = Chrc(player_data, 100, 100)
board.draw(screen)
all_sprites.draw(screen)
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False
        board.draw(screen)
        all_sprites.update(event)
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()

pygame.quit()
