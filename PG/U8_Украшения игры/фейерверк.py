import os
import random
import sys
import pygame
GRAVITY = 0.1


class Particle(pygame.sprite.Sprite):
    def __init__(self, app, pos, dx, dy):
        super().__init__(app.all_sprites)
        # сгенерируем частицы разного размера
        self.fire = [app.load_image("star.png")]
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect((0, 0, app.width, app.height)):
            self.kill()

class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Mario')
        self.fps = 30
        self.all_sprites = pygame.sprite.Group()


    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def run_game(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # создаём частицы по щелчку мыши
                    self.create_particles(pygame.mouse.get_pos())
            # update

            # render
            self.screen.fill(pygame.Color('blue'))
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def create_particles(self, position):
        # количество создаваемых частиц
        particle_count = 100
        # возможные скорости
        numbers = range(-10, 11)
        for _ in range(particle_count):
            Particle(self, position, random.choice(numbers), random.choice(numbers))


if __name__ == '__main__':
    app = App()
    app.run_game()