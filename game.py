import pygame
from player import Player
from enemy import Enemy
from healthbar import HealthBar
from random import randint

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
# Set up display dimensions
WIDTH, HEIGHT = 800, 600

class Game:
    def __init__(self):
        # Initialize the player
        self.player = Player(WIDTH // 2, HEIGHT // 2, 20, BLUE)
        # Set up the display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI Game")
        # Set up a clock for managing the frame rate
        self.clock = pygame.time.Clock()
        self.enemies = [Enemy(randint(0, WIDTH), randint(0, HEIGHT), 15, (255, 0, 0), self.player) for _ in range(5)]
        self.health_bar = HealthBar(10, 10, 200, 20, self.player.health, self.player.max_health)
        self.last_spawn_time = pygame.time.get_ticks()  # Store the current time
        self.spawn_interval = 1000  # 1000 milliseconds = 1 second

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def process_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move_forward()
        if keys[pygame.K_s]:
            self.player.move_backward()
        if keys[pygame.K_a]:
            self.player.rotate_left()
        if keys[pygame.K_d]:
            self.player.rotate_right()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_enemy()
            self.last_spawn_time = current_time
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.enemies)
            if enemy.is_colliding_with_player(self.player):
                # Check if the player is hitting the enemy with the front "spike"
                if self.player.is_attacking(enemy):
                    self.enemies.remove(enemy)
                    self.player.heal(1)  # Heal the player when they defeat an enemy
                else:
                    self.player.take_damage(self.player.health * 0.1)  # Player takes 10% health damage
                    self.enemies.remove(enemy)  # Remove the enemy that collided with the player
        # Update health bar
        self.health_bar.health = self.player.health

    def render(self):
        # Fill the screen with a white background
        self.screen.fill(WHITE)
        # Draw the player
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.health_bar.draw(self.screen)
        # Flip the display buffers to render the next frame
        pygame.display.flip()

    def spawn_enemy(self):
        # Create a new enemy and add it to the enemies list
        new_enemy = Enemy(randint(0, WIDTH - 20), randint(0, HEIGHT - 20), 15, (255, 0, 0), self.player)
        self.enemies.append(new_enemy)
    def run(self):
        running = True
        while running:
            # Handle any events, like input or window closing
            running = self.handle_events()
            # Handle player input
            self.process_input()
            # Update game state
            self.update()
            # Render the new frame
            self.render()
            # Cap the frame rate to 30 frames per second
            self.clock.tick(30)

        pygame.quit()

# The actual game loop and other methods would be here
