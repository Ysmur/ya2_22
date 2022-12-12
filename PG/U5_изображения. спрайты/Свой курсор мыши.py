import os
import random
import sys

import pygame


def load_image(name, colorkey=None):
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


class Arrow():
    def __init__(self, width, height):
        super().__init__()
        self.image = load_image('arrow.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = random.randrange(height - self.rect.height)

    def update(self, *pos):

        if pos:
            pos = pos[0]
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        print(self.rect)



def main():
    pygame.init()
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60

    arrow = Arrow(width, height)
    running = True
    while running:
        # if pygame.mouse.get_focused():
        #     # скрыть системный курсор
        # else:
        #     # не скрывать системный курсор
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                arrow.update(event.pos)

        screen.fill((0, 0, 0))
        screen.blit(arrow.image, arrow.rect)
        if pygame.mouse.get_focused():
            arrow.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()