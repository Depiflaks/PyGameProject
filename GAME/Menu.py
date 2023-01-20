from Load import *


# Класс меню
class Menu(pygame.sprite.Group):
    def __init__(self, screen, indicator):
        super().__init__()
        self.screen = screen
        self.indicator = indicator
        self.draw_obj()

    def draw_obj(self, way=0):
        self.bcgr = pygame.sprite.Sprite(self)
        self.bcgr.image = load_image(f'background.jpg')
        self.bcgr.rect = self.bcgr.image.get_rect()
        self.bcgr.x, self.bcgr.y = 0, 0
        self.add_frame = 0
        self.m_x, self.m_y = 0, 0
        x = CENTER[0] - BUTTON_SIZE[0] // 2
        self.start_button = Button(self, self.screen, load_image(f'menu/start.jpg'), 3, x, 450, 400, 100)
        self.exit_button = Button(self, self.screen, load_image(f'menu/exit.jpg'), 2, x + 50, 600, 300, 80)
        self.val_button = Button(self, self.screen, load_image(f'menu/val.jpg'), 4, 1700, 900, 100, 100)

    def update_forms(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.m_x, self.m_y = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.rect.collidepoint(event.pos[0], event.pos[1]):
                self.indicator = False
            if self.exit_button.rect.collidepoint(event.pos[0], event.pos[1]):
                return True
            # вставлять сюда (громкость)
            if self.val_button.rect.collidepoint(event.pos[0], event.pos[1]):
                self.add_frame = abs(self.add_frame - 2)
                musicManager.setDoMusic(not musicManager.doMusic)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.add_frame = abs(self.add_frame - 2)
                musicManager.setDoMusic(not musicManager.doMusic)

        for i in filter(lambda n: n.__class__ == Button, self.sprites()):
            if i.rect.collidepoint(self.m_x, self.m_y):
                i.image = i.frames[1 + (self.add_frame if i == self.val_button else 0)]
            else:
                i.image = i.frames[0 + (self.add_frame if i == self.val_button else 0)]

        return False


class End(pygame.sprite.Group):
    def __init__(self, screen, menu, indicator):
        super().__init__()
        self.add_frame = 0
        self.screen = screen
        self.menu = menu
        self.indicator = indicator
        self.draw_obj()

    def appendLevelManager(self, levelManager):
        self.levelManager = levelManager

    def draw_obj(self):
        self.bcgr = pygame.sprite.Sprite(self)
        self.bcgr.image = load_image(f'ending.jpg')
        self.bcgr.rect = self.bcgr.image.get_rect()
        self.bcgr.x, self.bcgr.y = 0, 0
        self.m_x, self.m_y = 0, 0
        x = CENTER[0] - BUTTON_SIZE[0] // 2
        self.continue_button = Button(self, self.screen, load_image(f'menu/cont.jpg'), 2, x, 700, 400, 100)

    def update_forms(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.m_x, self.m_y = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button.rect.collidepoint(event.pos[0], event.pos[1]):
                # здесь снова должна вызваться менюшка
                self.menu.indicator = True
                self.indicator = False
                self.levelManager.currentLevel = 0
                self.levelManager.startLoad()
        for i in filter(lambda n: n.__class__ == Button, self.sprites()):
            if i.rect.collidepoint(self.m_x, self.m_y):
                i.image = i.frames[1 + (self.add_frame if i == self.continue_button else 0)]
            else:
                i.image = i.frames[0 + (self.add_frame if i == self.continue_button else 0)]
        return False


class Button(pygame.sprite.Sprite):
    def __init__(self, group, screen, img, count, x, y, w, h):
        super().__init__(group)
        self.frames = list()
        self.screen = screen
        self.cutFrames(img, count, w, h)
        self.image = self.frames[0]
        self.rect.x = x
        self.rect.y = y

    def cutFrames(self, sheet, count, w, h):
        self.rect = pygame.Rect(0, 0, w, h)
        sheet = pygame.transform.scale(sheet, (w * count, h))
        for i in range(count):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
