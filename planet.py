import pygame

from settings import WIDTH, HEIGHT, DT


class Planet:
    def __init__(self, x, y, radius, color, fixed=False):
        self.x = x
        self.y = y

        self.radius = radius
        self.color = color

        self.vx = 0
        self.vy = 0

        # Temporary mass
        self.mass = radius ** 2

        # Fixed planets do not move
        self.fixed = fixed

        # Planet Trail
        self.trail = []

    def move(self):
        if self.fixed:
            return

        # Save current position for trail
        self.trail.append((self.x, self.y))

        # Keep only last 60 positions
        if len(self.trail) > 60:
            self.trail.pop(0)

        # Position Update
        self.x += self.vx * DT
        self.y += self.vy * DT

        # ---------- Screen Boundary ----------

        # Left Wall
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx *= -0.9

        # Right Wall
        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -0.9

        # Top Wall
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy *= -0.9

        # Bottom Wall
        if self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -0.9

    def draw(self, screen):

        # Draw Trail
        for pos in self.trail:
            pygame.draw.circle(
                screen,
                (120, 120, 120),
                (int(pos[0]), int(pos[1])),
                2
            )

        # Draw Planet
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )