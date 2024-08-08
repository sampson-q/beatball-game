# sound.py
# Sound effects management for the Beatball Game

import pygame

class SoundManager:
    def __init__(self):
        """Initialize the SoundManager and load the sound effects."""
        pygame.mixer.init()
        self.fall_sound = pygame.mixer.Sound('assets/sounds/life.wav')
        self.score_sound = pygame.mixer.Sound('assets/sounds/score.wav')
        self.bounce_sound = pygame.mixer.Sound('assets/sounds/bounce.wav')
        self.game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')

    def play_bounce_sound(self):
        """Play the sound effect for the ball bouncing."""
        self.bounce_sound.play()

    def play_score_sound(self):
        """Play the sound effect for scoring."""
        self.score_sound.play()

    def play_game_over_sound(self):
        """Play the sound effect for game over."""
        self.game_over_sound.play()
    
    def play_fall_sound(self):
        """Play the sound effect when ball balls over"""
        self.fall_sound.play()