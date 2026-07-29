import pygame
import random

from settings import *
from planet import Planet
from physics import apply_gravity


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()


# বড় Sun তৈরি
sun = Planet(
    WIDTH // 2,
    HEIGHT // 2,
    50,
    WHITE,
    fixed=True
)

sun.mass = 5000


# Sun থেকে 200 pixel দূরে Earth
earth = Planet(
    WIDTH // 2 + 200,
    HEIGHT // 2,
    15,
    WHITE
)

# Orbit-এর জন্য tangential velocity
earth.vx = 0
earth.vy = 1.57


planets = [
    sun,
    earth
]


running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            radius = random.randint(10, 25)

            new_planet = Planet(
                x,
                y,
                radius,
                WHITE
            )

            new_planet.vx = 0
            new_planet.vy = 0

            planets.append(new_planet)

    screen.fill(BLACK)

    apply_gravity(planets)

    for planet in planets:

        planet.move()
        planet.draw(screen)

    pygame.display.flip()


pygame.quit()