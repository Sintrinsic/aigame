import pygame
from player import Player
from enemy import Enemy
from healthbar import HealthBar
from random import randint
import time

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
# Set up display dimensions
WIDTH, HEIGHT = 800, 600

class Game:
    def __init__(self):
        # Initialize the player
        # Set up the display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI Game")
        # Set up a clock for managing the frame rate
        self.clock = pygame.time.Clock()
        self.reset_game()

        self.health_bar = HealthBar(10, 10, 200, 20, self.player.health, self.player.max_health)
        self.last_spawn_time = pygame.time.get_ticks()  # Store the current time
        self.spawn_interval = 1000  # 1000 milliseconds = 1 second
        self.game_over_time = 0  # When the player died

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def reset_game(self):
        # Reset all game attributes to their starting values
        self.player = Player(WIDTH // 2, HEIGHT // 2, 20, BLUE)
        self.enemies = [Enemy(randint(0, WIDTH), randint(0, HEIGHT), 15, (255, 0, 0), self.player) for _ in range(5)]
        self.game_over = False
        self.game_over_displayed = False

    def display_game_over(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.game_over_time >= 10000:  # 10 seconds in milliseconds
            self.reset_game()
        else:
            screen.fill((0, 0, 0))  # Fill the screen with black or another color
            font = pygame.font.Font(None, 74)
            text = font.render('You Died', True, (255, 0, 0))
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(text, text_rect)

            # Optional: countdown timer
            countdown_seconds = 10 - (current_time - self.game_over_time) // 1000
            countdown_text = font.render(f'Restarting in: {countdown_seconds}', True, (255, 255, 255))
            countdown_rect = countdown_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))
            screen.blit(countdown_text, countdown_rect)

            pygame.display.flip()  # Update the screen with what we've drawn

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
        if not self.game_over:
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
                        self.player.take_damage(self.player.max_health * 0.5)  # Player takes 10% health damage
                        self.enemies.remove(enemy)  # Remove the enemy that collided with the player
            # Update health bar
            self.health_bar.health = self.player.health
            if not self.player.is_alive():
                self.game_over = True
                self.game_over_time = time.time()
        else:
            current_time = time.time()
            if current_time - self.game_over_time >= 1:
                self.reset_game()
            else:
                pass #self.display_game_over(self.screen)  # Pass your pygame screen object here

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
