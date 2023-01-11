import random

import pygame
import os
import sys

STEP = 200
FPS = 60


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(balls_group)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (255, 0, 0), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)
        self.lastBalls = set()

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy *= -1
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx *= -1
        per_ball = set(pygame.sprite.spritecollide(self, balls_group, False))
        per_ball.remove(self)
        if per_ball != [] and per_ball - self.lastBalls != set():
            a = list(per_ball)[0]
            self.vx, self.vy, a.vx, a.vy = a.vx, a.vy, self.vx, self.vy
        self.lastBalls = set(per_ball)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface((1, y2 - y1))
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface((x2 - x1, 1))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Столкновение шариков')
    running = True

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    balls_group = pygame.sprite.Group()

    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    for i in range(20):
        One = Ball(20, 200, 200)
    F = 1

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        F += 1
pygame.quit()
