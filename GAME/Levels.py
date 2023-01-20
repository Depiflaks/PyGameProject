import time

from BattleGround import *
from Statics import *
from LowPriorityStatics import *
from Character import Chrc
from Consts import *
import pygame
from threading import Thread
from Load import *
from pygame import mixer
from Map import *


class Level:
    def __init__(self, directory, screen):
        for i in characters:
            characters.remove(i)
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

        self.chrc_1_center = Chrc(player_data1, *self.spawnPositions[0], self.board_center, 1)
        self.chrc_2_center = Chrc(player_data2, *self.spawnPositions[1], self.board_center, 2)

        self.map = Minimap(f'{directory}/l.csv', MINIMAP_SIZE, (WINDOW_W - MINIMAP_SIZE[0], 0), self.chrc_1_center,
                           self.chrc_2_center, self.board_center.field[0][0])

        self.chrc_1_left = Chrc(player_data1, *self.spawnPositions[0], self.board_left, 1)

        self.chrc_2_right = Chrc(player_data2, *self.spawnPositions[1], self.board_right, 2)
        self.loaded = True

    def updateStates(self, event):
        self.chrc_1_center.updateState(event)
        self.chrc_2_center.updateState(event)
        self.chrc_1_left.updateState(event)
        self.chrc_2_right.updateState(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                menu.add_frame = abs(menu.add_frame - 2)
                musicManager.setDoMusic(not musicManager.doMusic)
            if event.key == pygame.K_m:
                self.map.hide(not self.map.hideable)

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
        red_point_center = ((self.chrc_1_center.x + self.chrc_2_center.x) / 2 + PLAYER_SIZE[0] / 2,
                     (self.chrc_1_center.y + self.chrc_2_center.y) / 2 + PLAYER_SIZE[1] / 2)
        self.board_center.updateToRedPoint(red_point_center, True)
        rebase(self.board_left, self.board_right, self.chrc_1_center, self.chrc_2_center, self.single_screen)
        red_point_left = (self.chrc_1_left.x + PLAYER_SIZE[0] / 2, self.chrc_1_left.y + PLAYER_SIZE[1] / 2)
        red_point_right = (self.chrc_2_right.x + PLAYER_SIZE[0] / 2, self.chrc_2_right.y + PLAYER_SIZE[1] / 2)
        if self.single_screen:
            red_point_left = (red_point_left[0] - (self.board_right.center[0] - self.chrc_2_center.x), red_point_left[1] - (self.board_right.center[1] - self.chrc_2_center.y))
            red_point_right = (red_point_right[0] - (self.board_left.center[0] - self.chrc_1_center.x), red_point_right[1] - (self.board_left.center[1] - self.chrc_1_center.y))
        characters.update()
        self.board_left.updateToRedPoint(red_point_left)
        self.board_right.updateToRedPoint(red_point_right)
        if self.single_screen:
            re_layered(self.board_center, self.chrc_1_center, self.chrc_2_center)
            self.board_center.Draw(self.screen)
        else:
            wall_group = pygame.sprite.Group()
            wall = pygame.sprite.Sprite(wall_group)
            wall.image = load_image(f'cells/23.jpg')
            wall.rect = wall.image.get_rect()
            wall.rect.x = CENTER[0] - CELL_SIZE[0] // 2
            wall.rect.y = 0
            #pygame.draw.rect(wall.image, (100, 100, 100), (0, 0, wall.rect.w, wall.rect.h))

            self.board_right.Draw(self.screen)
            self.board_left.Draw(self.screen)
            wall_group.draw(self.screen)
        self.map.draw(screen)
        if end:
            return True
    def loading(self):
        musicManager.play("load.mp3")
        load = Loading()
        while True:
            if self.loaded and not menu.indicator:
                musicManager.play()
                break
            if self.loaded:
                continue
            self.screen.blit(background, (0, 0))
            load.update()
            self.screen.blit(pygame.transform.scale(load.image, LOADING_SIZE), (load.rect.x, load.rect.y))
            pygame.display.flip()
            clock.tick(FPS)


class LevelManager:
    def __init__(self, *levels, screen=None):
        mixer.music.load("../resources/sounds/intro.mp3")
        mixer.music.play(-1)
        self.index = 0
        self.levels = list(levels)
        self.currentLevel = 0
        self.screen = screen
        self.drawIntro()
        self.startLoad()

    def next(self, flag):
        if not flag:
            return
        self.currentLevel += 1
        if (len(self.levels) > self.currentLevel):
            self.startLoad()
        else:
            end.indicator = True
            end.appendLevelManager(self)

    def drawIntro(self):
        self.screen.blit(intro[self.index], (0, 0))
        pygame.display.flip()
        self.index += 1
        clock.tick(6)
        if self.index < len(intro):
            self.drawIntro()

    def startLoad(self):
        self.level = Level(self.levels[self.currentLevel], self.screen)

