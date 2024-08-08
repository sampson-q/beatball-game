# game.py
# Core game logic and mechanics for the Beatball Game

import pygame
import random
from sound import SoundManager
sound_manager = SoundManager()

class Game:
    def __init__(self, screen):
        """Initialize the game with the screen, paddle, ball, and game state variables."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.paddle = Paddle(self.screen_rect)
        self.ball = Ball(self.screen_rect, self.paddle)
        self.score = 0
        self.lives = 3
        self.game_over = False

    def update(self):
        """Update the game state, including ball movement and collision detection."""
        if not self.game_over:
            self.ball.update()
            self.check_collisions()
            self.check_game_over()

    def draw(self):
        """Draw the game objects onto the screen."""
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

    def move_paddle_left(self):
        """Move the paddle to the left."""
        self.paddle.move_left()

    def move_paddle_right(self):
        """Move the paddle to the right."""
        self.paddle.move_right()

    def check_collisions(self):
        """Check for collisions between the ball and the paddle or walls."""
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.bounce()
            self.score += 1
            sound_manager.play_score_sound()

    def check_game_over(self):
        """Check if the ball has fallen off the screen, resulting in a lost life."""
        if self.ball.rect.top > self.screen_rect.bottom:
            self.lives -= 1
            sound_manager.play_fall_sound()
            if self.lives > 0:
                self.ball.reset()
            else:
                self.game_over = True
                sound_manager.play_game_over_sound()

class Paddle:
    def __init__(self, screen_rect):
        """Initialize the paddle with position, size, and speed."""
        self.screen_rect = screen_rect
        self.width = 100
        self.height = 20
        self.color = (255, 255, 255)
        self.speed = 10
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = screen_rect.midbottom

    def move_left(self):
        """Move the paddle to the left."""
        if self.rect.left > 0:
            self.rect.x -= self.speed

    def move_right(self):
        """Move the paddle to the right."""
        if self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed

    def draw(self, screen):
        """Draw the paddle onto the screen."""
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self, screen_rect, paddle):
        """Initialize the ball with position, velocity, and direction."""
        self.radius = 10
        self.color = (255, 0, 0)
        self.screen_rect = screen_rect
        self.paddle = paddle
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.reset()

    def reset(self):
        """Reset the ball to the initial position above the paddle."""
        self.rect.center = self.screen_rect.center
        self.rect.y = self.paddle.rect.top - self.radius * 2
        self.velocity = [random.choice([-5, 5]), -5]

    def update(self):
        """Update the ball's position and handle collisions with the screen edges."""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.left <= 0 or self.rect.right >= self.screen_rect.right:
            self.velocity[0] = -self.velocity[0]
            sound_manager.play_bounce_sound()

        if self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]
            sound_manager.play_bounce_sound()

    def bounce(self):
        """Bounce the ball off the paddle."""
        self.velocity[1] = -self.velocity[1]

    def draw(self, screen):
        """Draw the ball onto the screen."""
        pygame.draw.ellipse(screen, self.color, self.rect)
