import os
import random
import sys

import pygame


def start_screen():
    """Функция вызова(отображения) стартового экрана"""
    fon = pygame.transform.scale(load_image('start.png'), (WIDTH, HEIGHT))  # стартовая картинка
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # выход из игры
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # переход дальше
        pygame.display.flip()
        clock.tick(fps)


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


def terminate():
    """Функция выхода из игры"""
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    """Функция загрузки изображения"""
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


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
