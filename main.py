import pygame
from planet import Planet

from settings import *
from planet import Planet

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()
planet = Planet(
    WIDTH // 2,
    HEIGHT // 2,
    30,
    WHITE
)

planet = Planet(
    WIDTH // 2,
    HEIGHT // 2,
    40,
    WHITE
)

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    planet.draw(screen)

    planet.draw(screen)

    pygame.display.flip()

pygame.quit()