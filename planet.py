import pygame

from settings import WIDTH, HEIGHT, DT, WHITE


class Planet:

    def __init__(
        self,
        x,
        y,
        radius,
        color,
        fixed=False
    ):

        self.x = x
        self.y = y

        self.radius = radius
        self.color = color

        self.vx = 0.0
        self.vy = 0.0

        # Mass depends on radius
        self.mass = radius ** 2

        # Fixed objects do not move
        self.fixed = fixed

        # Trail
        self.trail = []

    # ===================================
    # Move Planet
    # ===================================

    def move(self):

        if self.fixed:
            return

        # Save trail position
        self.trail.append(
            (self.x, self.y)
        )

        # Limit trail length
        if len(self.trail) > 120:
            self.trail.pop(0)

        # Update position
        self.x += self.vx * DT
        self.y += self.vy * DT

        # ===================================
        # Boundary Bounce
        # ===================================

        if self.x - self.radius <= 0:

            self.x = self.radius
            self.vx *= -0.9

        elif self.x + self.radius >= WIDTH:

            self.x = WIDTH - self.radius
            self.vx *= -0.9

        if self.y - self.radius <= 0:

            self.y = self.radius
            self.vy *= -0.9

        elif self.y + self.radius >= HEIGHT:

            self.y = HEIGHT - self.radius
            self.vy *= -0.9

    # ===================================
    # Draw
    # ===================================

    def draw(self, screen):

        # =================================
        # Draw Trail
        # =================================

        for position in self.trail:

            pygame.draw.circle(
                screen,
                (70, 70, 70),
                (
                    int(position[0]),
                    int(position[1])
                ),
                1
            )

        # =================================
        # Draw Sun Glow
        # =================================

        if self.fixed:

            pygame.draw.circle(
                screen,
                (255, 180, 0),
                (
                    int(self.x),
                    int(self.y)
                ),
                self.radius + 10,
                2
            )

        # =================================
        # Draw Planet
        # =================================

        pygame.draw.circle(
            screen,
            self.color,
            (
                int(self.x),
                int(self.y)
            ),
            self.radius
        )

        # =================================
        # Draw Outline
        # =================================

        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(self.x),
                int(self.y)
            ),
            self.radius,
            1
        )