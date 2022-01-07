from Game_Alex import game_forrest
from Game_Mary import game_snowman
from general_game import game_mario
from main_functions import *

size = WIDTH, HEIGHT = 645, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ДОПИСАТЬ НАЗВАНИЕ')  # Название приложения
pygame.display.set_icon(load_image("icon.ico"))  # Иконка приложения
pygame.mouse.set_visible(True)
all_sprites = pygame.sprite.Group()
houses = pygame.sprite.Group()
fps = 60
clock = pygame.time.Clock()


def start_progect_screen():
    """Функция вызова(отображения) стартового экрана"""
    fon = pygame.transform.scale(load_image('start/start.png'), (WIDTH, HEIGHT))  # стартовая картинка
    pressed = False
    while True:
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
                        game_snowman()
                    elif 'house_2' in lst:
                        game_mario()
                    elif 'house_1' in lst:
                        game_forrest()
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                houses.update(pygame.mouse)
        screen.blit(fon, (0, 0))
        houses.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


class Houses(pygame.sprite.Sprite):
    house_1_small = load_image("start/house_1_small.png", color_key=-1)
    house_1_big = load_image("start/house_1_big.png", color_key=-1)
    house_2_small = load_image("start/house_2_small.png", color_key=-1)
    house_2_big = load_image("start/house_2_big.png", color_key=-1)
    house_3_small = load_image("start/house_3_small.png", color_key=-1)
    house_3_big = load_image("start/house_3_big.png", color_key=-1)
    exit_small = load_image("start/exit_small.png", color_key=-1)
    exit_big = load_image("start/exit_big.png", color_key=-1)

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
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def check_push(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            return self.name


Houses(11, 85, houses, 'house_1')
Houses(147, 130, houses, 'house_2')
Houses(425, 132, houses, 'house_3')
Houses(9, 307, houses, 'exit')
