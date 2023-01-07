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
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption('ToGetHer')

running = True
clock = pygame.time.Clock()

screen.fill(BACKGROUND_COLOR)

board = Board('l1.csv')
board.draw(screen)
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False
pygame.quit()
