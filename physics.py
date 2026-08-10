import math

from settings import (
    G,
    SOFTENING,
    DT
)


# =======================================
# Distance
# =======================================

def calculate_distance(
    planet1,
    planet2
):

    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    return math.sqrt(
        dx * dx +
        dy * dy
    )


# =======================================
# Circular Orbital Velocity
# =======================================

def calculate_orbital_velocity(
    planet,
    sun
):

    dx = planet.x - sun.x
    dy = planet.y - sun.y

    radius = math.sqrt(
        dx * dx +
        dy * dy
    )

    if radius <= 0:
        return 0.0, 0.0

    # -----------------------------------
    # Softened circular orbit
    #
    # a = GM*r / (r²+s²)^(3/2)
    #
    # v²/r = a
    #
    # Therefore:
    #
    # v = sqrt(
    # GM*r² /
    # (r²+s²)^(3/2)
    # )
    # -----------------------------------

    denominator = (
        radius * radius
        +
        SOFTENING * SOFTENING
    ) ** 1.5

    speed_squared = (
        G
        * sun.mass
        * radius
        * radius
        /
        denominator
    )

    speed = math.sqrt(
        speed_squared
    )

    # -----------------------------------
    # Tangent Direction
    # -----------------------------------

    tangent_x = -dy / radius
    tangent_y = dx / radius

    return (
        tangent_x * speed,
        tangent_y * speed
    )


# =======================================
# Calculate All Accelerations
# =======================================

def calculate_accelerations(
    planets
):

    accelerations = []

    # One acceleration pair for every planet
    for planet in planets:

        accelerations.append(
            [0.0, 0.0]
        )

    # ===================================
    # Pair-wise Gravity
    # ===================================

    for i in range(
        len(planets)
    ):

        for j in range(
            i + 1,
            len(planets)
        ):

            planet1 = planets[i]
            planet2 = planets[j]

            dx = (
                planet2.x
                -
                planet1.x
            )

            dy = (
                planet2.y
                -
                planet1.y
            )

            distance_squared = (
                dx * dx
                +
                dy * dy
                +
                SOFTENING * SOFTENING
            )

            if distance_squared <= 0:
                continue

            distance = math.sqrt(
                distance_squared
            )

            # --------------------------------
            # Common gravity factor
            # --------------------------------

            factor = (
                G
                /
                (
                    distance_squared
                    * distance
                )
            )

            # --------------------------------
            # Planet 1 acceleration
            # --------------------------------

            if not planet1.fixed:

                acceleration1 = (
                    factor
                    *
                    planet2.mass
                )

                accelerations[i][0] += (
                    acceleration1
                    * dx
                )

                accelerations[i][1] += (
                    acceleration1
                    * dy
                )

            # --------------------------------
            # Planet 2 acceleration
            # --------------------------------

            if not planet2.fixed:

                acceleration2 = (
                    factor
                    *
                    planet1.mass
                )

                accelerations[j][0] -= (
                    acceleration2
                    * dx
                )

                accelerations[j][1] -= (
                    acceleration2
                    * dy
                )

    return accelerations


# =======================================
# Stable Physics Step
# =======================================

def physics_step(
    planets
):

    if not planets:
        return

    # -----------------------------------
    # First acceleration
    # -----------------------------------

    accelerations_before = (
        calculate_accelerations(
            planets
        )
    )

    # -----------------------------------
    # Half velocity update
    # -----------------------------------

    for i, planet in enumerate(
        planets
    ):

        if planet.fixed:
            continue

        ax, ay = (
            accelerations_before[i]
        )

        planet.vx += (
            ax
            * DT
            * 0.5
        )

        planet.vy += (
            ay
            * DT
            * 0.5
        )

    # -----------------------------------
    # Position update
    # -----------------------------------

    for planet in planets:

        planet.move()

    # -----------------------------------
    # New acceleration after movement
    # -----------------------------------

    accelerations_after = (
        calculate_accelerations(
            planets
        )
    )

    # -----------------------------------
    # Second half velocity update
    # -----------------------------------

    for i, planet in enumerate(
        planets
    ):

        if planet.fixed:
            continue

        ax, ay = (
            accelerations_after[i]
        )

        planet.vx += (
            ax
            * DT
            * 0.5
        )

        planet.vy += (
            ay
            * DT
            * 0.5
        )


# =======================================
# Collision Check
# =======================================

def check_collision(
    planet1,
    planet2
):

    dx = (
        planet2.x
        -
        planet1.x
    )

    dy = (
        planet2.y
        -
        planet1.y
    )

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    return distance <= (
        planet1.radius
        +
        planet2.radius
    )


# =======================================
# Collision Resolution
# =======================================

def resolve_collision(
    planet1,
    planet2
):

    if not check_collision(
        planet1,
        planet2
    ):
        return None

    # ===================================
    # Sun Collision
    # ===================================

    # Planet hitting Sun is absorbed.
    # It does NOT bounce.

    if planet1.fixed and not planet2.fixed:

        return planet2

    if planet2.fixed and not planet1.fixed:

        return planet1

    # ===================================
    # Fixed-Fixed
    # ===================================

    if (
        planet1.fixed
        and
        planet2.fixed
    ):
        return None

    # ===================================
    # Planet-Planet Collision
    # ===================================

    dx = (
        planet2.x
        -
        planet1.x
    )

    dy = (
        planet2.y
        -
        planet1.y
    )

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    if distance == 0:
        distance = 0.1

    nx = dx / distance
    ny = dy / distance

    # -----------------------------------
    # Remove overlap
    # -----------------------------------

    overlap = (
        planet1.radius
        +
        planet2.radius
        -
        distance
    )

    if overlap > 0:

        planet1.x -= (
            nx
            * overlap
            * 0.5
        )

        planet1.y -= (
            ny
            * overlap
            * 0.5
        )

        planet2.x += (
            nx
            * overlap
            * 0.5
        )

        planet2.y += (
            ny
            * overlap
            * 0.5
        )

    # -----------------------------------
    # Relative velocity
    # -----------------------------------

    relative_vx = (
        planet2.vx
        -
        planet1.vx
    )

    relative_vy = (
        planet2.vy
        -
        planet1.vy
    )

    velocity_along_normal = (
        relative_vx * nx
        +
        relative_vy * ny
    )

    # Already moving apart
    if velocity_along_normal > 0:

        return None

    # -----------------------------------
    # Bounce
    # -----------------------------------

    restitution = 0.9

    inverse_mass1 = (
        1 / planet1.mass
    )

    inverse_mass2 = (
        1 / planet2.mass
    )

    total_inverse_mass = (
        inverse_mass1
        +
        inverse_mass2
    )

    impulse = (
        -(1 + restitution)
        *
        velocity_along_normal
        /
        total_inverse_mass
    )

    impulse_x = impulse * nx
    impulse_y = impulse * ny

    planet1.vx -= (
        impulse_x
        *
        inverse_mass1
    )

    planet1.vy -= (
        impulse_y
        *
        inverse_mass1
    )

    planet2.vx += (
        impulse_x
        *
        inverse_mass2
    )

    planet2.vy += (
        impulse_y
        *
        inverse_mass2
    )

    return None