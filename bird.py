import pygame
import random
import time

pygame.init()

# main window
screen_width = 634
screen_height = 636
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# main variables
clock = pygame.time.Clock()
fps = 60
white = (255, 255, 255)
high_score = 0


# main classes
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # check if mouse is over button
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# main functions
def draw_text(text, font_name, font_size, text_colour, x, y, center):
    game_font = pygame.font.Font(font_name, font_size)
    img = game_font.render(text, True, text_colour)

    if center:
        text_rect = img.get_rect(center=(x, y))
    else:
        text_rect = img.get_rect(topleft=(x, y))

    screen.blit(img, text_rect)


# load images and handle day/night mode
themes = {
    "day": {
        "background": "assets/images/day_background.png",
        "ground": "assets/images/day_ground.png",
        "main": "assets/images/day_main.png",
        "mode": "assets/images/day_mode.png",
        "play": "assets/images/day_play.png",
        "quit": "assets/images/day_quit.png",
        "restart": "assets/images/day_restart.png"
    },
    "night": {
        "background": "assets/images/night_background.png",
        "ground": "assets/images/night_ground.png",
        "main": "assets/images/night_main.png",
        "mode": "assets/images/night_mode.png",
        "play": "assets/images/night_play.png",
        "quit": "assets/images/night_quit.png",
        "restart": "assets/images/night_restart.png"
    }
}

# initial mode and images
current_theme = "day"
active_day = True
active_night = False

image_background = pygame.image.load(themes[current_theme]["background"])
image_ground = pygame.image.load(themes[current_theme]["ground"])
image_main = pygame.image.load(themes[current_theme]["main"])
image_mode = pygame.image.load(themes[current_theme]["mode"])
image_play = pygame.image.load(themes[current_theme]["play"])
image_quit = pygame.image.load(themes[current_theme]["quit"])
image_restart = pygame.image.load(themes[current_theme]["restart"])


def switch_theme(theme_name):
    global image_background, image_ground, image_main, image_mode, image_play, image_quit, image_restart
    global active_day, active_night, current_theme

    current_theme = theme_name
    assets = themes[theme_name]
    image_background = pygame.image.load(assets["background"])
    image_ground = pygame.image.load(assets["ground"])
    image_main = pygame.image.load(themes[current_theme]["main"])
    image_mode = pygame.image.load(themes[current_theme]["mode"])
    image_play = pygame.image.load(themes[current_theme]["play"])
    image_quit = pygame.image.load(themes[current_theme]["quit"])
    image_restart = pygame.image.load(assets["restart"])

    active_day = (theme_name == "day")
    active_night = not active_day


