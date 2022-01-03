import os
import random
import sys

import pygame
from final_screen import final_game_screen
from main_functions import *

pygame.init()
size = screen_width, screen_height = (645, 400)
tile_size = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Снеговик')  # Название приложения
clock = pygame.time.Clock()
fps = 60
WIDTH, HEIGHT = 645, 400
screen_rect = (0, 0, WIDTH, HEIGHT)
# Состояние игры
score_time = 0
score_coins = 0

black = (0, 0, 0)
white = (255, 255, 255)

tile_images = {
    'box': load_image('box.png'),
    'empty': load_image('ice.png'),
    'fire': load_image('fire.png', color_key=-1),
    'exit': load_image('stones.png'),
    'flag': load_image('flag.png', color_key=-1),
    'coin': load_image('coin.png', color_key=-1)
}
player_image = load_image('snowman.png', color_key=-1)
player_image_left = pygame.transform.flip(player_image, True, False)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':  # пусто
                Tile('empty', x, y)
            elif level[y][x] == '#':  # стена
                Tile('box', x, y)
            elif level[y][x] == '@':  # игрок
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = "."
            elif level[y][x] == '%':  # огонь
                Tile('empty', x, y)
                fire = Fire(x, y)
            elif level[y][x] == '*':  # coins
                Tile('empty', x, y)
                coins = Coins(x, y)
            elif level[y][x] == '2':  # exit_next_level
                Tile('empty', x, y)
                coins = Exit(x, y)
            elif level[y][x] == '5':  # final_level_exit
                Tile('empty', x, y)
                finish = Finish(x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)

        if tile_type == 'box':
            self.add(box_group, tiles_group, all_sprites)
        else:
            self.add(tiles_group, all_sprites)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.died = False
        self.add(player_group, all_sprites)

    def move_up(self):
        self.rect = self.rect.move(0, -50)

    def move_down(self):
        self.rect = self.rect.move(0, +50)

    def move_left(self):
        self.rect = self.rect.move(-50, 0)
        if self.image == player_image:
            self.image = player_image_left

    def move_right(self):
        self.rect = self.rect.move(+50, 0)
        if self.image == player_image_left:
            self.image = player_image


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = tile_images['fire']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)

        self.add(fire_group, all_sprites)


#
class Finish(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = tile_images['flag']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(finish_group, all_sprites)


#
class Exit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = tile_images['exit']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(exit_group, all_sprites)


# монетки
class Coins(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = tile_images['coin']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(coins_group, all_sprites)


class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx

        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width

        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy

        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - screen_width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - screen_height // 2)


def draw_text(intro_text):
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        text = font.render(line, True, pygame.Color('white'))
        text_x = screen_width // 2 - text.get_width() // 2
        text_y = text_coord + text.get_height()
        text_coord = text_y + 10
        screen.blit(text, (text_x, text_y))


class Particle(pygame.sprite.Sprite):
    """Класс для системы частиц(звездочек)"""
    fire = [load_image("star.png", color_key=-1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(star_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 0.25

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    """Функция для создания объектов класса частиц (звездочек)"""
    numbers = range(-5, 6)
    for _ in range(20):
        Particle(position, random.choice(numbers), random.choice(numbers))


class AnimatedSprite(pygame.sprite.Sprite):
    """Класс анимации для спрайтов"""

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(res_group)
        self.count_iteration = 0
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
        if self.count_iteration % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


def res_of_play():
    pygame.mouse.set_visible(False)
    if not player.died:
        for i in range(-300, 310, 50):
            create_particles((WIDTH // 2 + i, 0))
        coins = AnimatedSprite(load_image("coins.png", color_key=-1), 3, 2, 155, 212)
        clocks = AnimatedSprite(load_image("clocks.png", color_key=-1), 7, 2, 148, 130)
        intro_text = ["Вы Выиграли!", "",
                      f'Время: {str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}',
                      '', f"Монеты: {score_coins}"]
        fon = pygame.transform.scale(load_image('final.png'), size)
        screen.blit(fon, (0, 0))
        draw_text(intro_text)
    else:
        intro_text = ['']
        fon = load_image('gameover.png', color_key=-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                final_game_screen()
        screen.blit(fon, (0, 0))
        draw_text(intro_text)

        star_group.update()
        star_group.draw(screen)
        res_group.draw(screen)
        res_group.update()
        pygame.display.flip()
        clock.tick(fps)


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
res_group = pygame.sprite.Group()

player, level_x, level_y = generate_level(load_level("level_1.txt"))
camera = Camera((level_x, level_y))
running = True
while running:
    score_time += 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            player.move_up()
            if pygame.sprite.spritecollideany(player, box_group):
                player.move_down()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            player.move_down()
            if pygame.sprite.spritecollideany(player, box_group):
                player.move_up()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            player.move_left()
            if pygame.sprite.spritecollideany(player, box_group):
                player.move_right()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            player.move_right()
            if pygame.sprite.spritecollideany(player, box_group):
                player.move_left()

        if event.type == pygame.QUIT:
            terminate()

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    fire_group.draw(screen)
    coins_group.draw(screen)
    finish_group.draw(screen)
    exit_group.draw(screen)
    player_group.draw(screen)
    if pygame.sprite.groupcollide(player_group, coins_group, False, True):
        score_coins += 1
    if pygame.sprite.groupcollide(player_group, exit_group, False, False):
        res_of_play()
    if pygame.sprite.groupcollide(player_group, finish_group, False, False):
        res_of_play()
        running = False
    if pygame.sprite.groupcollide(player_group, fire_group, False, False):
        player.died = True
        running = False
    if player.died:
        res_of_play()
    pygame.display.flip()
    clock.tick(fps)

terminate()
