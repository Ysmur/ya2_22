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
        self.flag = False
        self.red_cell = (-1, -1)

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


class Lines(Board):
    # создание поля
    def __init__(self, width, height):
        super().__init__(width, height)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    pygame.draw.circle(screen, pygame.Color(0, 0, 255),
                                       (x * self.cell_size + self.left + self.cell_size // 2,
                                        y * self.cell_size + self.top + self.cell_size // 2),
                                       self.cell_size // 2)
                elif self.board[y][x] == 2:
                    pygame.draw.circle(screen, pygame.Color(255, 0, 0),
                                       (x * self.cell_size + self.left + self.cell_size // 2,
                                        y * self.cell_size + self.top + self.cell_size // 2),
                                       self.cell_size // 2)
                elif self.board[y][x] != -1:
                    font = pygame.font.Font(None, self.cell_size)
                    text = font.render(str(self.board[y][x]), True, (100, 255, 100))
                    screen.blit(text, (x * self.cell_size + self.left, y * self.cell_size + self.top))
                pygame.draw.rect(screen, pygame.Color("white"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def has_path(self, start, finish):
        """ волновой алгоритм"""
        distance = [[100] * self.width for _ in range(self.height)]
        distance[start[1]][start[0]] = 0
        queue = [start]  # кортеж координат стартовой клетки
        while queue:
            x, y = queue.pop(0)  # удаляем первый в очереди
            for dx, dy in (1, 0), (-1, 0), (0, 1), (0, - 1):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                if self.board[y + dy][x + dx] == 0 and distance[y + dy][x + dx] == 100:
                    distance[y + dy][x + dx] = distance[y][x] + 1
                    queue.append((x + dx, y + dy))
        return distance[finish[1]][finish[0]]

    def on_click(self, cell):
        x, y = cell
        if not self.board[y][x] and not self.flag:
            self.board[y][x] = 1  # синий шарик
        elif not self.board[y][x] and self.flag:
            if self.has_path(self.red_cell, cell) != 100:
                self.board[self.red_cell[1]][self.red_cell[0]] = 0
                self.board[cell[1]][cell[0]] = 1
                self.flag = False
        elif self.board[y][x] == 2:
            self.board[y][x] = 1
            self.flag = False
        elif self.board[y][x] == 1 and not self.flag:
            self.board[y][x] = 2  # красный шарик
            self.flag = True
            self.red_cell = cell


def main():
    pygame.init()
    size = 501, 501
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60

    board = Lines(5, 5)
    board.set_view(1, 1, 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()