import os
import pygame
import random
import sys
from final_screen import final_game_screen
from main_functions import *


def build_level():
    for i in range(13):
        Tile("block", i, 7)


size = WIDTH, HEIGHT = 645, 400
tile_size = 50
score_coins = 0
score_time = 0
XP = 5
onGround = False
jump = False
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
NEW_BEST = 'Вы попадаете в таблицу лидеров!'

tile_images = {
    'block': load_image('BlackForrest/block.png'),
    'eye': load_image('BlackForrest/Eye_1_pos.png', color_key=-1),
    'hero': load_image("BlackForrest/Hero3_1_pos.png", color_key=-1)
}

coin_images = [load_image("BlackForrest/Coin_1_pos.png", color_key=-1),
               load_image("BlackForrest/Coin_2_pos.png", color_key=-1),
               load_image("BlackForrest/Coin_3_pos.png", color_key=-1),
               load_image("BlackForrest/Coin_4_pos.png", color_key=-1)]

false_coin_images = [pygame.transform.scale(load_image("BlackForrest/False_coin_1_pos.png", color_key=-1), (16, 16)),
                     pygame.transform.scale(load_image("BlackForrest/False_coin_2_pos.png", color_key=-1), (16, 16)),
                     pygame.transform.scale(load_image("BlackForrest/False_coin_3_pos.png", color_key=-1), (16, 16)),
                     pygame.transform.scale(load_image("BlackForrest/False_coin_4_pos.png", color_key=-1), (16, 16))]

mushroom_images = [load_image("BlackForrest/Mushroom_1_pos.png", color_key=-1),
                   load_image("BlackForrest/Mushroom_2_pos.png", color_key=-1),
                   load_image("BlackForrest/Mushroom_3_pos.png", color_key=-1),
                   load_image("BlackForrest/Mushroom_4_pos.png", color_key=-1),
                   load_image("BlackForrest/Mushroom_5_pos.png", color_key=-1),
                   load_image("BlackForrest/Mushroom_6_pos.png", color_key=-1),
                   load_image("BlackForrest/Mushroom_7_pos.png", color_key=-1),
                   load_image("BlackForrest/Mushroom_8_pos.png", color_key=-1)]

mushroom_reverse_images = [load_image("BlackForrest/m_Mushroom_1_pos.png", color_key=-1),
                           load_image("BlackForrest/m_Mushroom_2_pos.png", color_key=-1),
                           load_image("BlackForrest/m_Mushroom_3_pos.png", color_key=-1),
                           load_image("BlackForrest/m_Mushroom_4_pos.png", color_key=-1),
                           load_image("BlackForrest/m_Mushroom_5_pos.png", color_key=-1),
                           load_image("BlackForrest/m_Mushroom_6_pos.png", color_key=-1),
                           load_image("BlackForrest/m_Mushroom_7_pos.png", color_key=-1),
                           load_image("BlackForrest/m_Mushroom_8_pos.png", color_key=-1)]

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
false_coin_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()
mushroom_group = pygame.sprite.Group()
flying_eye = pygame.sprite.Group()
exit_img = pygame.transform.scale(load_image("BlackForrest/exit_btn.png", color_key=-1), (88, 38))
restart_img = pygame.transform.scale(load_image("BlackForrest/restart_btn.png", color_key=-1), (88, 38))
coins = AnimatedSprite(load_image("BlackForrest/Coin_Sheet.png", color_key=-1), 4, 1, 6, 0, menu_group, 10)
clocks = AnimatedSprite(load_image("BlackForrest/clocks.png", color_key=-1), 7, 2, tile_size * 2, 0, menu_group, 10)
heart_pic = load_image("BlackForrest/heart_sheet1.png", color_key=-1)
start_img = load_image("BlackForrest/start_button.png", color_key=-1)
back_img = load_image("BlackForrest/back_img.png", color_key=-1)
hero_right = load_image("BlackForrest/Hero3_1_pos.png", color_key=-1)
hero_left = pygame.transform.flip(load_image("BlackForrest/Hero3_1_pos.png", color_key=-1), True, False)
hero_jump_right = load_image("BlackForrest/hero_jump.png", color_key=-1)
hero_jump_left = pygame.transform.flip(load_image("BlackForrest/hero_jump.png", color_key=-1), True, False)
back_img = pygame.transform.scale(back_img, (86, 41))
start_img = pygame.transform.scale(start_img, (148, 68))
heart_pic = pygame.transform.scale(heart_pic, (256, 26))
heart = AnimatedSprite(heart_pic, 4, 1, tile_size * 4 - 15, 0, menu_group, 10)


