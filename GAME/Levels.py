from BattleGround import *
from Statics import *
from Character import Chrc
from Consts import *
import pygame


class Level:
    def __init__(self, directory, screen):
        self.screen = screen
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
        self.board_center.update()
        self.board_left.copyFrom(self.board_center)
        self.board_right.copyFrom(self.board_center)
        characters.update()
        red_point = ((self.chrc_1_center.x + self.chrc_2_center.x) / 2 + PLAYER_SIZE[0] / 2,
                     (self.chrc_1_center.y + self.chrc_2_center.y) / 2 + PLAYER_SIZE[1] / 2)
        self.board_center.updateToRedPoint(red_point, True)
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
            wall.image = pygame.Surface((CELL_SIZE[0], 1080))
            wall.rect = pygame.Rect(CENTER[0] - CELL_SIZE[0] // 2, 0, CELL_SIZE[0], 1080)
            pygame.draw.rect(wall.image, (100, 100, 100), (0, 0, wall.rect.w, wall.rect.h))

            self.board_right.draw(self.screen)
            self.board_left.draw(self.screen)
            wall_group.draw(self.screen)
        pygame.display.flip()
        clock.tick(FPS)
