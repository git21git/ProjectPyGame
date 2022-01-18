"""В этом файле собраны основные функции, необходимые для функционирования проекта
    (для исключения повторения их в файлах проекта)"""
import os
import pygame
import sys

pygame.init()
size = screen_width, screen_height = (645, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyPurble Game Studio')  # Название приложения


def load_image(name, color_key=None):
    """Функция для загрузки изображения"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    """Функция для завершения работы приложения"""
    pygame.quit()
    sys.exit()


def load_level(filename):
    """Функция для загрузки уровня"""
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


class Button:
    """Класс всех кнопок"""

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def update(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)


def draw_text(intro_text, Font=None, color=pygame.Color('white')):
    """Функция для отображения текста"""
    font = pygame.font.Font(Font, 40)
    text_coord = 50
    for line in intro_text:
        text = font.render(line, True, color)
        text_x = screen_width // 2 - text.get_width() // 2
        text_y = text_coord + text.get_height()
        text_coord = text_y + 10
        screen.blit(text, (text_x, text_y))


def draw_mini_text(text, color, pos, Font=None, size=20):
    """Рисование текста маленького размера для меню"""
    font = pygame.font.Font(Font, size)
    x, y = pos
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
