import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

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
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/day_bird1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

run = True
while run:

    clock.tick(fps)

    # draw background and bird sprite
    screen.blit(day_background, (0, 0))

    bird_group.draw(screen)

    # draw and scroll ground
    screen.blit(day_ground, (ground_scroll, 728))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
