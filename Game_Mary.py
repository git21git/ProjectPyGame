import random

from final_screen import final_game_screen
from main_functions import *

pygame.init()
size = screen_width, screen_height = (645, 400)
tile_size = 50
screen_size = (645, 400)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
WIDTH, HEIGHT = 645, 400
screen_rect = (0, 0, WIDTH, HEIGHT)
# Состояние игры
score_time = 0
score_coins = 0
score_buckets = 0

tile_images = {
    'box': load_image('snow/box.png'),
    'empty': load_image('snow/ice.png'),
    'fire': load_image('snow/fire.png', color_key=-1),
    'exit': load_image('snow/new_level.png', color_key=-1),
    'flag': load_image('snow/flag.png', color_key=-1),
    'coin': load_image('snow/coin.png', color_key=-1),
    'bucket': load_image('snow/bucket.png', color_key=-1),
}
player_image = load_image('snow/snowman.png', color_key=-1)
player_image_up = load_image('snow/snowman_up.png', color_key=-1)
player_image_down = load_image('snow/snowman_down.png', color_key=-1)
player_image_left = load_image('snow/snowman_left.png', color_key=-1)

start_img = load_image('snow/btn_start.png')
bg = load_image('snow/bg.png')
back_img = load_image('snow/back_img.png', color_key=-1)
# menu_img = load_image('snow/menu_img.png')

levels = ['snow/level_1.txt', 'snow/level_2.txt', 'snow/level_3.txt',
          'snow/level_4.txt', 'snow/level_5.txt']
random.shuffle(levels)
levels.append('snow/level_6.txt')
n_lvl = {'snow/level_1.txt': 'Начало', 'snow/level_2.txt': 'Так держать',
         'snow/level_4.txt': 'Продолжай!', 'snow/level_3.txt': 'Бонусный уровень',
         'snow/level_5.txt': 'Black forrest!', 'snow/level_6.txt': 'Финал!'}  # Названия для уровней
max_level = len(levels)
white = (255, 255, 255)

motion = 'STOP'  # по умолчанию — стоим, флаг для непрерывного движения


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
                _ = Fire(x, y)
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

    level_map = load_level(levels[level])
    player, level_x, level_y = generate_level(level_map)
    camera = Camera((level_x, level_y))


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
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)

        if tile_type == 'box':
            self.add(box_group, tiles_group, all_sprites)
        else:
            self.add(tiles_group, all_sprites)


class Player(Sprite):
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
    def __init__(self, pos_x, pos_y):
        super().__init__(fire_group)
        self.image = tile_images['fire']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)

        self.add(fire_group, all_sprites)


class Bucket(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bucket_group)
        self.image = tile_images['bucket']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)

        self.add(bucket_group, all_sprites)


