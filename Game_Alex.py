import random
import os
import sys
import pygame


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fps = 50
    intro_text = ["Black Forrest", "",
                  "press anything to start"]

    fon = pygame.transform.scale(load_image('font_start.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("data/BlackForrest/SilafejiraRegular.otf", 60)
    text_coord = 60
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(0, 85, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        if line == "Black Forrest":
            intro_rect.x = (WIDTH - 253) // 2
        elif line == "press anything to start":
            intro_rect.x = (WIDTH - 369) // 2
        else:
            intro_rect.x = 225
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def build_level():
    for i in range(13):
        Tile("block", i, 7)
    Mushroom()


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

    font = pygame.font.Font("data/BlackForrest/SilafejiraRegular.otf", 20)
    x, y = pos
    text = font.render(text, True, color)
    screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))


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
XP = 5
onGround = False
jump = False
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Black Forrest')
clock = pygame.time.Clock()

tile_images = {
    'block': load_image('block.png'),
    'eye': load_image('Eye_1_pos.png', colorkey=-1),
    'hero': load_image("Hero3_1_pos.png", colorkey=-1)
}

coin_images = [load_image("Coin_1_pos.png", colorkey=-1), load_image("Coin_2_pos.png", colorkey=-1),
               load_image("Coin_3_pos.png", colorkey=-1), load_image("Coin_4_pos.png", colorkey=-1)]

mushroom_images = [load_image("Mushroom_1_pos.png", colorkey=-1), load_image("Mushroom_2_pos.png", colorkey=-1),
                   load_image("Mushroom_3_pos.png", colorkey=-1), load_image("Mushroom_4_pos.png", colorkey=-1),
                   load_image("Mushroom_5_pos.png", colorkey=-1), load_image("Mushroom_6_pos.png", colorkey=-1),
                   load_image("Mushroom_7_pos.png", colorkey=-1), load_image("Mushroom_8_pos.png", colorkey=-1)]

mushroom_reverse_images = [load_image("m_Mushroom_1_pos.png", colorkey=-1), load_image("m_Mushroom_2_pos.png", colorkey=-1),
                           load_image("m_Mushroom_3_pos.png", colorkey=-1), load_image("m_Mushroom_4_pos.png", colorkey=-1),
                           load_image("m_Mushroom_5_pos.png", colorkey=-1), load_image("m_Mushroom_6_pos.png", colorkey=-1),
                           load_image("m_Mushroom_7_pos.png", colorkey=-1), load_image("m_Mushroom_8_pos.png", colorkey=-1)]

# hero_image = load_image("Hero3_1_pos.png", colorkey=-1)

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
coins = AnimatedSprite(load_image("Coin-Sheet.png", colorkey=-1), 4, 1, 5, 0, menu_group, 9)
clocks = AnimatedSprite(load_image("clocks.png", colorkey=-1), 7, 2, tile_size + 12, 0, menu_group, 6)


# exit_group = pygame.sprite.Group()
# finish_group = pygame.sprite.Group()
# star_group = pygame.sprite.Group()
# res_group = pygame.sprite.Group()


class BlackForrest(pygame.sprite.Sprite):
    image = load_image("my_font.png", colorkey=None)
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = BlackForrest.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        # self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        # self.rect.bottom = HEIGHT


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
    # def __init__(self, pos_x, pos_y, onGround):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = tile_images['hero']
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.died = False
        # self.onGround = onGround
        self.add(player_group, all_sprites)

    def move_up(self):
        # self.rect = self.rect.move(0, -100)
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
            XP = 0


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
        # self.rect = self.rect.move(tile_size * pos_x, tile_size * pos_y)
        self.add(coins_group, all_sprites)

    def update(self, *args):
        self.rect = self.rect.move(0, +1)
        if self.rect.y % 8 == 0:
            self.counter += 1
            self.image = pygame.transform.scale(coin_images[self.counter % 4], (16, 16))

        if pygame.sprite.spritecollideany(self, player_group):
            global score_coins
            score_coins += 1
            self.kill()

        if pygame.sprite.spritecollideany(self, mushroom_group):
            self.kill()

        if pygame.sprite.spritecollideany(self, block_group):
            global XP
            XP -= 1
            self.kill()


class Mushroom(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = mushroom_images[0]
        # self.image = AnimatedSprite("Mushroom_sheet.png", 8, 1, self.rect.x, HEIGHT - 100, mushroom_group, 10)
        self.rect = self.image.get_rect()
        self.rect.x = 1
        self.rect.y = HEIGHT - 85
        self.counter = 0
        self.add(mushroom_group, all_sprites)

    def update(self, *args):
        # self.rect = self.rect.move(+1, 0)
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
# player = Player(6, 6, False)
player = Player(6, 6)

Border(-1, -1, WIDTH + 1, -1)  # Верхняя граница
Border(-1, HEIGHT + 1, WIDTH + 1, HEIGHT + 1)  # Нижняя граница
Border(-10, -1, -10, HEIGHT + 1)
Border(WIDTH + 10, -1, WIDTH + 10, HEIGHT + 1)

pygame.init()
start_screen()
build_level()


def main():
    fps = 85
    score_time = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        score_time += 1
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and onGround == False:
                player.move_up()
                if pygame.sprite.spritecollideany(player, horizontal_borders):
                    player.move_down()
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            #     player.move_down()
            #     if pygame.sprite.spritecollideany(player, horizontal_borders):
            #         player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
                if pygame.sprite.spritecollideany(player, vertical_borders):
                    player.move_right()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()
                if pygame.sprite.spritecollideany(player, vertical_borders):
                    player.move_left()
        if jump:  # Если герой не достиг конечной точки прыжка
            player.move_up()
        if onGround:  # Если герой не земле
            player.fall()

        if score_time % 100 == 0:  # Можно использовать как уровень сложности, типо число поменять на 50, если уровень
            #  действительно сложный!
            Coins()
            # print(score_time)

        screen.fill(pygame.Color("black"))
        all_sprites.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, tile_size // 2))
        draw_mini_text(f'x {score_coins}', (184, 15, 10), (tile_size, 12))
        time = f'{str(score_time // 3600).rjust(2, "0")}:{str(score_time % 3600 // 60).rjust(2, "0")}'
        draw_mini_text(f'  {time}', (184, 15, 10), (tile_size * 3, 12))
        draw_mini_text(f'x  {XP}', (184, 15, 10), (tile_size * 5, 12))
        menu_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
