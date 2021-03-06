import random
from final_screen import final_game_screen
from main_functions import *

pygame.init()
WIDTH, HEIGHT = screen_size = (645, 400)
screen = pygame.display.set_mode(screen_size)
FPS = 60
onGround = False

tile_images = {
    'exit': load_image('mario/new_level.png', color_key=-1),
    'menu': load_image('mario/menu.png'),
    'menu_coins': load_image("mario/menu_coins.png", color_key=-1),
    'menu_clocks': load_image("mario/menu_clocks.png", color_key=-1),
    'menu_door': load_image("mario/block.png", color_key=-1),
    'dirt': load_image("mario/dirt.png"),
    'grass': load_image("mario/grass.png", color_key=-1),
    'gru_wall': pygame.transform.scale(load_image("BlackForrest/block.png", color_key=-1), (50, 50)),
    'snow': load_image("mario/snow.png", color_key=-1)
}

player_image = pygame.transform.scale(load_image("mario/0.png", color_key=-1), (30, 50))
start_img = pygame.transform.scale(load_image('mario/start_button.png'), (148, 68))
bg = pygame.transform.scale(load_image('mario/mario (1).jpg'), (WIDTH, HEIGHT))

back_img = load_image('mario/back_img.png', color_key=-1)
exit_img = pygame.transform.scale(load_image("BlackForrest/exit_btn.png", color_key=-1), (117, 49))
restart_img = pygame.transform.scale(load_image("BlackForrest/restart_btn.png", color_key=-1), (117, 49))

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
         'data/mario/music/peace.mp3', 'data/mario/music/desert.mp3',
         'data/mario/music/snow_back.mp3', 'data/mario/music/castle.mp3',
         'data/mario/music/forest.mp3', 'data/mario/music/evil_wizard.mp3',
         'data/mario/music/win.mp3']

f_lvl = [load_image('mario/portal.jpg'), load_image('mario/second_peyzaj.jpg'),
         load_image('mario/third_peizaj.jpg'),
         load_image('mario/desert.jpeg'), load_image('mario/snow_rocks.jpg'),
         load_image('mario/far_castle.jpeg'), load_image('mario/dark_forrest.jpg'),
         load_image('mario/evil_mag.jpg'), load_image('mario/last_fon.jpg')]  # ?????????????? ?????????? ?????? ??????????????

n_lvl = ['???????????? ?? ????????', '?????? ?????????????? ????????????????', '?????????????????? ??????????????',
         '?????????????? ????????????', '???????????? ??????????????????????', '???????????? ?????????? ????????',
         '???????????? ??????', '???????? ??????????????????', '?????????? ??????????????????']  # ???????????????? ?????? ??????????????

left_run = [pygame.transform.scale(load_image("mario/l1.png", color_key=-1), (30, 50)),
            pygame.transform.scale(load_image("mario/l2.png", color_key=-1), (30, 50)),
            pygame.transform.scale(load_image("mario/l3.png", color_key=-1), (30, 50)),
            pygame.transform.scale(load_image("mario/l4.png", color_key=-1), (30, 50)),
            pygame.transform.scale(load_image("mario/l5.png", color_key=-1), (30, 50))]

right_run = [pygame.transform.scale(load_image("mario/r1.png", color_key=-1), (30, 50)),
             pygame.transform.scale(load_image("mario/r2.png", color_key=-1), (30, 50)),
             pygame.transform.scale(load_image("mario/r3.png", color_key=-1), (30, 50)),
             pygame.transform.scale(load_image("mario/r4.png", color_key=-1), (30, 50)),
             pygame.transform.scale(load_image("mario/r5.png", color_key=-1), (30, 50))]

jumping_img = [pygame.transform.scale(load_image("mario/j.png", color_key=-1), (30, 50)),
               pygame.transform.scale(load_image("mario/jl.png", color_key=-1), (30, 50)),
               pygame.transform.scale(load_image("mario/jr.png", color_key=-1), (30, 50))]

skeleton_images = [pygame.transform.scale(load_image("Mario/Skeleton1.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton2.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton3.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton4.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton5.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton6.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton7.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton8.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton9.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton10.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton11.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton12.png", color_key=-1), (50, 50)),
                   pygame.transform.scale(load_image("Mario/Skeleton13.png", color_key=-1), (50, 50))
                   ]

