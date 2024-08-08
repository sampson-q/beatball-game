# ui.py
# User Interface elements for the Beatball Game

import pygame
import sys

class UI:
    def __init__(self, screen):
        """Initialize the UI with the screen and set up fonts and colors."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0)
        }
        self.state = 'start'  # possible states: start, playing, game_over

    def update(self, score, lives):
        """Update the UI elements based on the game state."""
        self.score = score
        self.lives = lives

    def draw(self):
        """Draw the UI elements based on the game state."""
        if self.state == 'start':
            self.draw_start_screen()
        elif self.state == 'playing':
            self.draw_game_screen()
        elif self.state == 'game_over':
            self.draw_game_over_screen()

    def draw_start_screen(self):
        """Draw the start screen with game title and instructions."""
        self.screen.fill(self.colors['black'])
        title = self.title_font.render('Beatball Game', True, self.colors['white'])
        instructions = self.font.render('Press ENTER to Start', True, self.colors['white'])
        self.screen.blit(title, title.get_rect(center=self.screen_rect.center))
        self.screen.blit(instructions, instructions.get_rect(midtop=(self.screen_rect.centerx, self.screen_rect.centery + 50)))
        pygame.display.flip()

    def draw_game_screen(self):
        """Draw the game screen with score and lives."""
        score_text = self.font.render(f'Score: {self.score}', True, self.colors['white'])
        lives_text = self.font.render(f'Lives: {self.lives}', True, self.colors['white'])
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (self.screen_rect.width - 120, 10))

    def draw_game_over_screen(self):
        """Draw the game over screen with final score and restart instructions."""
        self.screen.fill(self.colors['black'])
        game_over_text = self.title_font.render('Game Over', True, self.colors['red'])
        final_score_text = self.font.render(f'Final Score: {self.score}', True, self.colors['white'])
        restart_text = self.font.render('Press ENTER to Restart or ESC to Quit', True, self.colors['white'])
        self.screen.blit(game_over_text, game_over_text.get_rect(center=self.screen_rect.center))
        self.screen.blit(final_score_text, final_score_text.get_rect(midtop=(self.screen_rect.centerx, self.screen_rect.centery + 50)))
        self.screen.blit(restart_text, restart_text.get_rect(midtop=(self.screen_rect.centerx, self.screen_rect.centery + 100)))
        pygame.display.flip()

    def handle_events(self, event):
        """Handle UI-related events, such as key presses."""
        if self.state == 'start':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'playing'
        elif self.state == 'game_over':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = 'start'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        elif self.state == 'playing':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'game_over'
