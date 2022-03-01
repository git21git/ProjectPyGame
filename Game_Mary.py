from final_screen import final_game_screen
from main_functions import *
from pygame import mixer

pygame.mixer.pre_init()
mixer.init()
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_size = (645, 400)
screen_rect = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
tile_size = 50
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
fps = 60
# Состояние игры
score_time = 0
score_coins = 0
score_buckets = 0

NEW_BEST = 'Вы попадаете в таблицу лидеров!'

tile_images = {
    'box': load_image('snow/box.png'),
    'empty': load_image('snow/ice.png'),
    'fire': load_image('snow/fire.png', color_key=-1),
    'exit': load_image('snow/new_level.png', color_key=-1),
    'flag': load_image('snow/flag.png', color_key=-1),
    'coin': load_image('snow/coin.png', color_key=-1),
    'bucket': load_image('snow/bucket.png', color_key=-1),
    'stone': load_image('snow/stones.png')
}
player_image = load_image('snow/snowman.png', color_key=-1)
player_image_up = load_image('snow/snowman_up.png', color_key=-1)
player_image_down = load_image('snow/snowman_down.png', color_key=-1)
player_image_left = load_image('snow/snowman_left.png', color_key=-1)

exit_img = pygame.transform.scale(load_image("BlackForrest/exit_btn.png", color_key=-1), (117, 49))
restart_img = pygame.transform.scale(load_image("BlackForrest/restart_btn.png", color_key=-1), (117, 49))
start_img = load_image('snow/btn_start.png')
bg = load_image('snow/bg.png')
back_img = load_image('snow/back_img.png', color_key=-1)
rules_img = load_image('snow/rules_img.png', color_key=-1)

levels = ['snow/level_1.txt', 'snow/level_2.txt', 'snow/level_3.txt',
          'snow/level_4.txt', 'snow/level_5.txt']
random.shuffle(levels)
levels.append('snow/level_6.txt')
n_lvl = {'snow/level_1.txt': 'Начало', 'snow/level_2.txt': 'Так держать',
         'snow/level_4.txt': 'Продолжай!', 'snow/level_3.txt': 'Бонусный уровень',
         'snow/level_5.txt': 'Black forrest!', 'snow/level_6.txt': 'Финал!'}  # Названия для уровней
max_level = len(levels)
white = (255, 255, 255)
fffon = pygame.transform.scale(load_image('snow/grass.png'), screen_size)
# подключение музыки
main_music_loud = 0.5
signal_sound_loud = 1
coin_sound = pygame.mixer.Sound('data/snow/music/coin.mp3')
coin_sound.set_volume(signal_sound_loud)
buckets_sound = pygame.mixer.Sound('data/snow/music/bucket.mp3')
buckets_sound.set_volume(signal_sound_loud)
stop_fire_sound = pygame.mixer.Sound('data/snow/music/stop_fire.mp3')
stop_fire_sound.set_volume(signal_sound_loud)
new_level_sound = pygame.mixer.Sound('data/snow/music/new_level.mp3')
new_level_sound.set_volume(signal_sound_loud)
game_over_sound = pygame.mixer.Sound('data/snow/music/game_over.mp3')
game_over_sound.set_volume(signal_sound_loud)


def generate_level(level):
    """Функция преобразования уровня из карты"""
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':  # пусто
                Tile('empty', x, y)
            elif level[y][x] == '#':  # стена
                Tile('box', x, y)
            elif level[y][x] == 'B':  # стена
                Tile('box1', x, y)
            elif level[y][x] == '@':  # игрок
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = "."
            elif level[y][x] == '%':  # огонь
                Tile('empty', x, y)
                _ = Fire(x, y)
            elif level[y][x] == 'V':  # камни
                Tile('empty', x, y)
                _ = Stones(x, y)
            elif level[y][x] == '*':  # coins
                Tile('empty', x, y)
                _ = Coins(x, y)
            elif level[y][x] == '2':  # exit_next_level
                Tile('empty', x, y)
                _ = Exit(x, y)
            elif level[y][x] == '5':  # final_level_exit
                Tile('empty', x, y)
                _ = Finish(x, y)
            elif level[y][x] == '0':  # ведро с водой
                Tile('empty', x, y)
                _ = Bucket(x, y)
    return new_player, x, y


