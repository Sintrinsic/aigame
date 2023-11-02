import math
import pygame
from random import randint

ENEMY_SPEED = 2

class Enemy:
    def __init__(self, x, y, size, color, target):
        self.position = [x, y]
        self.size = size
        self.color = color
        self.target = target  # The target (player) the enemy will move towards

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.size)

    def update(self, enemies):
        # Calculate direction towards the player
        dir_x = self.target.position[0] - self.position[0]
        dir_y = self.target.position[1] - self.position[1]
        # Normalize the direction
        distance = math.sqrt(dir_x ** 2 + dir_y ** 2)
        dir_x, dir_y = dir_x / distance, dir_y / distance
        # Move towards the player
        self.position[0] += dir_x * ENEMY_SPEED
        self.position[1] += dir_y * ENEMY_SPEED
        separation_force = self.separate(enemies)
        self.position[0] += separation_force[0]
        self.position[1] += separation_force[1]

    def is_colliding_with_player(self, player):
        # Simple collision detection
        distance = math.sqrt((self.position[0] - player.position[0]) ** 2 + (self.position[1] - player.position[1]) ** 2)
        return distance < self.size + player.size

    def separate(self, enemies):
        separation_radius = 30  # Adjust as needed for 'personal space'
        separation_force = [0, 0]
        for other in enemies:
            if other is not self:
                dx = self.position[0] - other.position[0]
                dy = self.position[1] - other.position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < separation_radius:
                    # Calculate vector pointing away from the neighbor
                    separation_force[0] += dx
                    separation_force[1] += dy

        # Normalize the separation force and scale it if necessary
        magnitude = math.sqrt(separation_force[0] ** 2 + separation_force[1] ** 2)
        if magnitude > 0:
            separation_force[0] /= magnitude
            separation_force[1] /= magnitude

            # Optionally scale the force if you want a stronger or weaker effect
            separation_force[0] *= 1  # Adjust scaling factor as necessary
            separation_force[1] *= 1  # Adjust scaling factor as necessary

        return separation_force