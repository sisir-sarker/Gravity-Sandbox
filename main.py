import pygame
import random

from settings import *
from planet import Planet
from physics import apply_gravity, resolve_collision

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 55)


# ---------------------------------------
# Random Planet Color
# ---------------------------------------
PLANET_COLORS = [
    (100, 180, 255),
    (255, 120, 120),
    (120, 255, 120),
    (255, 255, 120),
    (255, 120, 255),
    (120, 255, 255),
    (255, 180, 80)
]


# ---------------------------------------
# Initial Scene
# ---------------------------------------
def create_initial_planets():

    sun = Planet(
        WIDTH // 2,
        HEIGHT // 2,
        40,
        (255, 220, 0),
        fixed=True
    )

    earth = Planet(
        WIDTH // 2 + 200,
        HEIGHT // 2,
        15,
        (80, 170, 255)
    )

    earth.vy = 120

    return [sun, earth]


planets = create_initial_planets()

paused = False

running = True

while running:

    clock.tick(FPS)

    # -----------------------------
    # Events
    # -----------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:
                planets = create_initial_planets()

        # Create Planet
        if event.type == pygame.MOUSEBUTTONDOWN and not paused:

            x, y = pygame.mouse.get_pos()

            radius = random.randint(10, 30)

            planet = Planet(
                x,
                y,
                radius,
                random.choice(PLANET_COLORS)
            )

            planet.vx = random.uniform(-80, 80)
            planet.vy = random.uniform(-80, 80)

            planets.append(planet)

    # -----------------------------
    # Physics
    # -----------------------------
    if not paused:

        # Gravity
        for i in range(len(planets)):
            for j in range(len(planets)):
                if i != j:
                    apply_gravity(planets[i], planets[j])

        # Collision
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                resolve_collision(planets[i], planets[j])

        # Movement
        for planet in planets:
            planet.move()

    # -----------------------------
    # Draw
    # -----------------------------
    screen.fill(BLACK)

    for planet in planets:
        planet.draw(screen)

    # FPS
    fps = font.render(
        f"FPS : {int(clock.get_fps())}",
        True,
        WHITE
    )

    screen.blit(fps, (10, 10))

    # Planet Count
    count = font.render(
        f"Planets : {len(planets)}",
        True,
        WHITE
    )

    screen.blit(count, (10, 40))

    # Controls
    controls = font.render(
        "SPACE: Pause   R: Reset   Mouse: Create Planet",
        True,
        WHITE
    )

    screen.blit(controls, (10, HEIGHT - 30))

    # Pause Message
    if paused:

        txt = big_font.render(
            "PAUSED",
            True,
            WHITE
        )

        screen.blit(
            txt,
            (
                WIDTH // 2 - txt.get_width() // 2,
                40
            )
        )

    pygame.display.flip()

pygame.quit()