def menu_forrest_game(dic_game):
    pygame.display.set_caption('Black Forrest')
    pygame.display.set_icon(load_image("BlackForrest/Black_Forrest.ico"))
    pygame.mixer.music.load("Data/BlackForrest/start_window_black_forrest.mp3")
    pygame.mixer.music.play()
    pygame.mouse.set_visible(True)
    intro_text = ["Black Forrest"]
    fon = pygame.transform.scale(load_image("BlackForrest/font_start.png"), size)
    screen.blit(fon, (0, 0))
    start_btn = Button(WIDTH // 2 - start_img.get_width() // 2,
                       HEIGHT // 2 - start_img.get_height() // 2 + 50, start_img)
    go_back = Button(10, 10, back_img)
    text_coord = 60
    font = pygame.font.Font("data/BlackForrest/SilafejiraRegular.otf", 60)
    # menu = Button(screen_width // 2 - menu_img.get_width() // 2,
    #              screen_height // 2 - menu_img.get_height() // 2, menu_img)

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(0, 135, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        if line == "Black Forrest":
            intro_rect.x = (WIDTH - 253) // 2 + 2
        else:
            intro_rect.x = 225
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while dic_game['forrest_menu']:
        sound_button = pygame.mixer.Sound("Data/BlackForrest/button (2).mp3")
        start_btn.update()
        go_back.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.pause()
                dic_game['forrest_menu'] = False
                dic_game['game'] = False

        if start_btn.clicked:
            sound_button.play()
            pygame.mixer.music.pause()
            dic_game['forrest_game'] = True
            dic_game['forrest_menu'] = False

        if go_back.clicked:
            pygame.mixer.music.pause()
            sound_button.play()
            dic_game['forrest_menu'] = False
            dic_game['houses'] = True

        pygame.display.flip()
    return dic_game


def res_of_play_forrest(dic_game):
    """Здесь можно выводить результат игры"""
    global hero, XP, score_time, score_coins, black_forrest, mushroom, restart_img, pressed
    pressed = False
    sound_button = pygame.mixer.Sound("Data/BlackForrest/button (2).mp3")
    if hero.died:
        pygame.mixer.music.pause()
        pygame.mixer.music.load("Data/BlackForrest/You_died.mp3")
        pygame.mixer.music.play()
        counter = 0
        bg = pygame.transform.scale(load_image('BlackForrest/demon_bg.png'), (645, 400))
        fon = pygame.transform.scale(load_image('BlackForrest/you_died.png', color_key=-1), (645, 400))
        while True:
            counter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.pause()
                    dic_game['forrest_res'] = False
                    dic_game['game'] = False
                elif (event.type == pygame.KEYDOWN or
                      event.type == pygame.MOUSEBUTTONDOWN) and counter > 200:
                    pygame.mixer.music.pause()
                    pressed = True
            screen.blit(bg, (0, 0))
            screen.blit(fon, (0, 0))

            pygame.display.flip()
            if pressed or not dic_game['forrest_res']:
                break
    if pressed:
        if score_coins > 50:
            time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
            intro_text = ["You did it!", "", f'Time: {time}',
                          '', f"Coins: {score_coins}",
                          f"{NEW_BEST if check_new_table('forrest', int(score_coins), time) else ''}"]
            pygame.mixer.music.load("Data/BlackForrest/dark_souls_15. Four Kings.mp3")
            fon = pygame.transform.scale(load_image('BlackForrest/you_won.png'), size)
        else:
            time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
            intro_text = ["You died! I'm sorry...", "",
                          f'Time: {time}', '', f"Coins: {score_coins}"]
            pygame.mixer.music.load("Data/BlackForrest/when_you_lose.mp3")
            fon = pygame.transform.scale(load_image('BlackForrest/you_not_won.png'), size)
        pygame.mixer.music.play()
        restart = Button(50, HEIGHT - 87, restart_img)

        exit_btn = Button(WIDTH - 50 - 88, HEIGHT - 87, exit_img)

        while dic_game['forrest_res']:
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.pause()
                    dic_game['forrest_res'] = False
                    dic_game['game'] = False
            screen.blit(fon, (0, 0))
            draw_text(intro_text, Font="data/BlackForrest/SilafejiraRegular.otf",
                      color=pygame.Color(255, 150, 150))  # было 255, 96, 66 плохо видно
            restart.update()
            exit_btn.update()
            pygame.display.flip()

            if restart.clicked:
                sound_button.play()
                pygame.mixer.music.pause()
                all_sprites.empty()
                false_coin_group.empty()
                hero.kill()
                mushroom.kill()
                score_time = 0
                score_coins = 0
                XP = 5
                black_forrest = BlackForrest()
                hero = Player(6, 6)
                mushroom = Mushroom()

                Border(-1, -1, WIDTH + 1, -1)  # Верхняя граница
                Border(-1, HEIGHT + 1, WIDTH + 1, HEIGHT + 1)  # Нижняя граница
                Border(-10, -1, -10, HEIGHT + 1)
                Border(WIDTH + 10, -1, WIDTH + 10, HEIGHT + 1)

                dic_game['forrest_res'] = False
                dic_game['forrest_game'] = True
            if exit_btn.clicked:
                pygame.mixer.music.stop()
                sound_button.play()
                dic_game['authors'] = True
                dic_game['forrest_res'] = False
    return dic_game


class BlackForrest(pygame.sprite.Sprite):
    image = load_image("BlackForrest/my_font.png", color_key=None)
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = BlackForrest.image
        self.rect = self.image.get_rect()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)

        if tile_type == 'block':  # Нужно для того, чтобы монетки, падая, пропадали
            self.add(block_group, tiles_group, all_sprites)
        elif tile_type == 'eye':
            self.add(flying_eye, tiles_group, all_sprites)
        else:
            self.add(tiles_group, all_sprites)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = tile_images['hero']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.counter = 0
        self.sound1 = pygame.mixer.Sound('Data/BlackForrest/jump.mp3')
        self.sound1.set_volume(0.5)
        self.sound2 = pygame.mixer.Sound('Data/BlackForrest/shag.mp3')
        self.sound3 = pygame.mixer.Sound('Data/BlackForrest/coin..mp3')
        self.sound4 = pygame.mixer.Sound('Data/BlackForrest/smeh.mp3')
        self.died = False
        # self.onGround = onGround
        self.add(player_group, all_sprites)

    def move_up(self):
        if hero.image == hero_right:
            hero.image = hero_jump_right
        elif hero.image == hero_left:
            hero.image = hero_jump_left
        self.sound1.play()
        self.rect = self.rect.move(0, -10)
        global onGround
        global jump
        if self.rect.y > HEIGHT - 200:
            jump = True
        else:
            jump = False
        onGround = True

    def move_down(self):  # Потом обязательно удалю :3
        self.rect = self.rect.move(0, +50)

    def move_left(self):
        hero.image = hero_left
        self.sound2.play()
        self.rect = self.rect.move(-50, 0)

    def move_right(self):
        hero.image = hero_right
        self.sound2.play()
        self.rect = self.rect.move(+50, 0)

    def fall(self):
        if self.rect.y < 300:
            self.rect = self.rect.move(0, +5)
        else:
            global onGround
            onGround = False
            if hero.image == hero_jump_left:
                hero.image = hero_left
            if hero.image == hero_jump_right:
                hero.image = hero_right

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, mushroom_group):
            self.sound4.play()
            global XP
            self.counter += 1
            if self.counter == 1 or self.counter % 5 == 0:
                XP -= 1
                if XP <= 0:
                    self.kill()
                    mushroom.kill()
        else:
            self.counter = 0


