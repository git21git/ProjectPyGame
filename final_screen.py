import csv

from main_functions import *

pygame.init()
FPS = 60
gravity = 0.5
SCREEN_WIDTH, SCREEN_HEIGHT = screen_size = (645, 400)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

screen_rect = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


def draw_text(screen):
    """Функция вывода текста об авторах"""
    text = []
    with open('data/final/text.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            text.append(*row)
    font = pygame.font.Font('data/final/seguisbi.ttf', 22)
    text_coord = 26
    for line in text:
        text = font.render(line, True, pygame.Color('white'))
        text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        text_y = text_coord + text.get_height()
        text_coord = text_y
        screen.blit(text, (text_x, text_y))


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
        self.gravity = gravity

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


all_sprites = pygame.sprite.Group()
star_group = pygame.sprite.Group()

pygame.mouse.set_visible(True)
for i in range(-300, 400, 50):
    create_particles((SCREEN_WIDTH // 2 + i, 0))
pygame.display.set_caption('PyPurble Game Studio')  # Название приложения
pygame.display.set_icon(load_image("icon.ico"))  # Иконка приложения

exit_img = pygame.transform.scale(load_image("BlackForrest/exit_btn.png", color_key=-1), (117, 49))

"""Анмированные герои"""
dragon = AnimatedSprite(load_image("final/dragon_sheet8x2.png", color_key=-1), 8, 2, 523, 299, all_sprites, 6)
girl = AnimatedSprite(load_image("final/girl.png", color_key=-1), 6, 1, 523, 1, all_sprites, 6)
bird = AnimatedSprite(load_image("final/bird.png", color_key=-1), 6, 2, 15, 1, all_sprites, 6)
boy = AnimatedSprite(load_image("final/boy.png", color_key=-1), 5, 4, 20, 250, all_sprites, 6)


def final_game_screen(dic_game):
    """Функция отображения окна с авторами"""
    global exit_img
    exit_btn = Button(255.5, 350, exit_img)
    while dic_game['authors']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.K_RETURN and event.key == pygame.K_ESCAPE):
                dic_game['authors'] = False
                dic_game['game'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
        fon = pygame.transform.scale(load_image('final.png'), screen_size)  # картинка
        screen.blit(fon, (0, 0))
        draw_text(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        star_group.update()
        star_group.draw(screen)
        exit_btn.update()
        if exit_btn.clicked:
            dic_game['authors'] = False
            dic_game['houses'] = True

        pygame.display.flip()
        clock.tick(FPS)
    return dic_game


if __name__ == '__main__':
    dic_game = {'houses': False, 'authors': True, 'table': False, 'game': True,
                'mario_game': False, 'mario_menu': False, 'mario_res': False,
                'snow_game': False, 'snow_menu': False, 'snow_res': False,
                'forrest_game': False, 'forrest_menu': False, 'forrest_res': False}
    final_game_screen(dic_game)
