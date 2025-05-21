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

run = True
while run:

    clock.tick(fps)

    # draw background
    screen.blit(day_background, (0, 0))

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
