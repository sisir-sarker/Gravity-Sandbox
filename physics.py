import math


G = 0.1
SOFTENING = 20


def apply_gravity(planets):

    for planet1 in planets:

        # Fixed planet-এর velocity change হবে না
        if planet1.fixed:
            continue

        total_ax = 0
        total_ay = 0

        for planet2 in planets:

            if planet1 is planet2:
                continue

            dx = planet2.x - planet1.x
            dy = planet2.y - planet1.y

            distance_squared = (
                dx * dx
                + dy * dy
                + SOFTENING * SOFTENING
            )

            distance = math.sqrt(distance_squared)

            # planet2-এর mass planet1-কে আকর্ষণ করছে
            acceleration = (
                G * planet2.mass / distance_squared
            )

            ax = acceleration * dx / distance
            ay = acceleration * dy / distance

            total_ax += ax
            total_ay += ay

        planet1.vx += total_ax
        planet1.vy += total_ay