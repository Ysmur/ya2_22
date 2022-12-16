import os
import sys
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self, app):
        super().__init__(app.all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = app.height


class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png")

    def __init__(self, app, pos):
        super().__init__(app.all_sprites)
        self.app = app
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    # def update(self):
    #     self.rect = self.rect.move(0, 1)
    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, self.app.mountain):
            self.rect = self.rect.move(0, 1)


class App:
    def __init__(self):
        pygame.init()
        size = self.width, self.height = 501, 501
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('desant')
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.all_sprites = pygame.sprite.Group()
        self.running = True


    def main(self):
        self.mountain = Mountain(self)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Landing(self, event.pos)

            self.screen.fill((255, 255, 255))
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        pygame.quit()


if __name__ == '__main__':
    app = App()
    app.main()
