"""Short-lived particle blast used for Sun impact effects."""

from __future__ import annotations

import random
import pygame


class Explosion:
    """A directional burst of hot debris emitted from an impact point."""

    COLORS = ((255, 245, 170), (255, 185, 50), (255, 82, 20), (210, 35, 15))

    def __init__(self, position, direction, strength):
        generator = random.Random()
        direction = pygame.Vector2(direction)
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)
        direction = direction.normalize()
        count = max(16, min(110, int(28 + strength * 150)))
        self.particles = []

        for _ in range(count):
            spread = direction.rotate(generator.uniform(-72, 72))
            speed = generator.uniform(65, 260) * (0.7 + strength)
            self.particles.append(
                [pygame.Vector2(position), spread * speed, generator.uniform(0.35, 1.15), generator.choice(self.COLORS)]
            )

    @property
    def alive(self):
        return bool(self.particles)

    def update(self, dt):
        remaining = []
        for position, velocity, life, color in self.particles:
            life -= dt
            if life <= 0:
                continue
            position += velocity * dt
            velocity *= 0.975
            remaining.append([position, velocity, life, color])
        self.particles = remaining

    def draw(self, surface):
        for position, _, life, color in self.particles:
            alpha = int(min(255, life * 255))
            radius = 1 if life < 0.45 else 2
            glow = pygame.Surface((radius * 6, radius * 6), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*color, alpha), (radius * 3, radius * 3), radius)
            surface.blit(glow, glow.get_rect(center=position))
