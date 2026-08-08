import pygame
import random
import math

from settings import *
from planet import Planet

from physics import (
    apply_gravity_pair,
    resolve_collision,
    calculate_orbital_velocity
)


# =======================================
# Pygame Initialization
# =======================================

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    None,
    26
)

big_font = pygame.font.SysFont(
    None,
    55
)


# =======================================
# Planet Colors
# =======================================

PLANET_COLORS = [
    BLUE,
    RED,
    GREEN,
    PURPLE,
    ORANGE,
    CYAN
]


# =======================================
# Create Sun
# =======================================

def create_sun():

    return Planet(
        WIDTH // 2,
        HEIGHT // 2,
        40,
        YELLOW,
        fixed=True
    )


# =======================================
# Find Sun
# =======================================

def find_sun(planets):

    for planet in planets:

        if planet.fixed:
            return planet

    return None


# =======================================
# Create Earth Orbit
# =======================================

def create_initial_planets():

    sun = create_sun()

    # Distance from Sun
    orbit_radius = 250

    earth = Planet(
        WIDTH // 2 + orbit_radius,
        HEIGHT // 2,
        15,
        BLUE
    )

    # Calculate circular orbital velocity
    earth.vx, earth.vy = (
        calculate_orbital_velocity(
            earth,
            sun
        )
    )

    return [
        sun,
        earth
    ]


# =======================================
# Orbit Demo
# =======================================

def create_orbit_demo():

    sun = create_sun()

    orbit_radius = 250

    earth = Planet(
        WIDTH // 2 + orbit_radius,
        HEIGHT // 2,
        15,
        BLUE
    )

    earth.vx, earth.vy = (
        calculate_orbital_velocity(
            earth,
            sun
        )
    )

    return [
        sun,
        earth
    ]


# =======================================
# Create Random Orbital Planet
# =======================================

def create_random_planet(
    x,
    y,
    sun
):

    radius = random.randint(
        10,
        22
    )

    planet = Planet(
        x,
        y,
        radius,
        random.choice(
            PLANET_COLORS
        )
    )

    # ===================================
    # No Sun Available
    # ===================================

    if sun is None:

        planet.vx = random.uniform(
            -30,
            30
        )

        planet.vy = random.uniform(
            -30,
            30
        )

        return planet

    # ===================================
    # Distance From Sun
    # ===================================

    dx = planet.x - sun.x
    dy = planet.y - sun.y

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    minimum_distance = (
        sun.radius +
        radius +
        30
    )

    # ===================================
    # Too Close To Sun
    # ===================================

    if distance <= minimum_distance:

        planet.x = (
            sun.x +
            minimum_distance
        )

        planet.y = sun.y

        distance = minimum_distance

    # ===================================
    # Orbital Velocity
    # ===================================

    planet.vx, planet.vy = (
        calculate_orbital_velocity(
            planet,
            sun
        )
    )

    return planet


# =======================================
# Initial Scene
# =======================================

planets = create_initial_planets()

paused = False

running = True


# =======================================
# Main Loop
# =======================================

while running:

    clock.tick(FPS)

    # ===================================
    # Events
    # ===================================

    for event in pygame.event.get():

        # --------------------------------
        # Quit
        # --------------------------------

        if event.type == pygame.QUIT:

            running = False

        # --------------------------------
        # Keyboard
        # --------------------------------

        if event.type == pygame.KEYDOWN:

            # Pause / Resume
            if event.key == pygame.K_SPACE:

                paused = not paused

            # Reset
            elif event.key == pygame.K_r:

                planets = create_initial_planets()

                paused = False

            # Orbit Demo
            elif event.key == pygame.K_o:

                planets = create_orbit_demo()

                paused = False

            # Clear
            elif event.key == pygame.K_c:

                planets = []

        # --------------------------------
        # Mouse
        # --------------------------------

        if (
            event.type ==
            pygame.MOUSEBUTTONDOWN
            and not paused
        ):

            x, y = pygame.mouse.get_pos()

            sun = find_sun(planets)

            new_planet = (
                create_random_planet(
                    x,
                    y,
                    sun
                )
            )

            planets.append(
                new_planet
            )

    # ===================================
    # Physics
    # ===================================

    if not paused:

        # --------------------------------
        # Gravity
        # --------------------------------

        for i in range(
            len(planets)
        ):

            for j in range(
                i + 1,
                len(planets)
            ):

                apply_gravity_pair(
                    planets[i],
                    planets[j]
                )

        # --------------------------------
        # Collision
        # --------------------------------

        for i in range(
            len(planets)
        ):

            for j in range(
                i + 1,
                len(planets)
            ):

                resolve_collision(
                    planets[i],
                    planets[j]
                )

        # --------------------------------
        # Movement
        # --------------------------------

        for planet in planets:

            planet.move()

    # ===================================
    # Drawing
    # ===================================

    screen.fill(BLACK)

    # Draw all planets
    for planet in planets:

        planet.draw(screen)

    # ===================================
    # Information
    # ===================================

    fps_text = font.render(
        f"FPS: {int(clock.get_fps())}",
        True,
        WHITE
    )

    screen.blit(
        fps_text,
        (10, 10)
    )

    planet_text = font.render(
        f"Planets: {len(planets)}",
        True,
        WHITE
    )

    screen.blit(
        planet_text,
        (10, 40)
    )

    status = (
        "PAUSED"
        if paused
        else
        "RUNNING"
    )

    status_text = font.render(
        f"Status: {status}",
        True,
        WHITE
    )

    screen.blit(
        status_text,
        (10, 70)
    )

    # ===================================
    # Controls
    # ===================================

    controls_text = font.render(
        "SPACE: Pause | R: Reset | O: Orbit | C: Clear | Mouse: Planet",
        True,
        WHITE
    )

    screen.blit(
        controls_text,
        (
            10,
            HEIGHT - 30
        )
    )

    # ===================================
    # Pause Message
    # ===================================

    if paused:

        pause_text = big_font.render(
            "PAUSED",
            True,
            WHITE
        )

        screen.blit(
            pause_text,
            (
                WIDTH // 2
                -
                pause_text.get_width() // 2,
                40
            )
        )

    # ===================================
    # Update Screen
    # ===================================

    pygame.display.flip()


# =======================================
# Quit
# =======================================

pygame.quit()