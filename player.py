import math
import pygame

# Constants for the player's movement
PLAYER_SPEED = 5
ROTATION_SPEED = 5

class Player:
    def __init__(self, x, y, size, color):
        self.position = [x, y]
        self.size = size
        self.color = color
        self.angle = 0
        self.health = 100
        self.max_health = 100
        self.attack_distance = size * 10  # Adjust as needed
        self.attack_angle = 75  # Adjust as needed, smaller values result in a narrower attack zone

    def draw(self, surface):
        # Create a triangle for the player with a "nose" to indicate direction
        points = [
            (self.position[0] + self.size * math.cos(math.radians(self.angle)),
             self.position[1] + self.size * math.sin(math.radians(self.angle))),
            (self.position[0] - self.size * math.cos(math.radians(self.angle + 120)),
             self.position[1] - self.size * math.sin(math.radians(self.angle + 120))),
            (self.position[0] - self.size * math.cos(math.radians(self.angle - 120)),
             self.position[1] - self.size * math.sin(math.radians(self.angle - 120))),
        ]
        pygame.draw.polygon(surface, self.color, points)

    def move_forward(self):
        # Update the position based on the angle and speed
        self.position[0] += PLAYER_SPEED * math.cos(math.radians(self.angle))
        self.position[1] += PLAYER_SPEED * math.sin(math.radians(self.angle))

    def move_backward(self):
        # Update the position based on the angle and speed, in reverse
        self.position[0] -= PLAYER_SPEED * math.cos(math.radians(self.angle))
        self.position[1] -= PLAYER_SPEED * math.sin(math.radians(self.angle))

    def rotate_left(self):
        self.angle = (self.angle - ROTATION_SPEED) % 360

    def rotate_right(self):
        self.angle = (self.angle + ROTATION_SPEED) % 360

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100  # Cap the player's health at 100%
    def is_alive(self):
        return self.health > 0

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health


    def point_in_triangle(self, pt, v1, v2, v3):
        # Barycentric technique to check if point is inside the triangle
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(pt, v1, v2) < 0.0
        b2 = sign(pt, v2, v3) < 0.0
        b3 = sign(pt, v3, v1) < 0.0

        return (b1 == b2) and (b2 == b3)

    def is_attacking(self, enemy):
        # Define the vertices of the triangle (attack zone) in front of the player
        front_tip = (
            self.position[0] + math.cos(math.radians(self.angle)) * self.attack_distance,
            self.position[1] + math.sin(math.radians(self.angle)) * self.attack_distance
        )
        left_vertex = (
            self.position[0] + math.cos(math.radians(self.angle - self.attack_angle)) * self.size,
            self.position[1] + math.sin(math.radians(self.angle - self.attack_angle)) * self.size
        )
        right_vertex = (
            self.position[0] + math.cos(math.radians(self.angle + self.attack_angle)) * self.size,
            self.position[1] + math.sin(math.radians(self.angle + self.attack_angle)) * self.size
        )

        # Calculate the vertices of the enemy's bounding box
        enemy_corners = [
            (enemy.position[0] - enemy.size / 2, enemy.position[1] - enemy.size / 2),
            (enemy.position[0] + enemy.size / 2, enemy.position[1] - enemy.size / 2),
            (enemy.position[0] + enemy.size / 2, enemy.position[1] + enemy.size / 2),
            (enemy.position[0] - enemy.size / 2, enemy.position[1] + enemy.size / 2),
        ]

        # Check if any of the enemy's corners are in the player's attack zone
        for corner in enemy_corners:
            if self.point_in_triangle(corner, front_tip, left_vertex, right_vertex):
                return True

        return False