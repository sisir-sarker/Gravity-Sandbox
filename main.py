import pygame
import random

from settings import *
from planet import Planet

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

planets = [
    Planet(300, 300, 25, WHITE),
    Planet(500, 300, 35, WHITE),
    Planet(700, 300, 20, WHITE)
]

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            radius = random.randint(10, 35)

            new_planet = Planet(x, y, radius, WHITE)

            planets.append(new_planet)

    screen.fill(BLACK)

    for planet in planets:
        planet.draw(screen)

    pygame.display.flip()

pygame.quit()