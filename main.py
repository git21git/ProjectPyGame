import random
from Game_Alex import menu_forrest_game
from Game_Mary import main_gameplay_snow
from final_screen import final_game_screen
from main_functions import *

size = WIDTH, HEIGHT = 645, 400
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
houses = pygame.sprite.Group()
star_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()

back_img = load_image('snow/back_img.png', color_key=-1)
gold_coins_img = load_image("snow/menu_coins.png", color_key=-1)
menu_clocks_img = load_image("snow/menu_clocks.png", color_key=-1)

running_authors = False
running_mario_res = False
running_houses = True
running_mario_game = False
running_back = False
running_mario_menu = False


class Particle(pygame.sprite.Sprite):
    """Класс для системы частиц(звездочек)"""
    fire = [load_image("star.png", color_key=-1)]
    for scale in (10, 15, 25):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(star_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0.1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    """Функция для создания объектов класса частиц (звездочек)"""
    numbers = range(-6, 5)
    for _ in range(20):
        Particle(position, random.choice(numbers), random.choice(numbers))


def draw_res_text(screen):
    font = pygame.font.Font('data/final/seguisbi.ttf', 28)
    text = font.render('WINNERS SCORE', True, pygame.Color('black'))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 15))
    # Результаты игры Марио
    with open('data/mario/res_mario.txt', encoding="utf8") as file:
        text = file.readlines()
    text_mario = clean_text(text)
    text_coord = 25
    for line in text_mario:
        text = font.render(line, True, pygame.Color('white'))
        text_x = 410 - text.get_width()
        text_y = text_coord + text.get_height() + 10
        text_coord = text_y
        screen.blit(text, (text_x, text_y))

    # Результаты игры Forrest
    with open('data/BlackForrest/res_forrest.txt', encoding="utf8") as file:
        text_forrest = clean_text(file.readlines())
    text_coord = 25
    for line in text_forrest:
        text = font.render(line, True, pygame.Color('white'))
        text_x = 190 - text.get_width()
        text_y = text_coord + text.get_height() + 10
        text_coord = text_y
        screen.blit(text, (text_x, text_y))

    # Результаты игры Snow
    with open('data/snow/res_snow.txt', encoding="utf8") as file:
        text_snow = clean_text(file.readlines())
    text_coord = 25
    for line in text_snow:
        text = font.render(line, True, pygame.Color('white'))
        text_x = 620 - text.get_width()
        text_y = text_coord + text.get_height() + 10
        text_coord = text_y
        screen.blit(text, (text_x, text_y))


