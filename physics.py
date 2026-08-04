import math

from settings import G, SOFTENING, DT


# -----------------------------
# Distance (Gravity)
# -----------------------------
def calculate_distance(planet1, planet2):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    return math.sqrt(
        dx * dx +
        dy * dy +
        SOFTENING * SOFTENING
    )


# -----------------------------
# Collision Check
# -----------------------------
def check_collision(planet1, planet2):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    distance = math.sqrt(dx * dx + dy * dy)

    return distance <= (planet1.radius + planet2.radius)


# -----------------------------
# Gravity Force
# -----------------------------
def calculate_force(planet1, planet2):

    distance = calculate_distance(planet1, planet2)

    return G * planet2.mass / (distance * distance)


# -----------------------------
# Apply Gravity
# -----------------------------
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


# -----------------------------
# Elastic Collision Bounce
# -----------------------------
def resolve_collision(planet1, planet2):

    if not check_collision(planet1, planet2):
        return

    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y

    distance = math.sqrt(dx * dx + dy * dy)

    if distance == 0:
        distance = 0.1

    # Unit Normal
    nx = dx / distance
    ny = dy / distance

    # --------------------------------
    # Remove Overlap
    # --------------------------------

    overlap = (planet1.radius + planet2.radius) - distance

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

    # --------------------------------
    # Relative Velocity
    # --------------------------------

    rvx = planet2.vx - planet1.vx
    rvy = planet2.vy - planet1.vy

    velocity_along_normal = rvx * nx + rvy * ny

    if velocity_along_normal > 0:
        return

    restitution = 0.9

    inv_mass1 = 0 if planet1.fixed else 1 / planet1.mass
    inv_mass2 = 0 if planet2.fixed else 1 / planet2.mass

    impulse = -(1 + restitution)
    impulse *= velocity_along_normal
    impulse /= (inv_mass1 + inv_mass2)

    impulse_x = impulse * nx
    impulse_y = impulse * ny

    if not planet1.fixed:
        planet1.vx -= impulse_x * inv_mass1
        planet1.vy -= impulse_y * inv_mass1

    if not planet2.fixed:
        planet2.vx += impulse_x * inv_mass2
        planet2.vy += impulse_y * inv_mass2