import pygame

pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption('circles')
FPS = 100  # число кадров в секунду
clock = pygame.time.Clock()
circles = []
speed = []
radius = 0


def draw(pos, r):
    pygame.draw.circle(screen, (255, 255, 0), pos, r)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            circles.append(event.pos)
            speed.append([-1, -1])
            radius = 10
            draw(event.pos, radius)

    screen.fill((0, 0, 255))
    for i in range(len(circles)):
        pos_circle = circles[i]
        if pos_circle[0] >= 400 or pos_circle[0] <= 0:
            speed[i][0] = - speed[i][0]
        if pos_circle[1] >= 500 or pos_circle[1] <= 0:
            speed[i][1] = - speed[i][1]
        circles[i] = pos_circle[0] + speed[i][0], pos_circle[1] + speed[i][1]
        draw(circles[i], radius)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()