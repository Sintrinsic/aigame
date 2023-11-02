import pygame

class HealthBar:
    def __init__(self, x, y, width, height, health, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = max_health

    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # Draw health
        health_width = (self.health / self.max_health) * self.width
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, health_width, self.height))