class Houses(pygame.sprite.Sprite):
    house_1_small = load_image("start/house_1_small.png", color_key=-1)
    house_1_big = load_image("start/house_1_big.png", color_key=-1)
    house_2_small = load_image("start/house_2_small.png", color_key=-1)
    house_2_big = load_image("start/house_2_big.png", color_key=-1)
    house_3_small = load_image("start/house_3_small.png", color_key=-1)
    house_3_big = load_image("start/house_3_big.png", color_key=-1)
    exit_small = load_image("start/exit_small.png", color_key=-1)
    exit_big = load_image("start/exit_big.png", color_key=-1)
    res_small = load_image("start/res_small.png", color_key=-1)
    res_big = load_image("start/res_big.png", color_key=-1)

    def __init__(self, x, y, group, name):
        super().__init__(group)
        if name == 'exit':
            self.image = Houses.exit_small
        elif name == 'house_1':
            self.image = Houses.house_1_small
        elif name == 'house_2':
            self.image = Houses.house_2_small
        elif name == 'house_3':
            self.image = Houses.house_3_small
        elif name == 'res':
            self.image = Houses.res_small
        self.name = name
        self.rect = self.image.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and args[-1] == 1 and self.rect.collidepoint(args[0].get_pos()):
            terminate()
        if args and self.rect.collidepoint(args[0].get_pos()):
            if self.name == 'exit':
                self.image = Houses.exit_big
            elif self.name == 'house_1':
                self.image = Houses.house_1_big
            elif self.name == 'house_2':
                self.image = Houses.house_2_big
            elif self.name == 'house_3':
                self.image = Houses.house_3_big
            elif self.name == 'res':
                self.image = Houses.res_big
            self.rect.x = self.pos[0] - 4
            self.rect.y = self.pos[1] - 3
        else:
            if self.name == 'exit':
                self.image = Houses.exit_small
            elif self.name == 'house_1':
                self.image = Houses.house_1_small
            elif self.name == 'house_2':
                self.image = Houses.house_2_small
            elif self.name == 'house_3':
                self.image = Houses.house_3_small
            elif self.name == 'res':
                self.image = Houses.res_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def check_push(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            return self.name


Houses(11, 85, houses, 'house_1')
Houses(147, 130, houses, 'house_2')
Houses(425, 132, houses, 'house_3')
Houses(9, 307, houses, 'exit')
Houses(140, 55, houses, 'res')

FPS = 80
onGround = False
tile_images = {
    'exit': load_image('mario/new_level.png', color_key=-1),
    'menu': load_image('mario/menu.png'),
    'menu_coins': load_image("mario/menu_coins.png", color_key=-1),
    'menu_clocks': load_image("mario/menu_clocks.png", color_key=-1),
    'menu_door': load_image("mario/block.png", color_key=-1),
    'dirt': load_image("mario/dirt.png"),
    'grass': load_image("mario/grass.png", color_key=-1),
    'gru_wall': load_image("mario/gru_wall.png", color_key=-1),
    'snow': load_image("mario/snow.png", color_key=-1)
}
player_image = load_image('mario/mario.png', color_key=-1)
start_img = pygame.transform.scale(load_image('mario/start_button.png'), (148, 68))
bg = pygame.transform.scale(load_image('mario/mario (1).jpg'), (WIDTH, HEIGHT))

# back_img = pygame.transform.scale(load_image('mario/back_img.png', color_key=-1), (86, 41))

tile_size = tile_width = tile_height = 50
level_completed = True
cur_level = 8
score_coins = 0
score_time = 0
levels = ['mario/levels/level_1.txt', 'mario/levels/level_2.txt',
          'mario/levels/level_3.txt', 'mario/levels/level_4.txt',
          'mario/levels/level_5.txt', 'mario/levels/level_6.txt',
          'mario/levels/level_7.txt', 'mario/levels/level_8.txt',
          'mario/levels/level_9.txt']
music = ['data/mario/music/portal.mp3', 'data/mario/music/field.mp3',
         'data/mario/music/peace.mp3', 'data/mario/music/peace.mp3',
         'data/mario/music/peace.mp3', 'data/mario/music/castle.mp3',
         'data/mario/music/forest.mp3', 'data/mario/music/win.mp3',
         'data/mario/music/peace.mp3']
f_lvl = [load_image('mario/start_mario.jpg'), load_image('mario/second_peyzaj.jpg'),
         load_image('mario/third_peizaj.jpg'),
         load_image('mario/desert.png'), load_image('mario/fon_4.png'),
         load_image('mario/far_castle.jpeg'), load_image('mario/black_forrest.jpg'),
         load_image('mario/gru.png'), load_image('mario/last_fon.jpg')]  # словарь фонов для уровней
n_lvl = ['Портал в лесу', 'Луг деревни Атрейдес', 'Лечебница Аркрайт',
         'Пустыня Сахара', 'Зимние приключения', 'Проход через горы',
         'Темный лес', 'Злой волшебник', 'Замок принцессы']  # Названия для уровней
max_level = len(levels)
NEW_BEST = 'Вы попадаете в таблицу лидеров!'


def draw_mini_text(text, color, pos):
    """Рисование текста маленького размера для меню (марио)"""
    font = pygame.font.Font(None, 30)
    x, y = pos
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


def generate_level(level):
    new_player, x, y = None, None, None
    list_with_walls = list()
    list_with_walls.clear()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == 'M':
                til = Tile('menu', x, y)
                tile = (til.image, til.rect)
                list_with_walls.append(tile)
            elif level[y][x] == '#':
                wall = Wall(x, y, 'wall')
                tile = (wall.image, wall.rect)
                list_with_walls.append(tile)
            elif level[y][x] == '9':
                wall = Wall(x, y, 'dirt')
                tile = (wall.image, wall.rect)
                list_with_walls.append(tile)
            elif level[y][x] == '8':
                wall = Wall(x, y, 'gru_wall')
                tile = (wall.image, wall.rect)
                list_with_walls.append(tile)
            elif level[y][x] == '5':
                wall = Wall(x, y, 'snow')
                tile = (wall.image, wall.rect)
                list_with_walls.append(tile)
            elif level[y][x] == '@':
                new_player = Player(x, y)
                level[y][x] = "."
            elif level[y][x] == '2':
                Exit(x, y)
            elif level[y][x] == 'P':
                Princess(x, y)
            elif level[y][x] == '*':
                AnimatedSprite(load_image("mario/menu_coins.png", color_key=-1), 3, 2,
                               tile_size * x + tile_size // 4, tile_size * y + tile_size // 4, coins_group, 9)
    return new_player, x, y, list_with_walls


def menu_mario_game():
    global running_mario_menu, running_mario_game, running_houses
    pygame.display.set_caption('Mario: Multiverse')  # Название приложения
    pygame.mixer.music.load("data/mario/music/honor-and-sword-main.mp3")
    pygame.mixer.music.play()
    sound_btn = pygame.mixer.Sound("data/BlackForrest/button (2).mp3")
    pygame.mouse.set_visible(True)
    start_btn = Button(SCREEN_WIDTH // 2 - start_img.get_width() // 2,
                       SCREEN_HEIGHT // 2 - start_img.get_height() // 2, start_img)
    go_back = Button(10, 10, back_img)
    while running_mario_menu:
        screen.blit(bg, (0, 0))
        start_btn.update()
        go_back.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if start_btn.clicked:
            sound_btn.play()
            pygame.mixer.music.stop()
            running_mario_game = True
            running_mario_menu = False
        if go_back.clicked:
            pygame.mixer.music.stop()
            sound_btn.play()
            running_mario_menu = False
            running_houses = True

        pygame.display.flip()


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(Sprite):
    def __init__(self, pos_x, pos_y, name):
        super().__init__(sprite_group)
        if name == 'wall':
            self.image = load_image(f'mario/box{random.choice(range(1, 4))}.png')
        else:
            self.image = tile_images[name]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.add(wall_group)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.index = 0
        self.counter = 0

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.gravity = 0
        self.notOnGround = True
        self.jumped = False
        self.direction = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.start = tile_width * pos_x + 15, tile_height * pos_y + 5
        self.pos = (pos_x, pos_y)
        self.died = False

    def update(self):
        global onGround, level_completed
        move_x = 0
        move_y = 0

        moving = 4

        if not hero.died:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and not self.jumped and not self.notOnGround:
                self.gravity = -17
                self.jumped = True
            if not key[pygame.K_UP]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                move_x -= moving
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                move_x += moving
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
            if self.rect.x >= WIDTH:
                self.rect = self.image.get_rect().move(self.rect.x % WIDTH, self.rect.y)
            if self.rect.x <= 0:
                self.rect = self.image.get_rect().move(WIDTH, self.rect.y)
            if self.rect.y >= HEIGHT:
                self.rect = self.image.get_rect().move(self.start)
            self.gravity += 1
            if self.gravity > 10:
                self.gravity = 10
            move_y += self.gravity

            self.notOnGround = True

            for tile in lst:
                if tile[1].colliderect(self.rect.x + move_x, self.rect.y, self.width, self.height):
                    move_x = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + move_y, self.width, self.height):
                    if self.gravity < 0:
                        move_y = tile[1].bottom - self.rect.top
                        self.gravity = 0

                    elif self.gravity >= 0:
                        move_y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.notOnGround = False

            if pygame.sprite.spritecollide(self, exit_group, False):
                level_completed = True

            self.rect.x += move_x
            self.rect.y += move_y

        screen.blit(self.image, self.rect)


class Exit(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group)
        self.image = tile_images['exit']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)


class Princess(Sprite):
    princess_l = load_image('mario/princess_l.png', color_key=-1)
    princess_r = load_image("mario/princess_r.png", color_key=-1)

    def __init__(self, pos_x, pos_y):
        super().__init__(princess_group)
        self.lst = [Princess.princess_l, Princess.princess_r]
        self.image = Princess.princess_l
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.count = 0

    def update(self):
        if self.count % 109 == 0:
            if self.count % 2 == 0:
                self.image = self.lst[0]
            else:
                self.image = self.lst[1]
        self.count += 1


def res_of_play():
    global score_time, score_coins, lst, cur_level, level_completed, \
        running_mario_res, running_houses, running_authors
    pygame.mouse.set_visible(True)
    if not hero.died:
        for i in range(-300, 310, 50):
            create_particles((WIDTH // 2 + i, 0))
        _ = AnimatedSprite(load_image("snow/coins.png", color_key=-1), 3, 2, 155, 212, res_group, 5)
        _ = AnimatedSprite(load_image("snow/clocks.png", color_key=-1), 7, 2, 148, 130, res_group, 5)
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        intro_text = ["Вы Выиграли. Принцесса спасена!", "", f'Время: {time}',
                      '', f"Монеты: {score_coins}",
                      f"{NEW_BEST if check_new_table('mario', int(score_coins), time) else ''}"]
        fon = pygame.transform.scale(load_image('mario/final_mario.png'), screen_size)
        screen.blit(fon, (0, 0))
        draw_text(intro_text)
    else:
        intro_text = ['']
        fon = load_image('mario/gameover.png', color_key=-1)
    exit_btn = Button(SCREEN_WIDTH / 2 - 117 / 2, 299,
                      pygame.transform.scale(load_image("BlackForrest/exit_btn.png", color_key=-1), (117, 49)))

    while running_mario_res:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
        screen.blit(fon, (0, 0))
        draw_text(intro_text, color=pygame.Color('black'))
        res_group.draw(screen)
        res_group.update()
        star_group.update()
        star_group.draw(screen)
        exit_btn.update()
        if exit_btn.clicked:
            cur_level = 0
            score_coins = 0
            score_time = 0
            level_completed = True
            lst.clear()
            running_houses = True
            running_mario_res = False
        pygame.display.flip()
        clock.tick(FPS)


sprite_group = SpriteGroup()
wall_group = SpriteGroup()
hero_group = SpriteGroup()
exit_group = SpriteGroup()
princess_group = SpriteGroup()
coins_group = SpriteGroup()
res_group = SpriteGroup()
menu_mario_group = SpriteGroup()
# анимация панели меню
coins = AnimatedSprite(tile_images['menu_coins'], 3, 2, 5, 0, menu_mario_group, 9)
clocks = AnimatedSprite(tile_images['menu_clocks'], 7, 2, tile_size * 1.9, 0, menu_mario_group, 6)
door = AnimatedSprite(tile_images['menu_door'], 1, 1, tile_size * 11.5, 0, menu_mario_group, 6)


def open_level(level):
    global hero, max_x, max_y, level_map, lst

    sprite_group.empty()
    hero_group.empty()
    exit_group.empty()
    princess_group.empty()
    coins_group.empty()
    wall_group.empty()
    pygame.mixer.music.load(music[level - 1])
    pygame.mixer.music.play()
    level_map = load_level(levels[level - 1])
    hero, max_x, max_y, lst = generate_level(level_map)


level_map = load_level(levels[cur_level])
hero, max_x, max_y, lst = generate_level(level_map)


def game_mario():
    global score_time, level_completed, cur_level, score_coins, lst, \
        running_mario_game, running_mario_res
    while running_mario_game:
        score_time += 1
        if level_completed:
            pygame.mixer.music.stop()
            cur_level += 1
            open_level(cur_level)
            level_completed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_mario_game = False
                terminate()
        else:
            global onGround
            onGround = False

        fon = pygame.transform.scale(f_lvl[cur_level - 1], (WIDTH, HEIGHT))  # картинка
        screen.blit(fon, (0, 0))
        sprite_group.draw(screen)
        wall_group.draw(screen)
        hero_group.draw(screen)
        exit_group.draw(screen)
        princess_group.draw(screen)
        coins_group.draw(screen)
        coins_group.update()
        hero.update()
        princess_group.update()
        clock.tick(FPS)
        # Меню:
        draw_mini_text(f'X {score_coins}', (255, 255, 255), (tile_size + 5, 15))  # монетки
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_mini_text(f'  {time}', (255, 255, 255), (tile_size * 3, 15))
        draw_mini_text(f'LEVEL {cur_level}: {n_lvl[cur_level - 1]}', (255, 255, 255), (tile_size * 7, 15))
        draw_mini_text(f'X {cur_level - 1}', (255, 255, 255), (WIDTH - tile_size // 2, 15))
        menu_mario_group.draw(screen)
        menu_mario_group.update()
        if pygame.sprite.groupcollide(hero_group, coins_group, False, True):
            sound1 = pygame.mixer.Sound("data/mario/music/coin..mp3")
            sound1.play()
            score_coins += 1
        if pygame.sprite.groupcollide(hero_group, exit_group, False, False):
            level_completed = True
        if pygame.sprite.groupcollide(hero_group, princess_group, False, False):
            pygame.mixer.music.stop()
            running_mario_res = True
            running_mario_game = False
        pygame.display.flip()
    return


def start_progect_screen():
    """Функция вызова(отображения) стартового экрана"""
    global running_houses, running_mario_menu
    fon = pygame.transform.scale(load_image('start/start.png'), (WIDTH, HEIGHT))  # стартовая картинка
    pressed = False
    while running_houses:
        pygame.display.set_caption('PyPurble Game Studio')  # Название приложения
        pygame.display.set_icon(load_image("icon.ico"))  # Иконка приложения
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if pressed:
                    lst = [house.check_push(pygame.mouse) for house in houses]
                    if 'exit' in lst:
                        terminate()
                    elif 'house_3' in lst:
                        main_gameplay_snow()
                    elif 'house_2' in lst:
                        running_houses = False
                        running_mario_menu = True
                    elif 'house_1' in lst:
                        menu_forrest_game()
                    elif 'res' in lst:
                        res_game_screen()

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                houses.update(pygame.mouse)
        screen.blit(fon, (0, 0))
        houses.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    return


def res_game_screen():
    running = True
    fon = pygame.transform.scale(load_image('final/bg.png'), (WIDTH, HEIGHT))
    go_back = Button(10, 5, back_img)
    for i in range(-300, 310, 50):
        create_particles((SCREEN_WIDTH // 2 + i, 0))
    text_coord = 80
    for _ in range(3):
        coins = AnimatedSprite(gold_coins_img, 3, 2, 2, text_coord, menu_group, 9)
        coins = AnimatedSprite(gold_coins_img, 3, 2, 238, text_coord, menu_group, 9)
        coins = AnimatedSprite(gold_coins_img, 3, 2, 438, text_coord, menu_group, 9)
        clocks = AnimatedSprite(menu_clocks_img, 7, 2, 110, text_coord, menu_group, 6)
        clocks = AnimatedSprite(menu_clocks_img, 7, 2, 335, text_coord, menu_group, 6)
        clocks = AnimatedSprite(menu_clocks_img, 7, 2, 540, text_coord, menu_group, 6)
        text_coord += 50

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.K_RETURN and event.key == pygame.K_ESCAPE):
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
                pass
        screen.blit(fon, (0, 0))
        draw_res_text(screen)
        menu_group.draw(screen)
        menu_group.update()
        star_group.update()
        star_group.draw(screen)
        go_back.update()
        if go_back.clicked:
            running = False
        pygame.display.flip()
        clock.tick(FPS)
    return


def main_mario_gameplay_snow():
    """Функция для навигации по игре(возврат в главное меню и тд)"""
    global running_back, running_mario_menu, running_mario_game, running_mario_res, running_authors, running_houses
    running_back = False
    running_houses = True
    while not running_back:
        if running_houses:
            start_progect_screen()
        if running_mario_menu:
            menu_mario_game()
        if running_mario_game:
            game_mario()
        if running_mario_res:
            res_of_play()
        if running_authors:
            running_authors = False
            final_game_screen()

        if running_back:
            break
    return


if __name__ == '__main__':
    main_mario_gameplay_snow()