#
class Finish(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(finish_group)
        self.image = tile_images['flag']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(finish_group, all_sprites)


#
class Exit(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group)
        self.image = tile_images['exit']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(exit_group, all_sprites)


# монетки
class Coins(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coins_group)
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


def draw_mini_text(text, color, pos):
    """Рисование текста маленького размера для меню (снеговик)"""
    font = pygame.font.Font(None, 20)
    x, y = pos
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


def draw_text(intro_text):
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        text = font.render(line, True, pygame.Color('white'))
        text_x = screen_width // 2 - text.get_width() // 2
        text_y = text_coord + text.get_height()
        text_coord = text_y + 10
        screen.blit(text, (text_x, text_y))


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


start_btn = Button(screen_width // 2 - start_img.get_width() // 2,
                   screen_height // 2 - start_img.get_height() // 2, start_img)


def intro_game():
    pygame.mouse.set_visible(True)
    running = True
    go_back = Button(10, 10, back_img)
    # menu = Button(screen_width // 2 - menu_img.get_width() // 2,
    #              screen_height // 2 - menu_img.get_height() // 2, menu_img)
    while running:
        fon = pygame.transform.scale(bg, screen_size)
        screen.blit(fon, (0, 0))
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
            pass

        pygame.display.flip()


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


def res_of_play():
    pygame.mouse.set_visible(False)
    if not player.died:
        for i in range(-300, 310, 50):
            create_particles((WIDTH // 2 + i, 0))
        _ = AnimatedSprite(load_image("snow/coins.png", color_key=-1), 3, 2, 155, 212, res_group, 5)
        _ = AnimatedSprite(load_image("snow/clocks.png", color_key=-1), 7, 2, 148, 130, res_group, 5)
        intro_text = ["Вы Выиграли!", "",
                      f'Время: {str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}',
                      '', f"Монеты: {score_coins}"]
        fon = pygame.transform.scale(load_image('final.png'), size)
        screen.blit(fon, (0, 0))
        draw_text(intro_text)
    else:
        intro_text = ['']
        fon = load_image('snow/gameover.png', color_key=-1)

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
bucket_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()
# меню
coins = AnimatedSprite(load_image("snow/menu_coins.png", color_key=-1), 3, 2, 5, 0, menu_group, 9)
clocks = AnimatedSprite(load_image("snow/menu_clocks.png", color_key=-1), 7, 2, tile_size + 12, 0, menu_group, 6)
waters = AnimatedSprite(load_image("snow/menu_water.png", color_key=-1), 3, 2, tile_size * 2.9, 0, menu_group, 8)
doors = AnimatedSprite(load_image("snow/menu_doors.png", color_key=-1), 2, 1, WIDTH - tile_size * 1.3, 0, menu_group,
                       35)

level_completed = False

cur_level = 0
level_map = load_level(levels[cur_level])
player, level_x, level_y = generate_level(level_map)
camera = Camera((level_x, level_y))


def move(hero, direction):
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


def game_snowman():
    global score_time, score_buckets, score_coins, level_completed, cur_level, motion
    running = intro_game()
    pygame.display.set_caption('Снеговик')
    while running:
        score_time += 1
        if level_completed:
            cur_level += 1
            open_level(cur_level)
            level_completed = False
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_DOWN] or \
                    keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                if keys[pygame.K_UP]:
                    motion = 'up'
                elif keys[pygame.K_DOWN]:
                    motion = 'down'
                elif keys[pygame.K_LEFT]:
                    motion = 'left'
                elif keys[pygame.K_RIGHT]:
                    motion = 'right'
                move(player, motion)
            if event.type == pygame.QUIT:
                terminate()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill(pygame.Color(255, 100, 100))
        tiles_group.draw(screen)
        fire_group.draw(screen)
        coins_group.draw(screen)
        finish_group.draw(screen)
        exit_group.draw(screen)
        player_group.draw(screen)
        bucket_group.draw(screen)

        # Меню:
        pygame.draw.rect(screen, (181, 146, 146), (0, 0, WIDTH, tile_size // 2))
        draw_mini_text(f'X {score_coins}', white, (tile_size - 10, 12))
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_mini_text(f'  {time}', white, (tile_size * 2, 12))
        draw_mini_text(f'X {score_buckets}', white, (tile_size * 3.75, 12))
        text = n_lvl[levels[cur_level]]
        draw_mini_text(f'LEVEL {cur_level + 1}: {text}', white, (tile_size * 7, 12))
        draw_mini_text(f'X {cur_level}', white, (WIDTH - tile_size // 2, 12))
        menu_group.draw(screen)
        menu_group.update()

        if pygame.sprite.groupcollide(player_group, coins_group, False, True):
            score_coins += 1
        if pygame.sprite.groupcollide(player_group, bucket_group, False, True):
            score_buckets += 1
        if pygame.sprite.groupcollide(player_group, exit_group, False, False):
            level_completed = True
        if pygame.sprite.groupcollide(player_group, finish_group, False, False):
            res_of_play()
            running = False
        if pygame.sprite.groupcollide(player_group, fire_group, False, True):
            if score_buckets < 1:
                player.died = True
                running = False
            else:
                score_buckets -= 1

        if player.died:
            res_of_play()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    game_snowman()
