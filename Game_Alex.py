import os
import random
import sys

import pygame
from final_screen import final_game_screen
from main_functions import terminate


def build_level():
    for i in range(13):
        Tile("block", i, 7)


def load_image(name, colorkey=None):
    fullname = os.path.join('data/BlackForrest', name)
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


def draw_mini_text(text, color, pos):
    font = pygame.font.Font("data/BlackForrest/SilafejiraRegular.otf", 25)
    x, y = pos
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


def draw_text(intro_text):
    font = pygame.font.Font("data/BlackForrest/SilafejiraRegular.otf", 40)
    text_coord = 50
    for line in intro_text:
        text = font.render(line, True, pygame.Color(255, 96, 66))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = text_coord + text.get_height()
        text_coord = text_y + 10
        screen.blit(text, (text_x, text_y))


class AnimatedSprite(pygame.sprite.Sprite):
    """Класс анимации для спрайтов"""

    def __init__(self, sheet, columns, rows, x, y, group, t):
        super().__init__(group)
        self.count_iteration = 0
        self.timer = t
        self.frames = []
        self.group = group
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


size = WIDTH, HEIGHT = 645, 400
tile_size = 50
score_coins = 0
score_time = 0
XP = 5
onGround = False
jump = False
motion = 'STOP'  # по умолчанию — стоим, флаг для непрерывного движения
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Black Forrest')
pygame.display.set_icon(load_image("Black_Forrest.ico"))
clock = pygame.time.Clock()

tile_images = {
    'block': load_image('block.png'),
    'eye': load_image('Eye_1_pos.png', colorkey=-1),
    'hero': load_image("Hero3_1_pos.png", colorkey=-1)
}

coin_images = [load_image("Coin_1_pos.png", colorkey=-1), load_image("Coin_2_pos.png", colorkey=-1),
               load_image("Coin_3_pos.png", colorkey=-1), load_image("Coin_4_pos.png", colorkey=-1)]

mushroom_images = [load_image("Mushroom_1_pos.png", colorkey=-1),
                   load_image("Mushroom_2_pos.png", colorkey=-1),
                   load_image("Mushroom_3_pos.png", colorkey=-1),
                   load_image("Mushroom_4_pos.png", colorkey=-1),
                   load_image("Mushroom_5_pos.png", colorkey=-1),
                   load_image("Mushroom_6_pos.png", colorkey=-1),
                   load_image("Mushroom_7_pos.png", colorkey=-1),
                   load_image("Mushroom_8_pos.png", colorkey=-1)]

mushroom_reverse_images = [load_image("m_Mushroom_1_pos.png", colorkey=-1),
                           load_image("m_Mushroom_2_pos.png", colorkey=-1),
                           load_image("m_Mushroom_3_pos.png", colorkey=-1),
                           load_image("m_Mushroom_4_pos.png", colorkey=-1),
                           load_image("m_Mushroom_5_pos.png", colorkey=-1),
                           load_image("m_Mushroom_6_pos.png", colorkey=-1),
                           load_image("m_Mushroom_7_pos.png", colorkey=-1),
                           load_image("m_Mushroom_8_pos.png", colorkey=-1)]


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()
mushroom_group = pygame.sprite.Group()
flying_eye = pygame.sprite.Group()
coins = AnimatedSprite(load_image("Coin_Sheet.png", colorkey=-1), 4, 1, 6, 0, menu_group, 10)
clocks = AnimatedSprite(load_image("clocks.png", colorkey=-1), 7, 2, tile_size * 2, 0, menu_group, 10)
heart_pic = load_image("heart_sheet1.png", colorkey=-1)
start_img = load_image("start_button.png", colorkey=-1)
back_img = load_image("back_img.png", colorkey=-1)
back_img = pygame.transform.scale(back_img, (86, 41))
start_img = pygame.transform.scale(start_img, (148, 68))
heart_pic = pygame.transform.scale(heart_pic, (256, 26))
heart = AnimatedSprite(heart_pic, 4, 1, tile_size * 4 - 15, 0, menu_group, 10)


class Button:
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


