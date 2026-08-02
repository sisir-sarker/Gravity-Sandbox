import pygame
import random

from settings import *
from planet import Planet
from physics import apply_gravity

pygame.init()

font = pygame.font.SysFont(None, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()


def create_initial_planets():
    sun = Planet(
        WIDTH // 2,
        HEIGHT // 2,
        40,
        WHITE,
        fixed=True
    )

    planet = Planet(
        WIDTH // 2 + 200,
        HEIGHT // 2,
        15,
        WHITE
    )
    planet.vy = 120

    return [sun, planet]


planets = create_initial_planets()

paused = False


running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard Controls
        if event.type == pygame.KEYDOWN:

            # Pause / Resume
            if event.key == pygame.K_SPACE:
                paused = not paused

            # Reset
            if event.key == pygame.K_r:
                planets = create_initial_planets()

            # Speed Increase
            

        # Mouse Create Planet
        if event.type == pygame.MOUSEBUTTONDOWN and not paused:

            x, y = pygame.mouse.get_pos()

            radius = random.randint(10, 35)

            planets.append(
                Planet(
                    x,
                    y,
                    radius,
                    WHITE
                )
            )

    screen.fill(BLACK)

    if not paused:

        # Gravity
        for i in range(len(planets)):
            for j in range(len(planets)):
                if i != j:
                    apply_gravity(planets[i], planets[j])

        # Move
        for planet in planets:
            planet.move()

    # Draw Planets
    for planet in planets:
        planet.draw(screen)

    # FPS Counter
    fps_text = font.render(
        f"FPS: {int(clock.get_fps())}",
        True,
        WHITE
    )

    screen.blit(fps_text, (10, 10))

    # Speed Counter


    pygame.display.flip()

pygame.quit()