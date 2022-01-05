import os
import pygame
import random
import sys
from main_functions import terminate


def start_screen():
    fps = 50
    intro_text = ["Black Forrest", "",
                  "press anything to start"]

    fon = pygame.transform.scale(load_image('font_start.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("SilafejiraRegular.otf", 60)
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
        print(i)
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


size = WIDTH, HEIGHT = 645, 400
tile_size = 50
score_coins = 0
onGround = False
jump = False
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Black Forrest')
clock = pygame.time.Clock()

tile_images = {
    'block': load_image('block.png'),
    'mushroom': load_image('Mushroom_1_pos.png', colorkey=-1),
    'eye': load_image('Eye_1_pos.png', colorkey=-1),
    'hero': load_image("Hero3_1_pos.png", colorkey=-1)
}

coin_images = [load_image("Coin_1_pos.png", colorkey=-1), load_image("Coin_2_pos.png", colorkey=-1),
               load_image("Coin_3_pos.png", colorkey=-1), load_image("Coin_4_pos.png", colorkey=-1)]

# hero_image = load_image("Hero3_1_pos.png", colorkey=-1)

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
mushroom_group = pygame.sprite.Group()
flying_eye = pygame.sprite.Group()


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
        elif tile_type == 'mushroom':
            self.add(mushroom_group, tiles_group, all_sprites)
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
        print(self.rect.y)
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

        if pygame.sprite.spritecollideany(self, block_group):
            self.kill()


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


def game_forrest():
    start_screen()
    build_level()
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
            print(score_time)

        screen.fill(pygame.Color("black"))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    game_forrest()
