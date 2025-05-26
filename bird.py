import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 634
screen_height = 636

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
obstacle_gap = 150
obstacle_frequency = 1500
last_obstacle = pygame.time.get_ticks() - obstacle_frequency

# load images
day_background = pygame.image.load("images/day_background.png")
day_ground = pygame.image.load("images/day_ground.png")


# main object classes
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):

        # create bird
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            bird_anim = pygame.image.load(f"images/day_bird{num}.png")
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

            # rotate bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/day_obstacle.png")
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

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

run = True
while run:

    clock.tick(fps)

    # draw background and objects
    screen.blit(day_background, (0, -155))

    bird_group.draw(screen)
    bird_group.update()
    obstacle_group.draw(screen)

    # draw ground
    screen.blit(day_ground, (ground_scroll, 558))

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()
