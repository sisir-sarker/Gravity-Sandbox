import pygame

class Planet:

    def __init__(self, x, y, radius, color):

        self.x = x
        self.y = y

        self.radius = radius
        self.color = color

        self.vx = 0
        self.vy = 0

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

    def move(self):

        self.x += self.vx
        self.y += self.vy