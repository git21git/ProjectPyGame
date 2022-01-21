"""В этом файле собраны основные функции, необходимые для функционирования проекта
    (для исключения повторения их в файлах проекта)"""
import os
import pygame
import random
import sys

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_size = (645, 400)
screen_rect = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)
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


def clean_text(text, flag='RES'):
    clean_txt = []
    if flag == 'RES':
        for c in text:
            coins, time = c.strip().split(';')
            clean_txt.append(f'{coins}       {time}')
    elif flag == 'NEW':
        for c in text:
            coins, time = c.strip().split(';')
            clean_txt.append((int(coins), time))
    elif flag == 'CONVERT':
        for coin, time in text:
            clean_txt.append(f'{coin};{time}')
    return clean_txt


def check_new_table(game, score_coins, score_time):
    """Функция для проверки, попадает ли результат в таблицу лидеров"""
    filename = ''
    changed = False
    if game == 'forrest':
        filename = 'BlackForrest/res_forrest.txt'
    if game == 'mario':
        filename = 'mario/res_mario.txt'
    if game == 'snow':
        filename = 'snow/res_snow.txt'
    with open(f'data/{filename}', mode='r', encoding="utf8") as file:
        text = clean_text(file.readlines(), flag='NEW')
    for i in range(len(text)):
        coin, time = text[i]
        if score_coins > coin:
            text[i] = score_coins, score_time
            changed = True
        if score_coins == coin and time > score_time:
            text[i] = score_coins, score_time
            changed = True
    text = clean_text(text, flag='CONVERT')
    with open(f'data/{filename}', mode='w', encoding="utf8") as file:
        for line in text:
            print(line, file=file)
    return changed


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
        text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        text_y = text_coord + text.get_height()
        text_coord = text_y + 10
        screen.blit(text, (text_x, text_y))


def draw_mini_text(text, color, pos, Font=None, size=20):
    """Рисование текста маленького размера для меню"""
    font = pygame.font.Font(Font, size)
    x, y = pos
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class AnimatedSprite(Sprite):
    """Класс анимации для спрайтов"""

    def __init__(self, sheet, columns, rows, x, y, group, t):
        super().__init__(group)
        self.count_iteration = 0
        self.timer = t
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.count_iteration += 1
        if self.count_iteration % self.timer == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