def intro_game():
    pygame.mouse.set_visible(True)
    intro_text = ["Black Forrest"]
    fon = pygame.transform.scale(load_image("font_start.png"), size)
    screen.blit(fon, (0, 0))
    start_btn = Button(WIDTH // 2 - start_img.get_width() // 2,
                       HEIGHT // 2 - start_img.get_height() // 2 + 50, start_img)
    go_back = Button(10, 10, back_img)
    text_coord = 60
    font = pygame.font.Font("data/BlackForrest/SilafejiraRegular.otf", 60)
    running = True
    # fon = pygame.transform.scale(load_image("font_start.png"), size)
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

    while running:
        start_btn.update()
        go_back.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        if start_btn.clicked:
            return True
        if go_back.clicked:
            terminate()

        pygame.display.flip()


def res_of_play():
    """Здесь можно выводить результат игры"""
    global hero, XP, score_time, score_coins, black_forrest, mushroom
    if hero.died:
        counter = 0
        fon = pygame.transform.scale(load_image('you_died.png'), (645, 400))
        while True:
            counter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif (event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN) and counter > 200:
                    # End()
                    if score_coins > 50:
                        intro_text = ["You did it!", "",
                                      f'Time: {str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}',
                                      '', f"Coins: {score_coins}"]
                        fon = pygame.transform.scale(load_image('you_won.png'), size)
                    else:
                        intro_text = ["You died! I'm sorry...", "",
                                      f'Time: {str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}',
                                      '', f"Coins: {score_coins}"]
                        fon = pygame.transform.scale(load_image('you_not_won.png'), size)
                    restart = Button(50,
                                     HEIGHT - 87,
                                     pygame.transform.scale(load_image("restart_btn.png", colorkey=-1), (88, 38)))

                    exit_btn = Button(WIDTH - 50 - 88,
                                  HEIGHT - 87,
                                  pygame.transform.scale(load_image("exit_btn.png", colorkey=-1), (88, 38)))

                    while True:
                        pygame.mouse.set_visible(True)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                terminate()
                        screen.blit(fon, (0, 0))
                        draw_text(intro_text)
                        restart.update()
                        exit_btn.update()
                        pygame.display.flip()

                        if restart.clicked:
                            print('pressed restart (reset)')
                            all_sprites.empty()
                            hero.kill()
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

                            pygame.init()
                            game_forrest()
                        if exit_btn.clicked:
                            final_game_screen()
            screen.blit(fon, (0, 0))
            pygame.display.flip()


class BlackForrest(pygame.sprite.Sprite):
    image = load_image("my_font.png", colorkey=None)
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
        self.died = False
        # self.onGround = onGround
        self.add(player_group, all_sprites)

    def move_up(self):
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
        self.rect = self.rect.move(-50, 0)

    def move_right(self):
        self.rect = self.rect.move(+50, 0)

    def fall(self):
        if self.rect.y < 300:
            self.rect = self.rect.move(0, +5)
        else:
            global onGround
            onGround = False

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, mushroom_group):
            global XP
            self.counter += 1
            if self.counter == 1 or self.counter % 5 == 0:
                XP -= 1
                if XP == 0:
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
        elif self.rect.x < WIDTH - 25 and self.image in mushroom_reverse_images and self.rect.x > 0:
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


def game_forrest():
    global score_coins, XP, motion
    # start_screen()
    intro_game()
    build_level()
    fps = 85
    # score_time = 0
    clock = pygame.time.Clock()
    global score_time
    running = True
    while running:
        pygame.mouse.set_visible(False)
        infinityRun = False
        score_time += 1
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and onGround == False:
                hero.move_up()
                if pygame.sprite.spritecollideany(hero, horizontal_borders):
                    hero.move_down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    infinityRun = True
                    motion = 'lef'
                    hero.move_left()
                    if pygame.sprite.spritecollideany(hero, vertical_borders):
                        hero.move_right()
                if event.key == pygame.K_RIGHT:
                    infinityRun = True
                    motion = 'righ'
                    hero.move_right()
                    if pygame.sprite.spritecollideany(hero, vertical_borders):
                        hero.move_left()
            if event.type == pygame.KEYUP:
                motion = 'sto'
        if jump:  # Если герой не достиг конечной точки прыжка
            hero.move_up()
        if onGround:  # Если герой не земле
            hero.fall()

        if score_time % 100 == 0:  # Можно использовать как уровень сложности, типо число поменять на 50, если уровень
            #  действительно сложный!
            Coins()
            # print(score_time)
        if score_time % 10 == 0 and not infinityRun:  # реализация плавного непрерывного движения
            if motion == 'left' and hero.rect.x > 0:
                hero.move_left()
            elif motion == 'right' and hero.rect.x < WIDTH - 50:
                hero.move_right()

        screen.fill(pygame.Color("black"))
        all_sprites.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, tile_size // 2))
        draw_mini_text(f'X {score_coins}', (184, 15, 10), (tile_size, 12))
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_mini_text(f'  {time}', (184, 15, 10), (tile_size * 3, 12))
        draw_mini_text(f'X  {XP}', (184, 15, 10), (tile_size * 5, 12))
        menu_group.draw(screen)
        menu_group.update()
        pygame.display.flip()
        if pygame.sprite.groupcollide(player_group, coins_group, False, True):
            score_coins += 1
        if pygame.sprite.groupcollide(coins_group, mushroom_group, True, False):
            """Гриб съел монетку, можно что-то придумать"""
            pass
        if pygame.sprite.groupcollide(coins_group, block_group, True, False):
            XP -= 1
        if XP <= 0:
            hero.died = True
            res_of_play()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    game_forrest()