def open_level(level):
    """Функция открытия нового уровня"""
    global camera, player, level_x, level_y, level_map

    all_sprites.empty()
    player_group.empty()
    tiles_group.empty()
    box_group.empty()
    fire_group.empty()
    coins_group.empty()
    exit_group.empty()
    finish_group.empty()
    star_group.empty()
    res_group.empty()
    bucket_group.empty()
    stones_group.empty()

    level_map = load_level(levels[level])
    print(levels[level])
    player, level_x, level_y = generate_level(level_map)
    camera = Camera((level_x, level_y))


class Tile(Sprite):
    """Класс Тайла уровня"""

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)

        if tile_type == 'box':
            self.add(box_group, tiles_group, all_sprites)
        else:
            self.add(tiles_group, all_sprites)


class Player(Sprite):
    """Класс игрока"""

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.died = False
        self.pos = [pos_x, pos_y]
        self.add(player_group, all_sprites)

    def move(self, direction, x, y):
        speed = tile_size
        if direction == 'up':
            self.rect = self.rect.move(0, -speed)
            self.pos[1] = y
            self.image = player_image_up
        elif direction == 'down':
            self.rect = self.rect.move(0, +speed)
            self.pos[1] = y
            self.image = player_image_down
        elif direction == 'left':
            self.rect = self.rect.move(-speed, 0)
            self.pos[0] = x
            self.image = player_image_left
        elif direction == 'right':
            self.rect = self.rect.move(+speed, 0)
            self.pos[0] = x
            self.image = player_image


class Fire(Sprite):
    """Класс Костра"""

    def __init__(self, pos_x, pos_y):
        super().__init__(fire_group)
        self.image = tile_images['fire']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)

        self.add(fire_group, all_sprites)


class Stones(Sprite):
    """Класс камней"""

    def __init__(self, pos_x, pos_y):
        super().__init__(stones_group)
        self.image = tile_images['stone']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)

        self.add(stones_group, all_sprites)


class Bucket(Sprite):
    """Класс ведра с водой"""

    def __init__(self, pos_x, pos_y):
        super().__init__(bucket_group)
        self.image = tile_images['bucket']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)

        self.add(bucket_group, all_sprites)


class Finish(Sprite):
    """Класс финишного флага"""

    def __init__(self, pos_x, pos_y):
        super().__init__(finish_group)
        self.image = tile_images['flag']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(finish_group, all_sprites)


class Exit(Sprite):
    """Класс перехода на новый уровень"""

    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group)
        self.image = tile_images['exit']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(exit_group, all_sprites)


class Coins(Sprite):
    """Класс монеток"""

    def __init__(self, pos_x, pos_y):
        super().__init__(coins_group)
        self.image = tile_images['coin']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(coins_group, all_sprites)


