# Заготовка игрового поля (1. Расставить клетки на игровом поле нажатиями левой кнопки мышки)
import copy

import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(self.height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x_click, y_click = mouse_pos
        x_cell = (x_click - self.left) // self.cell_size
        y_cell = (y_click - self.top) // self.cell_size
        if x_cell < 0 or x_cell >= self.width or y_cell < 0 or y_cell >= self.height:
            return None
        return x_cell, y_cell

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def on_click(self, cell):
        print(cell)

    # генерацию следующего поколения (метод класса Board)
    def next_move(self):
        # сохраняем поле
        tmp_board = copy.deepcopy(self.board)
        # пересчитываем
        for y in range(self.height):
            for x in range(self.width):
                # сумма окружающих клеток
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        s += self.board[y + dy][x + dx]
                s -= self.board[y][x]
                if s == 3:
                    tmp_board[y][x] = 1
                elif s < 2 or s > 3:
                    tmp_board[y][x] = 0
        # обновляем поле
        self.board = copy.deepcopy(tmp_board)


class Life(Board):
    # создание поля
    def __init__(self, width, height):
        super().__init__(width, height)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    pygame.draw.rect(screen, pygame.Color(0, 255, 0),
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                      self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color("white"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def on_click(self, cell):
        print(cell)
        self.board[cell[1]][cell[0]] = 1


def main():
    pygame.init()
    size = 501, 501
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60

    board = Life(25, 25)
    board.set_view(1, 1, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            # Генерируем следующее поколение по нажатию клавиши "пробел"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                board.next_move()
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()