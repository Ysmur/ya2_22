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

class App:
    def __init__(self):
        pygame.init()
        size = self.width, self.height = 501, 501
        self.screen = pygame.display.set_mode(size)
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

            self.screen.fill((255, 255, 255))
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        pygame.quit()


if __name__ == '__main__':
    app = App()
    app.main()
