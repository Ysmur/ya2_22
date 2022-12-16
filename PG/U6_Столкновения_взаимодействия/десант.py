import pygame


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
