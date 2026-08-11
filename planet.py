"""Planet model and drawing helpers."""

from __future__ import annotations

from collections import deque
import math
import random
import pygame

from settings import HEIGHT, SUN_CORE, WHITE, WIDTH


class Planet:
    """A circular body represented in simulation coordinates (pixels)."""

    def __init__(self, x, y, radius, color, velocity=(0, 0), fixed=False, name=None):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity)
        self.radius = radius
        self.mass = float(radius**2)
        self.color = color
        self.fixed = fixed
        self.name = name
        self.trail = deque(maxlen=240)
        # Each body is rendered from stable, individual surface particles.
        generator = random.Random(f"{x:.1f}:{y:.1f}:{radius}:{color}")
        particle_count = 420 if fixed else max(22, radius * 3)
        self.surface_particles = []
        for _ in range(particle_count):
            angle = generator.uniform(0, math.tau)
            radial_distance = math.sqrt(generator.random()) * radius
            offset = pygame.Vector2(math.cos(angle), math.sin(angle)) * radial_distance
            brightness = generator.uniform(0.58, 1.12)
            dot_radius = 2 if fixed else 1
            self.surface_particles.append((offset, brightness, dot_radius))
        self.initial_particle_count = len(self.surface_particles)

    def update_trail(self):
        self.trail.append(self.position.copy())

    def is_outside_screen(self, margin=100):
        return (
            self.position.x < -margin
            or self.position.x > WIDTH + margin
            or self.position.y < -margin
            or self.position.y > HEIGHT + margin
        )

    def absorb_impact(self, projectile):
        """Remove an impact-sized section and return blast information."""
        if not self.fixed or not self.surface_particles:
            return None
        mass_ratio = projectile.mass / self.mass
        damage = min(0.60, 0.035 + mass_ratio * 1.20 + projectile.velocity.length() / 3000)
        removed_count = max(1, int(len(self.surface_particles) * damage))
        direction = projectile.position - self.position
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)
        direction = direction.normalize()
        impact_point = direction * self.radius
        self.surface_particles.sort(key=lambda particle: particle[0].distance_to(impact_point))
        del self.surface_particles[:removed_count]

        remaining_ratio = len(self.surface_particles) / self.initial_particle_count
        self.mass = max(1.0, self.mass * remaining_ratio)
        self.radius = max(12, int(self.radius * (0.82 + 0.18 * remaining_ratio)))
        return {
            "position": self.position + impact_point,
            "direction": direction,
            "strength": damage,
        }

    def draw(self, surface, font=None):
        if len(self.trail) > 1:
            pygame.draw.lines(surface, self.color, False, list(self.trail), 1)

        if self.fixed:
            # Soft, layered glow inspired by a dense hot particle body.
            glow = pygame.Surface((self.radius * 5, self.radius * 5), pygame.SRCALPHA)
            center = pygame.Vector2(glow.get_width() // 2, glow.get_height() // 2)
            for scale, alpha in ((2.2, 18), (1.7, 28), (1.35, 45)):
                pygame.draw.circle(glow, (*self.color, alpha), center, int(self.radius * scale))
            surface.blit(glow, glow.get_rect(center=self.position))

        for offset, brightness, dot_radius in self.surface_particles:
            base = SUN_CORE if self.fixed and offset.length() < self.radius * 0.55 else self.color
            shade = tuple(max(0, min(255, int(component * brightness))) for component in base)
            pygame.draw.circle(surface, shade, self.position + offset, dot_radius)
        if self.fixed:
            pygame.draw.circle(surface, WHITE, self.position, self.radius + 3, 1)
        if self.name and font:
            label = font.render(self.name, True, WHITE)
            surface.blit(label, label.get_rect(midtop=(self.position.x, self.position.y + self.radius + 6)))
