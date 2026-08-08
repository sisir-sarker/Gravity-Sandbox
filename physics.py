import math

from settings import G, SOFTENING, DT


# =======================================
# Distance
# =======================================

def calculate_distance(planet1, planet2):

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
    # Gravity with softening
    #
    # a = GM / (r^2 + s^2)
    #
    # For circular orbit:
    #
    # v^2 / r = GM / (r^2 + s^2)
    #
    # Therefore:
    #
    # v = sqrt(GM*r / (r^2+s^2))
    # -----------------------------------

    speed = math.sqrt(
        (
            G *
            sun.mass *
            radius
        )
        /
        (
            radius * radius
            +
            SOFTENING * SOFTENING
        )
    )

    # -----------------------------------
    # Tangent Direction
    # -----------------------------------

    tangent_x = -dy / radius
    tangent_y = dx / radius

    vx = tangent_x * speed
    vy = tangent_y * speed

    return vx, vy


# =======================================
# Gravity Between Two Planets
# =======================================

def apply_gravity_pair(
    planet1,
    planet2
):

    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    distance_squared = (
        dx * dx +
        dy * dy +
        SOFTENING * SOFTENING
    )

    distance = math.sqrt(
        distance_squared
    )

    if distance == 0:
        return

    # Unit direction
    nx = dx / distance
    ny = dy / distance

    # ===================================
    # Planet 1 Acceleration
    # ===================================

    if not planet1.fixed:

        acceleration1 = (
            G *
            planet2.mass
            /
            distance_squared
        )

        planet1.vx += (
            acceleration1 *
            nx *
            DT
        )

        planet1.vy += (
            acceleration1 *
            ny *
            DT
        )

    # ===================================
    # Planet 2 Acceleration
    # ===================================

    if not planet2.fixed:

        acceleration2 = (
            G *
            planet1.mass
            /
            distance_squared
        )

        planet2.vx -= (
            acceleration2 *
            nx *
            DT
        )

        planet2.vy -= (
            acceleration2 *
            ny *
            DT
        )


# =======================================
# Collision Check
# =======================================

def check_collision(
    planet1,
    planet2
):

    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    return distance <= (
        planet1.radius +
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
        return

    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    distance = math.sqrt(
        dx * dx +
        dy * dy
    )

    if distance == 0:

        distance = 0.1

    # Unit normal
    nx = dx / distance
    ny = dy / distance

    # ===================================
    # Remove Overlap
    # ===================================

    overlap = (
        planet1.radius +
        planet2.radius -
        distance
    )

    if overlap > 0:

        if planet1.fixed:

            planet2.x += nx * overlap
            planet2.y += ny * overlap

        elif planet2.fixed:

            planet1.x -= nx * overlap
            planet1.y -= ny * overlap

        else:

            planet1.x -= nx * overlap / 2
            planet1.y -= ny * overlap / 2

            planet2.x += nx * overlap / 2
            planet2.y += ny * overlap / 2

    # ===================================
    # Relative Velocity
    # ===================================

    relative_vx = (
        planet2.vx -
        planet1.vx
    )

    relative_vy = (
        planet2.vy -
        planet1.vy
    )

    velocity_along_normal = (
        relative_vx * nx +
        relative_vy * ny
    )

    # Already moving apart
    if velocity_along_normal > 0:
        return

    # ===================================
    # Bounce
    # ===================================

    restitution = 0.9

    inverse_mass1 = (
        0
        if planet1.fixed
        else 1 / planet1.mass
    )

    inverse_mass2 = (
        0
        if planet2.fixed
        else 1 / planet2.mass
    )

    total_inverse_mass = (
        inverse_mass1 +
        inverse_mass2
    )

    if total_inverse_mass == 0:
        return

    impulse = (
        -(1 + restitution)
        *
        velocity_along_normal
        /
        total_inverse_mass
    )

    impulse_x = impulse * nx
    impulse_y = impulse * ny

    if not planet1.fixed:

        planet1.vx -= (
            impulse_x *
            inverse_mass1
        )

        planet1.vy -= (
            impulse_y *
            inverse_mass1
        )

    if not planet2.fixed:

        planet2.vx += (
            impulse_x *
            inverse_mass2
        )

        planet2.vy += (
            impulse_y *
            inverse_mass2
        )