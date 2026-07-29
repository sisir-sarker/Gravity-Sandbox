import pygame


class Planet:

    def __init__(self, x, y, radius, color, fixed=False):

        self.x = x
        self.y = y

        self.radius = radius
        self.mass = radius * radius

        self.color = color

        self.vx = 0
        self.vy = 0

        # fixed=True হলে planet নড়বে না
        self.fixed = fixed

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

    def move(self):

        if self.fixed:
            return

        self.x += self.vx
        self.y += self.vy