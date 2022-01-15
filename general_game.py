from Game_Mary import draw_text
from final_screen import final_game_screen
from main_functions import *

pygame.init()
screen_size = (645, 400)
WIDTH, HEIGHT = 645, 400
screen = pygame.display.set_mode(screen_size)
FPS = 80
onGround = False
tile_images = {
    'wall': pygame.transform.scale(load_image('mario/box2.png'), (50, 50)),
    'empty': load_image('mario/grass.png'),
    'exit': load_image('mario/new_level.png', color_key=-1),
    'princess': load_image('mario/princess_l.png', color_key=-1),
    'menu': load_image('mario/menu.png'),
    'menu_coins': load_image("mario/menu_coins.png", color_key=-1),
    'menu_clocks': load_image("mario/menu_clocks.png", color_key=-1),
    'menu_door': load_image("mario/block.png", color_key=-1)

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
levels = ['mario/level_1.txt', 'mario/level_2.txt', 'mario/level_3.txt',
          'mario/level_4.txt', 'mario/level_5.txt', 'mario/level_6.txt']
f_lvl = [load_image('mario/start_mario.jpg'), load_image('mario/second_peyzaj.jpg'),
         load_image('mario/third_peizaj.jpg'), load_image('mario/far_castle.jpeg'),
         load_image('mario/black_forrest.jpg'), load_image('mario/last_fon.jpg')]  # словарь фонов для уровней
n_lvl = ['Начало', 'Так держать', 'Продолжай!',
         'Бонусный уровень', 'Black forrest', 'Спаси принцессу!']  # Названия для уровней
max_level = len(levels)


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
                Wall(x, y)
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


def menu_mario_game():
    pygame.mouse.set_visible(True)
    running = True
    start_btn = Button(screen_width // 2 - start_img.get_width() // 2,
                       screen_height // 2 - start_img.get_height() // 2, start_img)
    go_back = Button(10, 10, back_img)
    while running:
        screen.blit(bg, (0, 0))
        start_btn.update()
        go_back.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if start_btn.clicked:
            game_mario()
        if go_back.clicked:
            return True

        pygame.display.flip()


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images['wall']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.add(wall_group)


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
        self.died = False

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
        super().__init__(princess_group)
        self.image = tile_images['princess']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)


def res_of_play():
    pygame.mouse.set_visible(False)
    if not hero.died:
        # for i in range(-300, 310, 50):
        #    create_particles((WIDTH // 2 + i, 0))
        # coins = AnimatedSprite(load_image("mario/coins.png", color_key=-1), 3, 2, 155, 212, res_group, 5)
        # clocks = AnimatedSprite(load_image("mario/clocks.png", color_key=-1), 7, 2, 148, 130, res_group, 5)
        intro_text = ["Вы Выиграли, Принцесса спасена!", "",
                      f'Время: {str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}',
                      '', f"Монеты: {score_coins}"]
        fon = pygame.transform.scale(load_image('final.png'), size)
        screen.blit(fon, (0, 0))
        draw_text(intro_text)
    else:
        intro_text = ['']
        fon = load_image('mario/gameover.png', color_key=-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                final_game_screen()
        screen.blit(fon, (0, 0))
        draw_text(intro_text)
        res_group.draw(screen)
        res_group.update()
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
# анимация панели меню
coins = AnimatedSprite(tile_images['menu_coins'], 3, 2, 5, 0, menu_group, 9)
clocks = AnimatedSprite(tile_images['menu_clocks'], 7, 2, tile_size * 1.9, 0, menu_group, 6)
door = AnimatedSprite(tile_images['menu_door'], 1, 1, tile_size * 11.2, 0, menu_group, 6)


def start_screen():
    pygame.display.set_caption('Марио')  # Название приложения
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


def move(hero, direction):
    x, y = hero.pos
    if direction == "up":
        if y > 0 and level_map[int(y) - 1][int(x)] in [".", '2', 'P', '*']:
            global onGround
            if not onGround:
                print(x, y)
                if y > 0 and level_map[int(y) - 2][int(x)] in [".", '2', 'P', '*']:
                    hero.move(x, y - 2)
                elif y > 0 and level_map[int(y) - 3][int(x)] in [".", '2', 'P', '*'] \
                        and y > 0 and level_map[int(y) - 2][int(x)] in [".", '2', 'P', '*']:
                    hero.move(x, y - 3)
                else:
                    hero.move(x, y - 1)
                onGround = True
    elif direction == "down":
        if y < max_y and level_map[int(y) + 1][int(x)] in [".", '2', 'P', '*']:
            hero.move(x, y + 1)
    elif direction == "left":
        if x > 0 and level_map[int(y)][int(x) - 1] in [".", '2', 'P', '*']:
            # if onGround:
            #     hero.move(x, y - 1)
            hero.move(x - 1, y)
    elif direction == "right":
        if x < max_x and level_map[int(y)][int(x) + 1] in [".", '2', 'P', '*']:
            # if onGround:
            #     hero.move(x, y - 1)
            hero.move(x + 1, y)


def open_level(level):
    global hero, max_x, max_y, level_map

    sprite_group.empty()
    hero_group.empty()
    exit_group.empty()
    princess_group.empty()
    coins_group.empty()
    wall_group.empty()
    level_map = load_level(levels[level - 1])
    hero, max_x, max_y = generate_level(level_map)


level_map = load_level(levels[cur_level])
hero, max_x, max_y = generate_level(level_map)


def game_mario():
    global score_time, level_completed, cur_level, score_coins
    # start_screen()
    running = True
    while running:
        score_time += 1
        if level_completed:
            cur_level += 1
            open_level(cur_level)
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
        x, y = hero.pos
        if y < max_y and level_map[int(y) + 1][x] in [".", '2', 'P', '*']:
            if level_map[int(y) + 1][x] not in ['#']:
                if score_time % 8 == 0:
                    hero.move(x, y + 1)
            # else:
            #     global onGround
            #     onGround = False
            #     print(10)
        else:
            global onGround
            onGround = False
        #         hero.move(x, y + 0.1)
        # if onGround:
        #     # x, y = hero.pos
        #     hero.fall()

        fon = pygame.transform.scale(f_lvl[cur_level - 1], (WIDTH, HEIGHT))  # картинка
        screen.blit(fon, (0, 0))
        sprite_group.draw(screen)
        wall_group.draw(screen)
        hero_group.draw(screen)
        exit_group.draw(screen)
        princess_group.draw(screen)
        coins_group.draw(screen)
        coins_group.update()
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
            score_coins += 1
        if pygame.sprite.groupcollide(hero_group, exit_group, False, False):
            level_completed = True
        if pygame.sprite.groupcollide(hero_group, princess_group, False, False):
            res_of_play()
            running = False
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    game_mario()
