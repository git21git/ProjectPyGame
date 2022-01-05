import random

from final_screen import final_game_screen
from main_functions import *

pygame.init()
size = screen_width, screen_height = (645, 400)
tile_size = 50
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

levels = ['snow/level_1.txt', 'snow/level_2.txt', 'snow/level_3.txt',
          'snow/level_4.txt', 'snow/level_5.txt']
random.shuffle(levels)
levels.append('snow/level_6.txt')
max_level = min(len(levels) + 1, 5)


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
                exit = Exit(x, y)
            elif level[y][x] == '5':  # final_level_exit
                Tile('empty', x, y)
                finish = Finish(x, y)
            elif level[y][x] == '0':  # ведро с водой
                Tile('empty', x, y)
                bucket = Bucket(x, y)
    return new_player, x, y


def open_level(cur_level):
    global camera, player, level_x, level_y

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

    player, level_x, level_y = generate_level(load_level(levels[cur_level]))
    camera = Camera((level_x, level_y))


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

    def move_up(self, num=1):
        for i in range(num):
            self.rect = self.rect.move(0, -50)
        self.image = player_image_up

    def move_down(self, num=1):
        for i in range(num):
            self.rect = self.rect.move(0, +50)
        self.image = player_image_down

    def move_left(self, num=1):
        for i in range(num):
            self.rect = self.rect.move(-50, 0)
        self.image = player_image_left

    def move_right(self, num=1):
        for i in range(num):
            self.rect = self.rect.move(+50, 0)
        self.image = player_image


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = tile_images['fire']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)

        self.add(fire_group, all_sprites)


class Bucket(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = tile_images['bucket']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)

        self.add(bucket_group, all_sprites)


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


def draw_mini_text(text, color, pos):
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
        coins = AnimatedSprite(load_image("snow/coins.png", color_key=-1), 3, 2, 155, 212, res_group, 5)
        clocks = AnimatedSprite(load_image("snow/clocks.png", color_key=-1), 7, 2, 148, 130, res_group, 5)
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
doors = AnimatedSprite(load_image("snow/menu_doors.png", color_key=-1), 2, 1, WIDTH - tile_size * 1.3, 0, menu_group, 35)

level_completed = False

cur_level = 0
player, level_x, level_y = generate_level(load_level(levels[cur_level]))
camera = Camera((level_x, level_y))


def game_snowman():
    global score_time, score_buckets, score_coins, level_completed, cur_level
    running = True
    pygame.display.set_caption('Снеговик')
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_down(num=2)
                    player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_up(num=2)
                    player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_right(num=2)
                    player.move_left()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()
                if pygame.sprite.spritecollideany(player, box_group):
                    player.move_left(num=2)
                    player.move_right()

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
        draw_mini_text(f'X {score_coins}', (255, 255, 255), (tile_size - 10, 12))
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_mini_text(f'  {time}', (255, 255, 255), (tile_size * 2, 12))
        draw_mini_text(f'X {score_buckets}', (255, 255, 255), (tile_size * 3.75, 12))
        draw_mini_text(f'X {cur_level}', (255, 255, 255), (WIDTH - tile_size // 2, 12))
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
