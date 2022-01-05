import os
import pygame
import sys
from final_screen import final_game_screen
from main_functions import *

pygame.init()
screen_size = (645, 400)
WIDTH, HEIGHT = 645, 400
screen = pygame.display.set_mode(screen_size)
FPS = 60
tile_images = {
    'wall': load_image('mario/box.png'),
    'empty': load_image('mario/grass.png'),
    'bg': load_image('mario/bg.png'),
    'exit': load_image('mario/new_level.png', color_key=-1),
    'princess': load_image('mario/princess_l.png', color_key=-1),
    'menu': load_image('mario/menu.png')
}
player_image = load_image('mario/mario.png', color_key=-1)

tile_size = tile_width = tile_height = 50
level_completed = False
cur_level = 0
score_time = 0
levels = ['mario/level_1.txt', 'mario/level_2.txt', 'mario/level_3.txt']
n_lvl = ['Начало', 'Так держать', 'Спаси принцессу!']
max_level = min(len(levels) + 1, 5)


def draw_mini_text(text, color, pos):
    """Рисование текста маленького размера для меню (марио)"""
    font = pygame.font.Font(None, 30)
    x, y = pos
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == 'M':
                Tile('menu', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
                level[y][x] = "."
            elif level[y][x] == '2':
                exit = Exit(x, y)
            elif level[y][x] == 'P':
                princess = Princess(x, y)
    return new_player, x, y


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


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


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


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


class Exit(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group)
        self.image = tile_images['exit']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)


class Princess(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group)
        self.image = tile_images['princess']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
exit_group = SpriteGroup()
princess_group = SpriteGroup()
menu_group = SpriteGroup()
clocks = AnimatedSprite(load_image("mario/menu_clocks.png", color_key=-1), 7, 2, tile_size, 0, menu_group, 6)


def start_screen():
    intro_text = ['НУЖНО СДЕЛАТЬ МЕНЮ)))', "",
                  "Герой двигается",
                  "Карта на месте", '', 'Press any to start game']
    fon = pygame.transform.scale(load_image(r'mario\bg.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def move(hero, direction):
    x, y = hero.pos
    if direction == "up":
        if y > 0 and level_map[y - 1][x] in [".", '2', 'P']:
            hero.move(x, y - 1)
    elif direction == "down":
        if y < max_y - 1 and level_map[y + 1][x] in [".", '2', 'P']:
            hero.move(x, y + 1)
    elif direction == "left":
        if x > 0 and level_map[y][x - 1] in [".", '2', 'P']:
            hero.move(x - 1, y)
    elif direction == "right":
        if x < max_x - 1 and level_map[y][x + 1] in [".", '2', 'P']:
            hero.move(x + 1, y)


def open_level(cur_level):
    global hero, max_x, max_y, level_map

    sprite_group.empty()
    hero_group.empty()
    exit_group.empty()
    princess_group.empty()
    menu_group.empty()

    level_map = load_level(levels[cur_level])
    hero, max_x, max_y = generate_level(level_map)


level_map = load_level(levels[cur_level])
hero, max_x, max_y = generate_level(level_map)


def game_mario():
    global running, score_time, level_completed, cur_level
    start_screen()

    while running:
        score_time += 1
        if level_completed:
            cur_level += 1
            if cur_level <= max_level:
                open_level(cur_level)
            else:
                cur_level = max_level + 1
            level_completed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(hero, "up")
                elif event.key == pygame.K_DOWN:
                    move(hero, "down")
                elif event.key == pygame.K_LEFT:
                    move(hero, "left")
                elif event.key == pygame.K_RIGHT:
                    move(hero, "right")
        screen.blit(tile_images['bg'], (0, 0))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        exit_group.draw(screen)
        princess_group.draw(screen)
        clock.tick(FPS)
        # Меню:
        # draw_mini_text(f'X {score_coins}', (255, 255, 255), (tile_size - 10, 12))  # монетки
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_mini_text(f'  {time}', (255, 255, 255), (tile_size * 2, 15))
        draw_mini_text(f'LEVEL {cur_level + 1}: {n_lvl[cur_level]}', (255, 255, 255), (tile_size * 7, 15))
        draw_mini_text(f'X {cur_level}', (255, 255, 255), (WIDTH - tile_size // 2, 12))
        menu_group.draw(screen)
        menu_group.update()
        if pygame.sprite.groupcollide(hero_group, exit_group, False, False):
            level_completed = True
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    game_mario()
