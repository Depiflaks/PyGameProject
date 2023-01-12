from BattleGround import *
from Statics import *
from Character import Chrc
from Consts import *
import pygame
from threading import Thread
from Load import *


class Level:
    def __init__(self, directory, screen):
        self.screen = screen
        self.loaded = False
        th1 = Thread(target=self.loading)
        th1.start()
        self.single_screen = True
        self.board_center = Board(f'{directory}/l.csv', (0 - CELL_SIZE[0], 0), 1920 + CELL_SIZE[0], CENTER, 1500)
        self.board_left = Board(f'{directory}/l.csv', (0 - CELL_SIZE[0], 0), (WINDOW_W + CELL_SIZE[0]) // 2,
                                CENTER_LEFT, 1500)
        self.board_right = Board(f'{directory}/l.csv', ((WINDOW_W - CELL_SIZE[0]) // 2, 0),
                                 (WINDOW_W + CELL_SIZE[0]) // 2 + CELL_SIZE[0], CENTER_RIGHT, 1500)

        self.spawnPositions = [list(map(int, el.split())) for el in
                               open(f"../resources/levels/{directory}/chr.csv").read().strip().split("\n")]

        self.chrc_1_center = Chrc(player_data1, *self.spawnPositions[0], self.board_center)
        self.chrc_2_center = Chrc(player_data2, *self.spawnPositions[1], self.board_center)

        self.chrc_1_left = Chrc(player_data1, *self.spawnPositions[0], self.board_left)

        self.chrc_2_right = Chrc(player_data2, *self.spawnPositions[1], self.board_right)

        self.board_center.add(self.chrc_1_center, layer=CHARACTERS_LAYER)
        self.board_center.add(self.chrc_2_center, layer=CHARACTERS_LAYER)

        self.board_left.add(self.chrc_1_left, layer=CHARACTERS_LAYER)

        self.board_right.add(self.chrc_2_right, layer=CHARACTERS_LAYER)
        self.loaded = True

    def updateStates(self, event):
        self.chrc_1_center.updateState(event)
        self.chrc_2_center.updateState(event)
        self.chrc_1_left.updateState(event)
        self.chrc_2_right.updateState(event)

    def update(self):
        r = (self.chrc_1_center.x - self.chrc_2_center.x) ** 2 + (self.chrc_1_center.y - self.chrc_2_center.y) ** 2
        if r > MIN:
            self.single_screen = False
        else:
            self.single_screen = True
        self.screen.fill(BACKGROUND_COLOR)
        self.board_center.toStartForm()
        self.board_left.toStartForm()
        self.board_right.toStartForm()
        end = self.board_center.update()
        self.board_left.copyFrom(self.board_center)
        self.board_right.copyFrom(self.board_center)
        characters.update()
        red_point = ((self.chrc_1_center.x + self.chrc_2_center.x) / 2 + PLAYER_SIZE[0] / 2,
                     (self.chrc_1_center.y + self.chrc_2_center.y) / 2 + PLAYER_SIZE[1] / 2)
        self.board_center.updateToRedPoint(red_point, True)
        rebase(self.board_left, self.board_right, self.chrc_1_center, self.chrc_2_center, self.single_screen)
        red_point = (self.chrc_1_left.x + PLAYER_SIZE[0] // 2, self.chrc_1_left.y + PLAYER_SIZE[1] // 2)
        self.board_left.updateToRedPoint(red_point)
        red_point = (self.chrc_2_right.x + PLAYER_SIZE[0] // 2, self.chrc_2_right.y + PLAYER_SIZE[1] // 2)
        self.board_right.updateToRedPoint(red_point)
        if self.single_screen:
            re_layered(self.board_center, self.chrc_1_center, self.chrc_2_center)
            self.board_center.draw(self.screen)
        else:
            wall_group = pygame.sprite.Group()
            wall = pygame.sprite.Sprite(wall_group)
            wall.image = pygame.transform.scale(load_image(f'cells/22.jpg'), (150, 1080))
            wall.rect = wall.image.get_rect()
            wall.rect.x = CENTER[0] - CELL_SIZE[0] // 2
            wall.rect.y = 0
            #pygame.draw.rect(wall.image, (100, 100, 100), (0, 0, wall.rect.w, wall.rect.h))

            self.board_right.draw(self.screen)
            self.board_left.draw(self.screen)
            wall_group.draw(self.screen)
        if end:
            return True
        pygame.display.flip()
        clock.tick(FPS)

    def loading(self):
        pygame.init()
        load = Loading()
        while True:
            self.screen.blit(background, (0, 0))
            load.update()
            self.screen.blit(pygame.transform.scale(load.image, LOADING_SIZE), (load.rect.x, load.rect.y))
            pygame.display.flip()
            clock.tick(FPS)
            if self.loaded:
                break


class LevelManager:
    def __init__(self, *levels, screen=None):
        self.levels = list(levels)
        self.currentLevel = 0
        self.screen = screen
        self.level = Level(self.levels[self.currentLevel], self.screen)
    def next(self, flag):
        if not flag:
            return
        self.currentLevel += 1
        if (len(self.levels) > self.currentLevel):
            self.level = Level(self.levels[self.currentLevel], self.screen)
        else:
            print("Вы победили!")

