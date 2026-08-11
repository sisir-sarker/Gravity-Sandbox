"""Run the interactive Gravity Sandbox."""

from __future__ import annotations

import random
import pygame

from explosion import Explosion
from physics import calculate_orbital_velocity, physics_step, resolve_sun_impacts
from planet import Planet
from settings import *


def make_sun():
    return Planet(WIDTH // 2, HEIGHT // 2, 45, SUN_RED, fixed=True, name="Sun")


def make_orbiting_planet(sun, position, radius=12, color=BLUE, name=None):
    planet = Planet(*position, radius, color, name=name)
    planet.velocity = calculate_orbital_velocity(planet, sun)
    return planet


def initial_planets():
    sun = make_sun()
    solar_system = (
        ("Mercury", 72, 4, MOON, 15),
        ("Venus", 105, 6, SATURN, 75),
        ("Earth", 140, 7, BLUE, 135),
        ("Mars", 178, 5, MARS, 195),
        ("Jupiter", 224, 12, JUPITER, 255),
        ("Saturn", 270, 10, SATURN, 315),
        ("Uranus", 315, 8, CYAN, 35),
        ("Neptune", 360, 8, BLUE, 95),
    )
    planets = [sun]
    for name, orbit_radius, radius, color, angle in solar_system:
        offset = pygame.Vector2(orbit_radius, 0).rotate(angle)
        planets.append(
            make_orbiting_planet(sun, sun.position + offset, radius, color, name)
        )
    return planets


def draw_text(surface, font, text, position):
    surface.blit(font.render(text, True, WHITE), position)


def draw_arrow(surface, start, end, color=WHITE):
    """Draw a velocity vector with a small arrow head."""
    start, end = pygame.Vector2(start), pygame.Vector2(end)
    vector = end - start
    if vector.length() < 1:
        return
    pygame.draw.line(surface, color, start, end, 2)
    direction = vector.normalize()
    left = end - direction.rotate(28) * 11
    right = end - direction.rotate(-28) * 11
    pygame.draw.polygon(surface, color, [end, left, right])


def draw_launch_preview(surface, font, sun, start, mouse_position):
    """Show the predicted launch body, velocity vector, and circular guide."""
    distance = (start - sun.position).length()
    if distance > sun.radius + 5:
        pygame.draw.circle(surface, (115, 55, 70), sun.position, int(distance), 1)
    pygame.draw.circle(surface, CYAN, start, 10, 1)
    draw_arrow(surface, start, mouse_position, CYAN)
    velocity = (mouse_position - start) * LAUNCH_VELOCITY_SCALE
    draw_text(surface, font, f"Launch velocity: {velocity.length():.1f}", (16, 42))


def bounded_launch_velocity(sun, position, requested_velocity):
    """Keep manual launches gravitationally bound to the sun by default."""
    probe = Planet(*position, 10, BLUE)
    circular_speed = calculate_orbital_velocity(probe, sun).length()
    maximum_speed = circular_speed * MAX_LAUNCH_SPEED_MULTIPLIER
    if requested_velocity.length() > maximum_speed:
        return requested_velocity.normalize() * maximum_speed
    return requested_velocity


def main():
    pygame.init()
    fullscreen = START_FULLSCREEN
    display_flags = pygame.FULLSCREEN | pygame.SCALED if fullscreen else 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT), display_flags)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    planets = initial_planets()
    paused = False
    running = True
    launch_start = None
    speed_multiplier = 1.0
    custom_planet_index = 1
    explosions = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    speed_multiplier = min(4.0, speed_multiplier * 2)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed_multiplier = max(0.125, speed_multiplier / 2)
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    display_flags = pygame.FULLSCREEN | pygame.SCALED if fullscreen else 0
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), display_flags)
                elif event.key == pygame.K_r:
                    planets = initial_planets()
                    paused = False
                    launch_start = None
                    custom_planet_index = 1
                elif event.key == pygame.K_c:
                    planets = [make_sun()]
                    launch_start = None
                    custom_planet_index = 1
                elif event.key == pygame.K_o:
                    planets = initial_planets()
                    custom_planet_index = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                launch_start = pygame.Vector2(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and launch_start is not None:
                sun = planets[0]
                radius = random.randint(7, 16)
                color = random.choice(PLANET_COLORS)
                name = f"Planet X{custom_planet_index}"
                drag = pygame.Vector2(event.pos) - launch_start
                if drag.length() < CLICK_DRAG_THRESHOLD:
                    planets.append(make_orbiting_planet(sun, launch_start, radius, color, name))
                else:
                    velocity = bounded_launch_velocity(
                        sun, launch_start, drag * LAUNCH_VELOCITY_SCALE
                    )
                    planets.append(Planet(*launch_start, radius, color, velocity, name=name))
                custom_planet_index += 1
                launch_start = None

        if not paused:
            physics_step(planets, DT * speed_multiplier)
            planets, impacts = resolve_sun_impacts(planets)
            explosions.extend(Explosion(**impact) for impact in impacts)
            planets = [planet for planet in planets if planet.fixed or not planet.is_outside_screen()]
            for explosion in explosions:
                explosion.update(DT * speed_multiplier)
            explosions = [explosion for explosion in explosions if explosion.alive]

        screen.fill(BLACK)
        for planet in planets:
            planet.draw(screen, font)
        for explosion in explosions:
            explosion.draw(screen)
        if launch_start is not None:
            draw_launch_preview(screen, font, planets[0], launch_start, pygame.mouse.get_pos())
        draw_text(screen, font, "Drag: launch | Click: circular orbit | +/-: speed | F: fullscreen | Space: pause | R/O: solar system | C: clear", (16, 14))
        draw_text(screen, font, f"Speed: {speed_multiplier:g}x | Planet gravity: off", (16, 42))
        if paused:
            draw_text(screen, font, "PAUSED", (16, 66))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
