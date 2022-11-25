import pygame
pygame.init()
running = True


def draw():
    color_list = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue')]
    k = 0
    if n % 3 == 0:
        k = 1
    if n % 3 == 1:
        k = 0
    if n % 3 == 2:
        k = 2
    for i in range(n):
        pygame.draw.circle(screen, color_list[(i + k) % 3], (w * n, w * n), w * (n - i))


try:
    w, n = [int(i) for i in input().split()]
    width, height = w * n * 2, w * n * 2
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Крест')

    draw()
except ValueError:
    print('Неправильный формат ввода')
    running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
