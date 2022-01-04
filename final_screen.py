import csv
import random

from main_functions import *

pygame.init()
FPS = 60
gravity = 0.5
WIDTH, HEIGHT = 645, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

screen_rect = (0, 0, WIDTH, HEIGHT)


def draw_text(screen):
    text = []
    with open('data/text.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            text.append(*row)
    font = pygame.font.Font('data/seguisbi.ttf', 22)
    text_coord = 26
    for line in text:
        text = font.render(line, True, pygame.Color('white'))
        text_x = WIDTH // 2 - text.get_width() // 2
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


class AnimatedSprite(pygame.sprite.Sprite):
    """Класс анимации для спрайтов"""

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.count_iteration = 0
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
        if self.count_iteration % 8 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


all_sprites = pygame.sprite.Group()
star_group = pygame.sprite.Group()

pygame.mouse.set_visible(False)
for i in range(-300, 400, 50):
    create_particles((WIDTH // 2 + i, 0))
pygame.display.set_caption('ДОПИСАТЬ НАЗВАНИЕ')  # Название приложения
dragon = AnimatedSprite(load_image("dragon_sheet8x2.png", color_key=-1), 8, 2, 483, 299)
girl = AnimatedSprite(load_image("girl.png", color_key=-1), 6, 1, 295, 299)
bird = AnimatedSprite(load_image("bird.png", color_key=-1), 6, 2, 15, 1)
boy = AnimatedSprite(load_image("boy.png", color_key=-1), 5, 4, 20, 250)


def final_game_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.K_RETURN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
        fon = pygame.transform.scale(load_image('final.png'), (WIDTH, HEIGHT))  # картинка
        screen.blit(fon, (0, 0))
        draw_text(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        star_group.update()
        star_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == '__main__':
    final_game_screen()