class Camera:
    """Класс камеры"""

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
        self.dx = -(target.rect.x + target.rect.w // 2 - SCREEN_WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - SCREEN_HEIGHT // 2)


def menu_snowman_game(dic_game):
    """Функция меню игры"""
    pygame.display.set_caption('Snow_Snow')
    pygame.display.set_icon(load_image("icon.ico"))  # Иконка приложения
    pygame.mouse.set_visible(True)
    start_btn = Button(SCREEN_WIDTH // 2 - start_img.get_width() // 2,
                       SCREEN_HEIGHT // 2 - start_img.get_height() - 20, start_img)
    go_back = Button(10, 10, back_img)
    rules = Button(SCREEN_WIDTH // 2 - rules_img.get_width() // 2,
                   SCREEN_HEIGHT // 2 + 20, rules_img)
    while dic_game['snow_menu']:
        fon = pygame.transform.scale(bg, screen_size)
        screen.blit(fon, (0, 0))
        start_btn.update()
        go_back.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dic_game['game'] = False
                dic_game['snow_menu'] = False

        if start_btn.clicked:
            dic_game['snow_game'] = True
            dic_game['snow_menu'] = False
        if rules.clicked:
            print('rules')
        if go_back.clicked:
            dic_game['houses'] = True
            dic_game['snow_menu'] = False

        pygame.display.flip()
    return dic_game


class Particle(Sprite):
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


def res_of_play_snow(dic_game):
    """Функция окна результатов игры"""
    global score_time, score_coins, cur_level, \
        level_completed, exit_img, NEW_BEST, restart_img
    pygame.mouse.set_visible(True)
    exit_btn = Button(500, 350, exit_img)
    restart_btn = Button(35, 350, restart_img)
    res_group.empty()
    if not player.died:
        for i in range(-300, 310, 50):
            create_particles((SCREEN_WIDTH // 2 + i, 0))
        _ = AnimatedSprite(load_image("snow/coins.png", color_key=-1), 3, 2, 155, 212, res_group, 5)
        _ = AnimatedSprite(load_image("snow/clocks.png", color_key=-1), 7, 2, 148, 130, res_group, 5)
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        intro_text = ["Вы Выиграли!", "", f'Время: {time}', '', f"Монеты: {score_coins}",
                      f"{NEW_BEST if check_new_table('snow', int(score_coins), time) else ''}"]
        fon = pygame.transform.scale(load_image('final.png'), screen_size)
        screen.blit(fon, (0, 0))
        draw_text(intro_text)
    else:
        intro_text = ['']
        fon = load_image('snow/gameover.png', color_key=-1)

    while dic_game['snow_res']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dic_game['game'] = False
                dic_game['snow_res'] = False
        screen.blit(fon, (0, 0))
        draw_text(intro_text)

        star_group.update()
        star_group.draw(screen)
        res_group.draw(screen)
        res_group.update()
        exit_btn.update()
        restart_btn.update()
        pygame.display.flip()
        clock.tick(fps)
        if restart_btn.clicked:
            cur_level = 0
            score_coins = 0
            score_time = 0
            level_completed = False
            open_level(cur_level)
            dic_game['snow_res'] = False
            dic_game['snow_game'] = True
        if exit_btn.clicked:
            cur_level = 0
            score_coins = 0
            score_time = 0
            level_completed = False
            open_level(cur_level)
            dic_game['snow_res'] = False
            dic_game['authors'] = True

    return dic_game


"""Группы спрайтов"""
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
bucket_group = pygame.sprite.Group()
stones_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()
# меню
coins = AnimatedSprite(load_image("snow/menu_coins.png", color_key=-1), 3, 2, 5, 0, menu_group, 9)
clocks = AnimatedSprite(load_image("snow/menu_clocks.png", color_key=-1), 7, 2, tile_size + 12, 0, menu_group, 6)
waters = AnimatedSprite(load_image("snow/menu_water.png", color_key=-1), 3, 2, tile_size * 2.9, 0, menu_group, 8)
doors = AnimatedSprite(load_image("snow/menu_doors.png", color_key=-1), 2, 1, SCREEN_WIDTH - tile_size * 1.3, 0,
                       menu_group,
                       35)

level_completed = False

cur_level = 0
level_map = load_level(levels[cur_level])
player, level_x, level_y = generate_level(level_map)
camera = Camera((level_x, level_y))


def move(hero, direction):
    """Функция движения героя"""
    x, y = hero.pos
    green_move = [".", '2', '5', '*', '0', '%']
    if direction == "up":
        if y > 0 and level_map[y - 1][x] in green_move:
            hero.move(direction, x, y - 1)
        elif y == 0 and level_map[y - 1][x] in green_move:
            hero.move(direction, x, level_y)
    elif direction == "down":
        if y < level_y and level_map[y + 1][x] in green_move:
            hero.move(direction, x, y + 1)
        elif y == level_y and level_map[0][x] in green_move:
            hero.move(direction, x, 0)
    elif direction == "left":
        if x > 0 and level_map[y][x - 1] in green_move:
            hero.move(direction, x - 1, y)
        elif x == 0 and level_map[y][level_x] in green_move:
            hero.move(direction, level_x, y)
    elif direction == "right":
        if x < level_x and level_map[y][x + 1] in green_move:
            hero.move(direction, x + 1, y)
        elif x == level_x and level_map[y][0] in green_move:
            hero.move(direction, 0, y)


def game_snowman(dic_game):
    """Функция самой игры"""
    global score_time, score_buckets, score_coins, level_completed, cur_level
    pygame.display.set_caption('Snow_Snow')
    pygame.display.set_icon(load_image("icon.ico"))  # Иконка приложения
    while dic_game['snow_game']:
        score_time += 1
        if level_completed:
            cur_level += 1
            open_level(cur_level)
            new_level_sound.play()
            level_completed = False
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w] or \
                    keys[pygame.K_DOWN] or keys[pygame.K_s] or \
                    keys[pygame.K_LEFT] or keys[pygame.K_a] or \
                    keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    move(player, 'up')
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    move(player, 'down')
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    move(player, 'left')
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    move(player, 'right')
            if event.type == pygame.QUIT:
                dic_game['game'] = False
                dic_game['snow_game'] = False

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        """Рисуем группы спрайтов"""
        screen.blit(fffon, (0, 0))
        tiles_group.draw(screen)
        fire_group.draw(screen)
        coins_group.draw(screen)
        finish_group.draw(screen)
        exit_group.draw(screen)
        player_group.draw(screen)
        bucket_group.draw(screen)
        stones_group.draw(screen)

        """Отрисовка меню"""
        pygame.draw.rect(screen, (181, 146, 146), (0, 0, SCREEN_WIDTH, tile_size // 2))
        draw_mini_text(f'X {score_coins}', white, (tile_size - 10, 12))
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_mini_text(f'  {time}', white, (tile_size * 2, 12))
        draw_mini_text(f'X {score_buckets}', white, (tile_size * 3.75, 12))
        text = n_lvl[levels[cur_level]]
        draw_mini_text(f'LEVEL {cur_level + 1}: {text}', white, (tile_size * 7, 12))
        draw_mini_text(f'X {cur_level}', white, (SCREEN_WIDTH - tile_size // 2, 12))
        menu_group.draw(screen)
        menu_group.update()
        """проверка на столкновения"""
        if pygame.sprite.groupcollide(player_group, coins_group, False, True):
            coin_sound.play()
            score_coins += 1
        if pygame.sprite.groupcollide(player_group, bucket_group, False, True):
            buckets_sound.play()
            score_buckets += 1
        if pygame.sprite.groupcollide(player_group, exit_group, False, False):
            level_completed = True
        if pygame.sprite.groupcollide(player_group, finish_group, False, False):
            dic_game['snow_game'] = False
            dic_game['snow_res'] = True
        if pygame.sprite.groupcollide(player_group, fire_group, False, True):
            if score_buckets < 1:
                game_over_sound.play()
                player.died = True
            else:
                stop_fire_sound.play()
                score_buckets -= 1
        """Если игрок умер, завершаем игру"""
        if player.died:
            dic_game['snow_game'] = False
            dic_game['snow_res'] = True
        pygame.display.flip()
        clock.tick(fps)
    return dic_game


if __name__ == '__main__':
    """Если запустить файл отдельно, то будет работать только эта игра
            (меню, игра, результат, окно с авторами)"""
    dic_game = {'houses': False, 'authors': False, 'table': False, 'game': True,
                'mario_game': False, 'mario_menu': False, 'mario_res': False,
                'snow_game': False, 'snow_menu': True, 'snow_res': False,
                'forrest_game': False, 'forrest_menu': False, 'forrest_res': False}
    while dic_game['game']:
        if dic_game['houses']:
            dic_game['snow_menu'] = True
            dic_game['houses'] = False
        if dic_game['snow_menu']:
            dic_game = menu_snowman_game(dic_game)
        if dic_game['snow_game']:
            dic_game = game_snowman(dic_game)
        if dic_game['snow_res']:
            dic_game = res_of_play_snow(dic_game)
        if dic_game['authors']:
            dic_game = final_game_screen(dic_game)
        if not dic_game['game']:
            break
