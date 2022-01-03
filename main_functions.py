"""В этом файле собраны основные функции, необходимые для функционирования проекта
    (для исключения повторения их в файлах проекта)"""
import os
import random
import sys

import pygame

pygame.init()
size = screen_width, screen_height = (645, 400)
screen = pygame.display.set_mode(size)


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