skeleton_images_reverse = [pygame.transform.flip(skeleton_images[0], True, False),
                           pygame.transform.flip(skeleton_images[1], True, False),
                           pygame.transform.flip(skeleton_images[2], True, False),
                           pygame.transform.flip(skeleton_images[3], True, False),
                           pygame.transform.flip(skeleton_images[4], True, False),
                           pygame.transform.flip(skeleton_images[5], True, False),
                           pygame.transform.flip(skeleton_images[6], True, False),
                           pygame.transform.flip(skeleton_images[7], True, False),
                           pygame.transform.flip(skeleton_images[8], True, False),
                           pygame.transform.flip(skeleton_images[9], True, False),
                           pygame.transform.flip(skeleton_images[10], True, False),
                           pygame.transform.flip(skeleton_images[11], True, False),
                           pygame.transform.flip(skeleton_images[12], True, False),
                           ]

max_level = len(levels)
NEW_BEST = '???? ?????????????????? ?? ?????????????? ??????????????!'


def draw_mini_text(text, color, pos):
    """?????????????????? ???????????? ???????????????????? ?????????????? ?????? ???????? (??????????)"""
    font = pygame.font.Font(None, 30)
    x, y = pos
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


def generate_level(level):
    """?????????????? ?????????????????? ????????????
            (???????????????????????? ?????????? ????????????????, ?????????????? ????????????)"""
    new_player, x, y = None, None, None
    enemy_group.empty()
    list_with_walls = list()
    invisible_blocks_list = list()
    list_with_walls.clear()
    invisible_blocks_list.clear()
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
            elif level[y][x] == 'i':
                invisible_blocks = Invisible(x, y)
                tile = (invisible_blocks.image, invisible_blocks.rect)
                invisible_blocks_list.append(tile)
            elif level[y][x] == 'e':
                Enemy(x, y)
            elif level[y][x] == '*':
                AnimatedSprite(load_image("mario/menu_coins.png", color_key=-1), 3, 2,
                               tile_size * x + tile_size // 4, tile_size * y + tile_size // 4, coins_group, 9)
    return new_player, x, y, list_with_walls, invisible_blocks_list


class Particle(Sprite):
    """?????????? ?????? ?????????????? ????????????(??????????????????)"""
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
    """?????????????? ?????? ???????????????? ???????????????? ???????????? ???????????? (??????????????????)"""
    numbers = range(-6, 5)
    for _ in range(20):
        Particle(position, random.choice(numbers), random.choice(numbers))


def menu_mario_game(dic_game):
    """?????????????? ???????? ???????? ??????????"""
    pygame.display.set_caption('Mario: Multiverse')  # ???????????????? ????????????????????
    pygame.mixer.music.load("data/mario/music/honor-and-sword-main.mp3")
    pygame.mixer.music.play()
    sound_btn = pygame.mixer.Sound("data/BlackForrest/button (2).mp3")
    pygame.mouse.set_visible(True)
    start_btn = Button(SCREEN_WIDTH // 2 - start_img.get_width() // 2,
                       SCREEN_HEIGHT // 2 - start_img.get_height() // 2, start_img)
    go_back = Button(10, 10, back_img)
    while dic_game['mario_menu']:
        screen.blit(bg, (0, 0))
        start_btn.update()
        go_back.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dic_game['game'] = False
                dic_game['mario_menu'] = False

        if start_btn.clicked:
            sound_btn.play()
            pygame.mixer.music.stop()
            dic_game['mario_game'] = True
            dic_game['mario_menu'] = False
        if go_back.clicked:
            pygame.mixer.music.stop()
            sound_btn.play()
            dic_game['houses'] = True
            dic_game['mario_menu'] = False
        clock.tick(FPS)
        pygame.display.flip()
    return dic_game


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Invisible(Sprite):
    """?????????? ?????????????????? ????????????(?????? ???????????????? ???????????????? ???? ????????????)"""

    def __init__(self, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = pygame.transform.scale(load_image("mario/invisible_block.png", color_key=-1), (50, 50))
        # self.image = pygame.transform.scale(load_image("mario/invisible_block.png"), (50, 50))
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


class Enemy(Sprite):
    """?????????? ????????????(????????????????)"""

    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group)
        self.image = skeleton_images[0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.counter = 0
        self.motion = "right"

    def update(self):

        move_x = 0
        moving = 1

        if self.motion == "left":
            move_x -= moving
        if self.motion == "right":
            move_x += moving

        if self.counter % 8 == 0 and self.motion == "right":
            self.image = skeleton_images[(self.counter // 8) % 13]
        if self.counter % 8 == 0 and self.motion == "left":
            self.image = skeleton_images_reverse[(self.counter // 8) % 13]
        self.counter += 1

        for tile in invisible_lst:
            if tile[1].colliderect(self.rect.x + move_x, self.rect.y, self.width, self.height) or \
                    self.rect.x + move_x > WIDTH - 50 or self.rect.x + move_x < 0:
                if self.motion == "left":
                    self.motion = "right"
                    move_x += 2 * moving
                elif self.motion == "right":
                    self.motion = "left"
                    move_x -= 2 * moving

        for tile in lst:
            if tile[1].colliderect(self.rect.x + move_x, self.rect.y, self.width, self.height) or \
                    self.rect.x + move_x > WIDTH - 50 or self.rect.x + move_x < 0:
                if self.motion == "left":
                    self.motion = "right"
                    move_x += 2 * moving
                elif self.motion == "right":
                    self.motion = "left"
                    move_x -= 2 * moving

        self.rect.x += move_x

        screen.blit(self.image, self.rect)


class Player(Sprite):
    """?????????? ???????????? ??????????"""

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
        """?????????? ???????????????? ????????????"""
        global onGround, level_completed

        move_x = 0
        move_y = 0
        moving = 4

        if not hero.died:
            key = pygame.key.get_pressed()
            if (key[pygame.K_UP] or key[pygame.K_w]) and not self.jumped and not self.notOnGround:
                if self.image in left_run:
                    self.image = jumping_img[1]
                elif self.image in right_run:
                    self.image = jumping_img[2]
                else:
                    self.image = jumping_img[0]

                self.gravity = -17
                self.jumped = True
            if not (key[pygame.K_UP] or key[pygame.K_w]):
                self.jumped = False
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                move_x -= moving
                if self.counter % 8 == 0:
                    self.image = left_run[(self.counter // 8) % 5]
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                move_x += moving
                if self.counter % 8 == 0:
                    self.image = right_run[(self.counter // 8) % 5]
                self.counter += 1
                self.direction = 1
            if not (key[pygame.K_LEFT] or key[pygame.K_a]) and not (key[pygame.K_RIGHT] or key[pygame.K_d]):
                self.image = player_image
                self.counter = 0
                self.index = 0
            if self.image in left_run and self.notOnGround:
                self.image = jumping_img[1]
            elif self.image in right_run and self.notOnGround:
                self.image = jumping_img[2]
            elif self.image == player_image and self.notOnGround:
                self.image = jumping_img[0]
            if pygame.sprite.spritecollideany(self, enemy_group):
                self.rect = self.image.get_rect().move(self.start)
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
    """?????????? ???????????????? ???? ?????????? ?????????????? (????????)"""

    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group)
        self.image = tile_images['exit']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)


class Princess(Sprite):
    """?????????? ?????????????????? (???????? ????????)"""
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


def res_of_play_mario(dic_game):
    """?????????????? ?????????????????????? ?????????????????????? ???????? ??????????"""
    global score_time, score_coins, lst, cur_level, level_completed
    pygame.mouse.set_visible(True)
    res_group.empty()
    star_group.empty()
    if not hero.died:
        for i in range(-300, 310, 50):
            create_particles((WIDTH // 2 + i, 0))
        _ = AnimatedSprite(load_image("snow/coins.png", color_key=-1), 3, 2, 155, 212, res_group, 5)
        _ = AnimatedSprite(load_image("snow/clocks.png", color_key=-1), 7, 2, 148, 130, res_group, 5)
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        intro_text = ["???? ????????????????. ?????????????????? ??????????????!", "", f'??????????: {time}',
                      '', f"????????????: {score_coins}",
                      f"{NEW_BEST if check_new_table('mario', int(score_coins), time) else ''}"]
        fon = pygame.transform.scale(load_image('mario/final_mario.png'), screen_size)
        screen.blit(fon, (0, 0))
        draw_text(intro_text)
    else:
        intro_text = ['']
        fon = load_image('mario/gameover.png', color_key=-1)
    exit_btn = Button(500, 350, exit_img)
    restart_btn = Button(35, 350, restart_img)

    while dic_game['mario_res']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dic_game['game'] = False
                dic_game['mario_res'] = False
        screen.blit(fon, (0, 0))
        draw_text(intro_text, color=pygame.Color('black'))
        res_group.draw(screen)
        res_group.update()
        star_group.update()
        star_group.draw(screen)
        exit_btn.update()
        restart_btn.update()
        if restart_btn.clicked:
            cur_level = 0
            score_coins = 0
            score_time = 0
            lst.clear()
            level_completed = True
            dic_game['mario_res'] = False
            dic_game['mario_game'] = True
        if exit_btn.clicked:
            cur_level = 0
            score_coins = 0
            score_time = 0
            lst.clear()
            level_completed = True
            dic_game['mario_res'] = False
            dic_game['authors'] = True
        pygame.display.flip()
        clock.tick(FPS)
    return dic_game


clock = pygame.time.Clock()
# ???????????? ????????????????
sprite_group = SpriteGroup()
wall_group = SpriteGroup()
hero_group = SpriteGroup()
exit_group = SpriteGroup()
enemy_group = SpriteGroup()
princess_group = SpriteGroup()
menu_group = SpriteGroup()
coins_group = SpriteGroup()
res_group = SpriteGroup()
star_group = pygame.sprite.Group()
# ???????????????? ???????????? ????????
coins = AnimatedSprite(tile_images['menu_coins'], 3, 2, 5, 0, menu_group, 9)
clocks = AnimatedSprite(tile_images['menu_clocks'], 7, 2, tile_size * 1.9, 0, menu_group, 6)
door = AnimatedSprite(tile_images['menu_door'], 1, 1, tile_size * 11.5, 0, menu_group, 6)


def open_level(level):
    """?????????????? ???????????????? ????????????
        (?????????????????? ?????????? ????????????????, ?????????????????? ????????????, ???????????????? ????????????)"""
    global hero, max_x, max_y, level_map, lst, invisible_lst

    sprite_group.empty()
    hero_group.empty()
    exit_group.empty()
    princess_group.empty()
    coins_group.empty()
    wall_group.empty()
    res_group.empty()
    pygame.mixer.music.load(music[level - 1])
    pygame.mixer.music.play()
    level_map = load_level(levels[level - 1])
    hero, max_x, max_y, lst, invisible_lst = generate_level(level_map)


level_map = load_level(levels[cur_level])
hero, max_x, max_y, lst, invisible_lst = generate_level(level_map)


def game_mario(dic_game):
    """?????????????? ???????? ??????????"""
    global score_time, level_completed, cur_level, score_coins, lst
    while dic_game['mario_game']:
        score_time += 1
        if level_completed:
            pygame.mixer.music.stop()
            cur_level += 1
            open_level(cur_level)
            level_completed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dic_game['mario_game'] = False
                dic_game['game'] = False
        else:
            global onGround
            onGround = False

        fon = pygame.transform.scale(f_lvl[cur_level - 1], (WIDTH, HEIGHT))  # ????????????????
        screen.blit(fon, (0, 0))
        sprite_group.draw(screen)
        wall_group.draw(screen)
        enemy_group.draw(screen)
        hero_group.draw(screen)
        exit_group.draw(screen)
        princess_group.draw(screen)
        coins_group.draw(screen)
        coins_group.update()
        hero.update()
        princess_group.update()
        enemy_group.update()
        clock.tick(FPS)
        # ????????:
        draw_mini_text(f'X {score_coins}', (255, 255, 255), (tile_size + 5, 15))  # ??????????????
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
            dic_game['mario_game'] = False
            dic_game['mario_res'] = True
        pygame.display.flip()
    return dic_game


if __name__ == '__main__':
    """???????? ?????????????????? ???????? ????????????????, ???? ?????????? ???????????????? ???????????? ?????? ????????
            (????????, ????????, ??????????????????, ???????? ?? ????????????????)"""
    dic_game = {'houses': False, 'authors': False, 'table': False, 'game': True,
                'mario_game': False, 'mario_menu': True, 'mario_res': False,
                'snow_game': False, 'snow_menu': False, 'snow_res': False,
                'forrest_game': False, 'forrest_menu': False, 'forrest_res': False}
    while dic_game['game']:
        if dic_game['houses']:
            dic_game['mario_menu'] = True
            dic_game['houses'] = False
        if dic_game['mario_menu']:
            dic_game = menu_mario_game(dic_game)
        if dic_game['mario_game']:
            dic_game = game_mario(dic_game)
        if dic_game['mario_res']:
            dic_game = res_of_play_mario(dic_game)
        if dic_game['authors']:
            dic_game = final_game_screen(dic_game)
        if not dic_game['game']:
            break
