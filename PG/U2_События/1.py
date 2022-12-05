from numpy import subtract
import pygame

pygame.init()

WIDTH, HEIGHT = 501, 501
START_POS = WIDTH // 2, HEIGHT // 2
RADIUS = 20
FPS = 60
SPEED = 200 / FPS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f'К щелчку')


def draw(pos):
    screen.fill('black')
    pygame.draw.circle(screen, 'red', pos, RADIUS)

    pygame.display.update()


def main():
    def get_direction(dist):
        if abs(dist) <= SPEED:
            return 0

        return 1 - int(dist < 0) * 2

    clock = pygame.time.Clock()
    pos = START_POS
    target = pos

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                target = event.pos

        if target != pos:
            direction = tuple(map(get_direction, subtract(target, pos)))
            pos = tuple(map(lambda c: c[0] + SPEED * c[1], zip(pos, direction)))

        draw(pos)
        clock.tick(FPS)


main()
