from Game_Mary import game_snowman
from final_screen import final_game_screen
from main_functions import *


def start_screen():
    """Функция вызова(отображения) стартового экрана"""
    fon = pygame.transform.scale(load_image('start.png'), (WIDTH, HEIGHT))  # стартовая картинка
    screen.blit(fon, (0, 0))
    houses.update()
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
                    if 'Exit' in lst:
                        terminate()
                    elif 'Mary' in lst:
                        game_snowman()
                    elif 'Other' in lst:
                        pass
                    elif 'Alex' in lst:
                        pass
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                houses.update(pygame.mouse)
        screen.blit(fon, (0, 0))
        houses.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


class House_1(pygame.sprite.Sprite):
    image_small = load_image("house_1_small.png", color_key=-1)
    image_big = load_image("house_1_big.png", color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = House_1.image_small
        self.rect = self.image_small.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            self.image = self.image_big
            self.rect.x = self.pos[0] - 2
            self.rect.y = self.pos[1] - 2
        else:
            self.image = self.image_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def check_push(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            return 'Alex'


class House_2(pygame.sprite.Sprite):
    image_small = load_image("house_2_small.png", color_key=-1)
    image_big = load_image("house_2_big.png", color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = House_1.image_small
        self.rect = self.image_small.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            self.image = self.image_big
            self.rect.x = self.pos[0] - 2
            self.rect.y = self.pos[1] - 2
        else:
            self.image = self.image_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def check_push(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            return 'Other'


class House_3(pygame.sprite.Sprite):
    image_small = load_image("house_3_small.png", color_key=-1)
    image_big = load_image("house_3_big.png", color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = House_1.image_small
        self.rect = self.image_small.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            self.image = self.image_big
            self.rect.x = self.pos[0] - 2
            self.rect.y = self.pos[1] - 2
        else:
            self.image = self.image_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def check_push(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            return 'Mary'


class Exit_1(pygame.sprite.Sprite):
    image_small = load_image("exit_small.png", color_key=-1)
    image_big = load_image("exit_big.png", color_key=-1)

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Exit_1.image_small
        self.rect = self.image_small.get_rect()
        self.pos = [x, y]
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and args[-1] == 1 and self.rect.collidepoint(args[0].get_pos()):
            terminate()
        if args and self.rect.collidepoint(args[0].get_pos()):
            self.image = self.image_big
            self.rect.x = self.pos[0] - 2
            self.rect.y = self.pos[1] - 2
        else:
            self.image = self.image_small
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

    def check_push(self, *args):
        if args and self.rect.collidepoint(args[0].get_pos()):
            return 'Exit'


if __name__ == '__main__':
    size = WIDTH, HEIGHT = 645, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ДОПИСАТЬ НАЗВАНИЕ')  # Название приложения
    pygame.display.set_icon(load_image("icon.ico"))  # Иконка приложения
    pygame.mouse.set_visible(True)
    all_sprites = pygame.sprite.Group()
    houses = pygame.sprite.Group()
    House_1(11, 85, houses)
    House_2(147, 130, houses)
    House_3(425, 132, houses)
    Exit_1(9, 307, houses)

    fps = 60
    clock = pygame.time.Clock()
    start_screen()
    final_game_screen()
