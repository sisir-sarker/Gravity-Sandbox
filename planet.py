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

        # Bigger planets become much heavier
        self.mass = radius ** 2

        self.fixed = fixed

        # Orbit Trail
        self.trail = []

    # ----------------------------
    # Movement
    # ----------------------------
    def move(self):

        if self.fixed:
            return

        # Save Trail
        self.trail.append((self.x, self.y))

        if len(self.trail) > 80:
            self.trail.pop(0)

        # Position Update
        self.x += self.vx * DT
        self.y += self.vy * DT

        # ----------------------------
        # Screen Boundary
        # ----------------------------

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx *= -0.9

        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -0.9

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy *= -0.9

        if self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -0.9

    # ----------------------------
    # Draw
    # ----------------------------
    def draw(self, screen):

        # ---------- Trail ----------
        for i, pos in enumerate(self.trail):

            size = max(1, i // 25 + 1)

            pygame.draw.circle(
                screen,
                (90, 90, 90),
                (int(pos[0]), int(pos[1])),
                size
            )

        # ---------- Sun Glow ----------
        if self.fixed:

            pygame.draw.circle(
                screen,
                (255, 170, 0),
                (int(self.x), int(self.y)),
                self.radius + 12,
                2
            )

            pygame.draw.circle(
                screen,
                (255, 210, 0),
                (int(self.x), int(self.y)),
                self.radius + 6,
                2
            )

        # ---------- Planet ----------
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

        # ---------- Outline ----------
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.x), int(self.y)),
            self.radius,
            1
        )