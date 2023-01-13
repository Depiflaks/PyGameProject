from Levels import *

pygame.init()
size = WINDOW_W, WINDOW_H
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ToGetHer')
running = True

screen.fill((10, 255, 10))

levelManager = LevelManager("l3", "l1", "l3", screen=screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
            if event.key == pygame.K_c:
                pygame.display.iconify()
        levelManager.level.updateStates(event)
    levelManager.next(levelManager.level.update())
pygame.quit()
