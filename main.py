import random
from Game_Alex import menu_forrest_game
from Game_Mary import main_gameplay_snow
from final_screen import final_game_screen
from general_game import menu_mario_game
from main_functions import *

size = WIDTH, HEIGHT = 645, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyPurble Game Studio')  # Название приложения
pygame.display.set_icon(load_image("icon.ico"))  # Иконка приложения
pygame.mouse.set_visible(True)
FPS = 60
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
houses = pygame.sprite.Group()
star_group = pygame.sprite.Group()

back_img = load_image('snow/back_img.png', color_key=-1)


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


def start_progect_screen():
    """Функция вызова(отображения) стартового экрана"""
    fon = pygame.transform.scale(load_image('start/start.png'), (WIDTH, HEIGHT))  # стартовая картинка
    pressed = False
    while True:
        pygame.display.set_caption('PyPurble Game Studio')  # Название приложения
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
                        menu_mario_game()
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


def res_game_screen():
    running = True
    fon = pygame.transform.scale(load_image('final/bg.png'), (WIDTH, HEIGHT))
    go_back = Button(10, 5, back_img)
    for i in range(-300, 310, 50):
        create_particles((SCREEN_WIDTH // 2 + i, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.K_RETURN and event.key == pygame.K_ESCAPE):
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # create_particles(pygame.mouse.get_pos())
                pass
        screen.blit(fon, (0, 0))
        """draw_text(screen)
        all_sprites.draw(screen)
        all_sprites.update()"""
        star_group.update()
        star_group.draw(screen)
        go_back.update()
        if go_back.clicked:
            running = False
        pygame.display.flip()
        clock.tick(FPS)
    return


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

start_progect_screen()
