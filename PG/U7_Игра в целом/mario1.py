import os
import sys
import pygame


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, app):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - app.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - app.height // 2)


class Hero(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        super().__init__(app.player_group, app.all_sprites)
        self.image = app.load_image("mar.png")
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(app.tile_width * pos[0] + 15, app.tile_height * pos[1] + 5)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Tile(pygame.sprite.Sprite):
    def __init__(self, app, tile_type, pos_x, pos_y):
        super().__init__(app.tiles_group, app.all_sprites)
        tile_images = {
            'wall': app.load_image('box.png'),
            'empty': app.load_image('grass.png')
        }
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            app.tile_width * pos_x, app.tile_height * pos_y)


class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 500, 500
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Mario')
        pygame.key.set_repeat(200, 70)
        self.fps = 50
        self.tile_width = self.tile_height = 50
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.hero = None
        self.camera = Camera(self)



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

    def load_level(self, filename):
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile(self, 'empty', x, y)
                elif level[y][x] == '#':
                    Tile(self, 'wall', x, y)
                elif level[y][x] == '@':
                    Tile(self, 'empty', x, y)
                    self.hero = Hero(self, (x, y))
        # вернем игрока, а также размер поля в клетках
        #return #new_player, x, y

    def start_screen(self):
        intro_text = ["ЗАСТАВКА", "",
                      "Правила игры",
                      "Если в правилах несколько строк,",
                      "приходится выводить их построчно"]

        fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.fps)

    def run_game(self):
        run = True
        self.generate_level(self.load_level('map1.txt'))
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                key = pygame.key.get_pressed()
                if key[pygame.K_DOWN]:
                    self.hero.update(self.hero.rect.x, self.hero.rect.y + self.tile_width)
                if key[pygame.K_UP]:
                    self.hero.update(self.hero.rect.x, self.hero.rect.y - self.tile_width)
                if key[pygame.K_RIGHT]:
                    self.hero.update(self.hero.rect.x + self.tile_width, self.hero.rect.y)
                if key[pygame.K_LEFT]:
                    self.hero.update(self.hero.rect.x - self.tile_width, self.hero.rect.y)
            # update

            # render

            self.screen.fill(pygame.Color('blue'))
            #self.all_sprites.draw(self.screen)
            self.tiles_group.draw(self.screen)
            self.player_group.draw(self.screen)
            self.camera.update(self.hero)
            for sprite in self.all_sprites:
                self.camera.apply(sprite)
            pygame.display.flip()
            self.clock.tick(self.fps)




if __name__ == '__main__':
    app = App()
    #app.start_screen()
    app.run_game()