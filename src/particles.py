# particles.py
import pygame
import random


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.color = (255, 255, 255)  # White particles
        self.lifetime = random.randint(20, 40)
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_alive(self):
        return self.lifetime > 0


class ParticleManager:
    def __init__(self):
        self.particles = []

    def emit(self, x, y):
        for _ in range(20):  # Emit 20 particles for each collision
            self.particles.append(Particle(x, y))

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)


class ScreenShake:
    def __init__(self):
        self.shake_duration = 0
        self.magnitude = 0

    def start_shake(self, duration, magnitude):
        self.shake_duration = duration
        self.magnitude = magnitude

    def update(self):
        if self.shake_duration > 0:
            self.shake_duration -= 1

    def apply_shake(self):
        if self.shake_duration > 0:
            return random.randint(-self.magnitude, self.magnitude), random.randint(-self.magnitude, self.magnitude)
        return 0, 0


class BackgroundAnimation:
    def __init__(self, screen_width, screen_height):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 1  # Speed of background movement

    def update(self):
        self.x += self.speed
        if self.x > self.screen_width:
            self.x = 0

    def draw(self, screen):
        screen.blit(background_image, (-self.x, 0))
        screen.blit(background_image, (self.screen_width - self.x, 0))
