from main_functions import *
import random

def start_screen():
    """Функция вызова(отображения) стартового экрана"""
    fon = pygame.transform.scale(load_image('start.png'), (WIDTH, HEIGHT))  # стартовая картинка
    screen.blit(fon, (0, 0))
    houses.update()
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход из игры
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                houses.update(pygame.mouse, 1)
                game_screen()  # переход дальше
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                houses.update(pygame.mouse)
        screen.blit(fon, (0, 0))
        houses.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


class House_1(pygame.sprite.Sprite):
    image_small = load_image("house_1_small.png", color_key=-1)
    image_big = load_image("house_1_big.png", color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = House_1.image_small
        self.rect = self.image_small.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            self.image = self.image_big
            self.rect.x = self.pos[0] - 2
            self.rect.y = self.pos[1] - 2
        else:
            self.image = self.image_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]


class House_2(pygame.sprite.Sprite):
    image_small = load_image("house_2_small.png", color_key=-1)
    image_big = load_image("house_2_big.png", color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = House_1.image_small
        self.rect = self.image_small.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            self.image = self.image_big
            self.rect.x = self.pos[0] - 2
            self.rect.y = self.pos[1] - 2
        else:
            self.image = self.image_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]


class House_3(pygame.sprite.Sprite):
    image_small = load_image("house_3_small.png", color_key=-1)
    image_big = load_image("house_3_big.png", color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = House_1.image_small
        self.rect = self.image_small.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            self.image = self.image_big
            self.rect.x = self.pos[0] - 2
            self.rect.y = self.pos[1] - 2
        else:
            self.image = self.image_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]


class Exit_1(pygame.sprite.Sprite):
    image_small = load_image("exit_small.png", color_key=-1)
    image_big = load_image("exit_big.png", color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = House_1.image_small
        self.rect = self.image_small.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and args[-1] == 1 and self.rect.collidepoint(args[0].get_pos()):
            terminate()
        if args and self.rect.collidepoint(args[0].get_pos()):
            self.image = self.image_big
            self.rect.x = self.pos[0] - 2
            self.rect.y = self.pos[1] - 2
        else:
            self.image = self.image_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]


def game_screen():
    """Функция вызова(отображения) экрана игры"""
    for i in range(10):
        Ball(20, 100, 100)
    running = True
    while running:
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход из игры

            if event.type == pygame.MOUSEBUTTONDOWN:
                # all_sprites.update(event)
                return  # переход дальше
        screen.fill(pygame.Color("white"))
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(fps)


def finish_screen():
    """Функция вызова(отображения) финишного экрана"""
    fon = pygame.transform.scale(load_image('end.png'), (WIDTH, HEIGHT))  # завершающая картинка
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход из игры
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()  # выход из игры
        pygame.display.flip()
        clock.tick(fps)


class Ball(pygame.sprite.Sprite):
    """Класс шариков, которые отскакивают от стенки"""

    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        """функция движения с проверкой столкновение шара со стенками"""
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    """Класс стенок"""

    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


if __name__ == '__main__':
    size = WIDTH, HEIGHT = 645, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ДОПИСАТЬ НАЗВАНИЕ')  # Название приложения
    pygame.display.set_icon(load_image("icon.ico"))  # Иконка приложения

    all_sprites = pygame.sprite.Group()
    houses = pygame.sprite.Group()
    House_1(11, 85, houses)
    House_2(147, 130, houses)
    House_3(425, 132, houses)
    Exit_1(9, 307, houses)
    horizontal_borders = pygame.sprite.Group()
    Border(3, 3, WIDTH - 3, 3)
    Border(3, HEIGHT - 3, WIDTH - 3, HEIGHT - 3)
    vertical_borders = pygame.sprite.Group()
    Border(3, 3, 3, HEIGHT - 3)
    Border(WIDTH - 3, 3, WIDTH - 3, HEIGHT - 3)
    """Таймер"""
    fps = 60
    clock = pygame.time.Clock()
    """Поочередный вызов функций для игры старт - игра - финиш"""
    start_screen()
    game_screen()
    finish_screen()
