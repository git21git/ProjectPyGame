import random
from final_screen import final_game_screen
from main_functions import *

pygame.init()
WIDTH, HEIGHT = screen_size = (645, 400)
screen = pygame.display.set_mode(screen_size)
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

back_img = pygame.transform.scale(load_image('mario/back_img.png', color_key=-1), (86, 41))

tile_size = tile_width = tile_height = 50
level_completed = True
cur_level = 0
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


class Particle(Sprite):
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


def menu_mario_game():
    pygame.display.set_caption('Mario: Multiverse')  # Название приложения
    pygame.mixer.music.load("data/mario/music/honor-and-sword-main.mp3")
    pygame.mixer.music.play()
    sound_btn = pygame.mixer.Sound("data/BlackForrest/button (2).mp3")
    pygame.mouse.set_visible(True)
    running = True
    start_btn = Button(SCREEN_WIDTH // 2 - start_img.get_width() // 2,
                       SCREEN_HEIGHT // 2 - start_img.get_height() // 2, start_img)
    go_back = Button(10, 10, back_img)
    while running:
        screen.blit(bg, (0, 0))
        start_btn.update()
        go_back.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if start_btn.clicked:
            sound_btn.play()
            pygame.mixer.music.stop()
            game_mario()
        if go_back.clicked:
            pygame.mixer.music.stop()
            sound_btn.play()
            return True

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
    global score_time, score_coins, lst, cur_level, level_completed
    exit_btn_img = pygame.transform.scale(load_image("BlackForrest/exit_btn.png", color_key=-1), (88, 38))
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                final_game_screen()
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
            menu_mario_game()
        pygame.display.flip()
        clock.tick(FPS)


clock = pygame.time.Clock()
sprite_group = SpriteGroup()
wall_group = SpriteGroup()
hero_group = SpriteGroup()
exit_group = SpriteGroup()
princess_group = SpriteGroup()
menu_group = SpriteGroup()
coins_group = SpriteGroup()
res_group = SpriteGroup()
star_group = pygame.sprite.Group()
# анимация панели меню
coins = AnimatedSprite(tile_images['menu_coins'], 3, 2, 5, 0, menu_group, 9)
clocks = AnimatedSprite(tile_images['menu_clocks'], 7, 2, tile_size * 1.9, 0, menu_group, 6)
door = AnimatedSprite(tile_images['menu_door'], 1, 1, tile_size * 11.5, 0, menu_group, 6)


def start_screen():
    pygame.display.set_caption('Mario: Multiverse')  # Название приложения
    intro_text = ['НУЖНО СДЕЛАТЬ МЕНЮ)))', "",
                  "Герой двигается",
                  "Карта на месте", '', 'Press any to start game']
    fon = pygame.transform.scale(load_image(r'mario\fon.png'), screen_size)
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
    global score_time, level_completed, cur_level, score_coins, lst
    running = True
    while running:
        score_time += 1
        if level_completed:
            pygame.mixer.music.stop()
            cur_level += 1
            open_level(cur_level)
            level_completed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        menu_group.draw(screen)
        menu_group.update()
        if pygame.sprite.groupcollide(hero_group, coins_group, False, True):
            sound1 = pygame.mixer.Sound("data/mario/music/coin..mp3")
            sound1.play()
            score_coins += 1
        if pygame.sprite.groupcollide(hero_group, exit_group, False, False):
            level_completed = True
        if pygame.sprite.groupcollide(hero_group, princess_group, False, False):
            pygame.mixer.music.stop()
            res_of_play()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    game_mario()
