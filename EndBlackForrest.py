import pygame


pygame.init()
FPS = 60
gravity = 0.5
size = WIDTH, HEIGHT = 645, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

screen_rect = (0, 0, WIDTH, HEIGHT)


class End():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    pygame.mouse.set_visible(True)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.K_RETURN and event.key == pygame.K_ESCAPE):
                running = False
        if score_coins > 50:
            fon = pygame.transform.scale(load_image('you_won.png'), size)
        else:
            fon = pygame.transform.scale(load_image('you_not_won.png'), size)
        restart = Button(WIDTH // 2 - start_img.get_width() // 2 - 38,
                         HEIGHT // 2 - start_img.get_height() // 2 + 50,
                         pygame.transform.scale(load_image("restart_btn.png", colorkey=-1), (88, 38)))
        screen.blit(fon, (0, 0))
        restart.update()
        pygame.display.flip()
        if restart.clicked:
            print(20)