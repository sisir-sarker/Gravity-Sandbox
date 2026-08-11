"""Numerically stable gravity and orbit helpers."""

from __future__ import annotations

import math

from settings import G, SOFTENING, TIME_SCALE


def calculate_orbital_velocity(planet, center, clockwise=True):
    """Return tangential velocity for a near-circular orbit about *center*."""
    offset = planet.position - center.position
    distance = offset.length()
    if distance == 0:
        return (0.0, 0.0)

    # Match the softened acceleration used in ``physics_step`` exactly:
    # v² / r = G * M / (r² + softening²).
    speed = math.sqrt(G * center.mass * distance / (distance**2 + SOFTENING**2))
    tangent = offset.rotate(90 if clockwise else -90).normalize()
    return tangent * speed


def calculate_accelerations(planets):
    """Return Sun-only acceleration for each moving body.

    Bodies are deliberately independent: no planet can pull, collide with, or
    alter another planet's path.  This gives the clean trajectories seen in
    the reference sandbox.
    """
    accelerations = [planet.position * 0 for planet in planets]
    sun = next((planet for planet in planets if planet.fixed), None)
    if sun is None:
        return accelerations

    for index, planet in enumerate(planets):
        if planet.fixed:
            continue
        displacement = sun.position - planet.position
        raw_distance_squared = displacement.length_squared()
        if raw_distance_squared == 0:
            continue
        direction = displacement.normalize()
        accelerations[index] = direction * (
            G * sun.mass / (raw_distance_squared + SOFTENING**2)
        )
    return accelerations


def physics_step(planets, dt):
    """Advance bodies with velocity Verlet integration.

    This symplectic integrator conserves orbital energy much better than the
    basic Euler method, which keeps long-running circular orbits clean.
    """
    step = dt * TIME_SCALE
    first_accelerations = calculate_accelerations(planets)

    for planet, acceleration in zip(planets, first_accelerations):
        if not planet.fixed:
            planet.velocity += acceleration * (step * 0.5)
            planet.position += planet.velocity * step

    second_accelerations = calculate_accelerations(planets)
    for planet, acceleration in zip(planets, second_accelerations):
        if not planet.fixed:
            planet.velocity += acceleration * (step * 0.5)
            planet.update_trail()


def prevent_planet_overlap(planets):
    """Compatibility no-op; bodies intentionally have no mutual interaction."""
    return None
