import pygame

pygame.init()
size = 400, 400
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)

gr1 = pygame.sprite.LayeredUpdates()
gr2 = pygame.sprite.LayeredUpdates()
gr3 = pygame.sprite.LayeredUpdates()

a = pygame.sprite.Sprite(gr1)
a.image = pygame.Surface((100, 100))
a.rect = pygame.Rect(100, 100, 100, 100)
pygame.draw.rect(a.image, (255, 0, 0), (0, 0, 100, 100))


b = pygame.sprite.Sprite(gr2)
b.image = pygame.Surface((100, 100))
b.rect = pygame.Rect(150, 150, 100, 100)
pygame.draw.rect(b.image, (50, 50, 50), (0, 0, 100, 100))

gr3.add(gr1, gr2)

gr3.change_layer(a, 10)
gr3.change_layer(b, 1)

gr1.draw(screen)
gr2.draw(screen)
gr3.draw(screen)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False