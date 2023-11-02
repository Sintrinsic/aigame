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

    def is_alive(self):
        return self.health > 0

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def is_attacking(self, enemy):
        # Calculate direction of the enemy relative to the player
        dir_x = enemy.position[0] - self.position[0]
        dir_y = enemy.position[1] - self.position[1]
        # Calculate the angle to the enemy
        angle_to_enemy = math.degrees(math.atan2(dir_y, dir_x)) % 360
        # Calculate the difference in angle, wrapped between -180 and 180
        angle_difference = (angle_to_enemy - self.angle + 180) % 360 - 180
        # If the enemy is within 45 degrees of the player's front and close enough, it's an attack
        if -45 <= angle_difference <= 45:
            distance_to_enemy = math.sqrt(dir_x ** 2 + dir_y ** 2)
            if distance_to_enemy < self.size + enemy.size:
                return True
        return False