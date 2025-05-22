import pygame
from pygame.locals import *

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


# load images
day_background = pygame.image.load("images/day_background.png")
day_ground = pygame.image.load("images/day_ground.png")


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # create flappy bird
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

    def update(self):
        # handle animation
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

run = True
while run:

    clock.tick(fps)

    # draw background and flappy bird
    screen.blit(day_background, (0, -155))

    bird_group.draw(screen)
    bird_group.update()

    # draw and scroll ground
    screen.blit(day_ground, (ground_scroll, 558))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
