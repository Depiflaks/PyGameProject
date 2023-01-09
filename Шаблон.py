import pygame

if __name__ == '__main__':
    pygame.init()
    size = 400, 400
    screen = pygame.display.set_mode(size)

    group = pygame.sprite.Group()
    layered_group = pygame.sprite.LayeredUpdates()

    A = None
    if A:
        print(1)

    a = pygame.sprite.Sprite(layered_group)
    #layered_group.add(a)
    a.image = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
    a.rect = pygame.Rect(100, 100, 100, 100)
    pygame.draw.rect(a.image, (255, 0, 0), (0, 0, 100, 100))

    b = pygame.sprite.Sprite(layered_group)
    #layered_group.add(b)
    b.image = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
    b.rect = pygame.Rect(150, 150, 100, 100)
    pygame.draw.rect(b.image, (0, 0, 255), (0, 0, 100, 100))

    layered_group.change_layer(a, 2)
    layered_group.change_layer(b, 1)

    layered_group.draw(screen)

    #group.draw(screen)
    running = True
    pygame.display.flip()
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
