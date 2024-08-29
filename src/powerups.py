import pygame

# Load power-up images and resize them
def load_and_resize_image(path, size=(50, 50)):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)

# Resize dimensions for power-up images
power_up_size = (50, 50)

power_up_images = {
    "speed_boost": load_and_resize_image("assets/imgs/speed_boost.png", power_up_size),
    "shield": load_and_resize_image("assets/imgs/shield.png", power_up_size),
    "extra_life": load_and_resize_image("assets/imgs/extra_life.png", power_up_size)
}

class PowerUp:
    def __init__(self, type, position):
        self.type = type
        self.position = position
        self.image = power_up_images.get(type)
        self.rect = self.image.get_rect(topleft=position)
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def apply_effect(self):
        if self.type == "speed_boost":
            return "speed_boost"
        elif self.type == "shield":
            return "shield"
        elif self.type == "extra_life":
            return "extra_life"

    def is_expired(self, current_time, expiration_time):
        return current_time - self.spawn_time > expiration_time

    def collide_with(self, rect):
        return self.rect.colliderect(rect)
