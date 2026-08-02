import math

from settings import G, SOFTENING, DT


def calculate_distance(planet1, planet2):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    distance = math.sqrt(
        dx * dx +
        dy * dy +
        SOFTENING * SOFTENING
    )

    return distance


def check_collision(planet1, planet2):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    actual_distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    return actual_distance <= planet1.radius + planet2.radius


def calculate_force(planet1, planet2):
    distance = calculate_distance(planet1, planet2)

    force = G * planet2.mass / (distance * distance)

    return force


def apply_gravity(planet1, planet2):
    if planet1.fixed:
        return

    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    distance = calculate_distance(planet1, planet2)
    force = calculate_force(planet1, planet2)

    ax = force * dx / distance
    ay = force * dy / distance

    planet1.vx += ax * DT
    planet1.vy += ay * DT