class Coins(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        list_with_blocks_centers = [17, 67, 117, 167, 217, 267, 317, 367, 417, 467, 517, 567]
        self.image = coin_images[0]
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = list_with_blocks_centers[random.randint(0, 11)]
        self.rect.y = 0
        self.counter = 0
        self.add(coins_group, all_sprites)

    def update(self, *args):
        self.rect = self.rect.move(0, +1)
        if self.rect.y % 8 == 0:
            self.counter += 1
            self.image = pygame.transform.scale(coin_images[self.counter % 4], (16, 16))


class FalseCoins(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        list_with_blocks_centers = [17, 67, 117, 167, 217, 267, 317, 367, 417, 467, 517, 567]
        self.image = coin_images[0]
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = list_with_blocks_centers[random.randint(0, 11)]
        self.rect.y = 0
        self.counter = 0
        self.add(false_coin_group, all_sprites)

    def update(self, *args):
        self.rect = self.rect.move(0, +1)
        if self.rect.y % 8 == 0:
            self.counter += 1
            self.image = pygame.transform.scale(false_coin_images[self.counter % 4], (16, 16))


class Mushroom(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = mushroom_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 1
        self.rect.y = HEIGHT - 85
        self.counter = 0
        self.add(mushroom_group, all_sprites)

    def update(self, *args):
        if self.rect.x % 10 == 0:
            self.counter += 1
            if self.image in mushroom_images:
                self.image = mushroom_images[self.counter % 8]
            elif self.image in mushroom_reverse_images:
                self.image = mushroom_reverse_images[self.counter % 8]
        if self.rect.x < WIDTH - 25 and self.image in mushroom_images:
            self.rect = self.rect.move(+1, 0)
        elif WIDTH - 25 > self.rect.x > 0 and self.image in mushroom_reverse_images:
            self.rect = self.rect.move(-1, 0)
        elif self.rect.x >= WIDTH - tile_size and self.image in mushroom_images:
            self.image = mushroom_reverse_images[self.counter % 8]
            self.rect = self.rect.move(-1, 0)
        elif self.rect.x <= 0 and self.image in mushroom_reverse_images:
            self.image = mushroom_images[self.counter % 8]
            self.rect = self.rect.move(+1, 0)


class Border(pygame.sprite.Sprite):
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


black_forrest = BlackForrest()
hero = Player(6, 6)
mushroom = Mushroom()

Border(-1, -1, WIDTH + 1, -1)  # Верхняя граница
Border(-1, HEIGHT + 1, WIDTH + 1, HEIGHT + 1)  # Нижняя граница
Border(-10, -1, -10, HEIGHT + 1)
Border(WIDTH + 10, -1, WIDTH + 10, HEIGHT + 1)

pygame.init()
pygame.mixer.init()


def game_forrest(dic_game):
    global score_coins, XP

    pygame.display.set_caption('Black Forrest')
    pygame.display.set_icon(load_image("BlackForrest/Black_Forrest.ico"))
    pygame.mixer.music.load('Data/BlackForrest/Yuka Kitamura - Dark Souls III Soundtrack OST - Main Menu Theme.mp3')
    pygame.mixer.music.play()
    build_level()
    fps = 85
    global score_time
    while dic_game['forrest_game']:
        pygame.mouse.set_visible(False)
        score_time += 1
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dic_game['forrest_game'] = False
                dic_game['game'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not onGround:
                hero.move_up()
                if pygame.sprite.spritecollideany(hero, horizontal_borders):
                    hero.move_down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hero.move_left()
                    if pygame.sprite.spritecollideany(hero, vertical_borders):
                        hero.move_right()
                if event.key == pygame.K_RIGHT:
                    hero.move_right()
                    if pygame.sprite.spritecollideany(hero, vertical_borders):
                        hero.move_left()

        if pygame.sprite.groupcollide(player_group, false_coin_group, False, True):
            hero.sound1.stop()
            sound5 = pygame.mixer.Sound("Data/BlackForrest/fall_coin.mp3")
            sound5.play()
            score_coins -= 10
            if score_coins <= 0:
                score_coins = 0
                hero.died = True

            if score_coins == 0:
                draw_mini_text(f'X {score_coins}', (184, 15, 10), (tile_size, 12),
                               Font="data/BlackForrest/SilafejiraRegular.otf", size=25)
                dic_game['forrest_game'] = False
                dic_game['forrest_res'] = True

        if pygame.sprite.groupcollide(player_group, coins_group, False, True):
            hero.sound1.stop()
            sound3 = pygame.mixer.Sound("Data/BlackForrest/coin..mp3")
            sound3.play()
            score_coins += 1

        if jump:  # Если герой не достиг конечной точки прыжка
            hero.move_up()
        if onGround:  # Если герой не земле
            hero.fall()

        if score_time % 100 == 0 and score_time % 1000 != 0:
            Coins()

        if score_time % 1000 == 0:
            FalseCoins()

        screen.fill(pygame.Color("black"))
        all_sprites.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, tile_size // 2))
        draw_mini_text(f'X {score_coins}', (184, 15, 10), (tile_size, 12),
                       Font="data/BlackForrest/SilafejiraRegular.otf", size=25)
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_mini_text(f'  {time}', (184, 15, 10), (tile_size * 3, 12),
                       Font="data/BlackForrest/SilafejiraRegular.otf", size=25)
        draw_mini_text(f'X  {XP}', (184, 15, 10), (tile_size * 5, 12),
                       Font="data/BlackForrest/SilafejiraRegular.otf", size=25)
        menu_group.draw(screen)
        menu_group.update()
        pygame.display.flip()

        if pygame.sprite.groupcollide(false_coin_group, mushroom_group, True, False):
            sound5 = pygame.mixer.Sound("Data/BlackForrest/fall_coin.mp3")
            sound5.play()
            mushroom_group.empty()
            mushroom.kill()

        if pygame.sprite.groupcollide(coins_group, block_group, True, False):
            XP -= 1

        pygame.sprite.groupcollide(false_coin_group, block_group, True, False)
        pygame.sprite.groupcollide(coins_group, mushroom_group, True, False)

        if XP <= 0:
            hero.died = True
            dic_game['forrest_game'] = False
            dic_game['forrest_res'] = True
        clock.tick(fps)
    return dic_game


if __name__ == '__main__':
    dic_game = {'houses': False, 'authors': False, 'table': False, 'game': True,
                'mario_game': False, 'mario_menu': False, 'mario_res': False,
                'snow_game': False, 'snow_menu': False, 'snow_res': False,
                'forrest_game': False, 'forrest_menu': True, 'forrest_res': False}
    while dic_game['game']:
        if dic_game['houses']:
            dic_game['forrest_menu'] = True
            dic_game['houses'] = False
        if dic_game['forrest_menu']:
            dic_game = menu_forrest_game(dic_game)
        if dic_game['forrest_game']:
            dic_game = game_forrest(dic_game)
        if dic_game['forrest_res']:
            dic_game = res_of_play_forrest(dic_game)
        if dic_game['authors']:
            dic_game = final_game_screen(dic_game)
        if not dic_game['game']:
            break
