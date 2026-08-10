import pygame

from settings import (
    WIDTH,
    HEIGHT,
    DT,
    WHITE,
    SUN_MASS_MULTIPLIER
)


class Planet:

    def __init__(
        self,
        x,
        y,
        radius,
        color,
        fixed=False
    ):

        self.x = float(x)
        self.y = float(y)

        self.radius = radius
        self.color = color

        self.vx = 0.0
        self.vy = 0.0

        # -----------------------------------
        # Mass
        # -----------------------------------

        self.mass = radius ** 2

        # Sun is much more massive.
        if fixed:
            self.mass *= SUN_MASS_MULTIPLIER

        self.fixed = fixed

        # -----------------------------------
        # Trail
        # -----------------------------------

        self.trail = []

    # =======================================
    # Move Planet
    # =======================================

    def move(self):

        if self.fixed:
            return

        # Save trail position
        self.trail.append(
            (self.x, self.y)
        )

        # Limit trail length
        if len(self.trail) > 150:
            self.trail.pop(0)

        # Position update
        self.x += self.vx * DT
        self.y += self.vy * DT

    # =======================================
    # Check Outside Screen
    # =======================================

    def is_outside_screen(self):

        margin = self.radius + 50

        return (
            self.x < -margin
            or self.x > WIDTH + margin
            or self.y < -margin
            or self.y > HEIGHT + margin
        )

    # =======================================
    # Draw
    # =======================================

    def draw(self, screen):

        # -----------------------------------
        # Trail
        # -----------------------------------

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

        # -----------------------------------
        # Sun Glow
        # -----------------------------------

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

        # -----------------------------------
        # Planet
        # -----------------------------------

        pygame.draw.circle(
            screen,
            self.color,
            (
                int(self.x),
                int(self.y)
            ),
            self.radius
        )

        # -----------------------------------
        # Outline
        # -----------------------------------

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