def main_menu():
    play_button = Button(screen_width // 2 - 30, screen_height // 2 - 75, image_play)
    quit_button = Button(screen_width // 2 - 30, screen_height // 2, image_quit)
    mode_button = Button(screen_width - 50, screen_height - 625, image_mode)

    run_menu = True
    while run_menu:

        clock.tick(fps)

        screen.blit(image_background, (0, 0))
        screen.blit(image_ground, (0, 558))
        draw_text("FLAPPY BIRD", "assets/fonts/FlappyBirdRegular.ttf", 120, white, screen_width // 2, 160, True)

        if play_button.draw():
            play()
        if quit_button.draw():
            break
        if mode_button.draw():
            if active_day:
                switch_theme("night")
            else:
                switch_theme("day")

            play_button = Button(screen_width // 2 - 30, screen_height // 2 - 75, image_play)
            quit_button = Button(screen_width // 2 - 30, screen_height // 2, image_quit)
            mode_button = Button(screen_width - 50, screen_height - 625, image_mode)
            time.sleep(0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False

        pygame.display.update()

    pygame.quit()


def play():
    global high_score
    ground_scroll = 0
    scroll_speed = 4
    flying = False
    game_over = False
    obstacle_gap = 150
    obstacle_frequency = 1500
    last_obstacle = pygame.time.get_ticks() - obstacle_frequency
    score = 0
    pass_obstacle = False

    def reset_game():
        obstacle_group.empty()
        flappy.rect.x = 75
        flappy.rect.y = int(screen_height / 2 - 50)
        reset_score = 0
        return reset_score

    # main object classes
    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 4):
                if active_day:
                    bird_anim = pygame.image.load(f"assets/images/day_bird{num}.png")
                if active_night:
                    bird_anim = pygame.image.load(f"assets/images/night_bird{num}.png")
                self.images.append(bird_anim)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.vel = 0
            self.clicked = False

        def update(self):

            if flying:
                # gravity
                self.vel += 0.5
                if self.vel > 8:
                    self.vel = 8
                if self.rect.bottom < 558:
                    self.rect.y += int(self.vel)

            if not game_over:
                # jump
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    self.vel = -10
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

                # handle animation
                self.counter += 1
                flap_cooldown = 5

                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                self.image = self.images[self.index]
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * - 2)
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90)

    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
            pygame.sprite.Sprite.__init__(self)
            if active_day:
                self.image = pygame.image.load("assets/images/day_obstacle.png")
            if active_night:
                self.image = pygame.image.load("assets/images/night_obstacle.png")
            self.rect = self.image.get_rect()
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x, y - int(obstacle_gap / 2)]
            if position == -1:
                self.rect.topleft = [x, y + int(obstacle_gap / 2)]

        def update(self):
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()

    bird_group = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()

    flappy = Bird(100, int(screen_height / 2 - 40))

    bird_group.add(flappy)

    # create button instances
    restart_button = Button(screen_width // 2 - 50, screen_height // 2 - 100, image_restart)
    main_button = Button(screen_width // 2 - 65, screen_height // 2 - 25, image_main)

    run_play = True
    while run_play:

        clock.tick(fps)

        # draw background and objects
        screen.blit(image_background, (0, 0))
        bird_group.draw(screen)
        bird_group.update()
        obstacle_group.draw(screen)
        screen.blit(image_ground, (ground_scroll, 558))

        # check and draw score
        if len(obstacle_group) > 0:
            if bird_group.sprites()[0].rect.left > obstacle_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < obstacle_group.sprites()[0].rect.right \
                    and not pass_obstacle:
                pass_obstacle = True
            if pass_obstacle:
                if bird_group.sprites()[0].rect.left > obstacle_group.sprites()[0].rect.right:
                    score += 1
                    pass_obstacle = False

        draw_text(str(score), "assets/fonts/FlappyBirdRegular.ttf", 70, white, screen_width // 2 + 10, 50, True)
        draw_text(f"HI {str(high_score)}", "assets/fonts/FlappyBirdRegular.ttf", 40, white, 10, 600, False)

        # check for collision
        if pygame.sprite.groupcollide(bird_group, obstacle_group, False, False) or flappy.rect.top < 0:
            game_over = True

        # check if bird has hit the ground
        if flappy.rect.bottom >= 558:
            game_over = True
            flying = False

        if not game_over and flying:

            # generate new obstacles
            time_now = pygame.time.get_ticks()
            if time_now - last_obstacle > obstacle_frequency:
                obstacle_height = random.randint(-100, 100)
                btm_obstacle = Obstacle(screen_width, int(screen_height / 2) + obstacle_height, -1)
                top_obstacle = Obstacle(screen_width, int(screen_height / 2) + obstacle_height, 1)
                obstacle_group.add(btm_obstacle)
                obstacle_group.add(top_obstacle)
                last_obstacle = time_now

            # scroll ground
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0

            obstacle_group.update()

        if score > high_score:
            high_score = score

        if game_over:
            if restart_button.draw():
                game_over = False
                score = reset_game()
            if main_button.draw():
                main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_play = False
            if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True

        pygame.display.update()


main_menu()
