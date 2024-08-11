import random
import sys
import time

import pygame

from environment import (load_environment_images, set_background_images, show_environment_menu, load_ball_images,
                         show_ball_menu, balls)
from levels import difficulty_settings
from main_menu import show_main_menu
from menu import show_menu, show_difficulty_menu
from powerups import PowerUp
from leaderboard import add_score, display_leaderboard
from particles import ParticleManager, ScreenShake


# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Arial", 30)

# Load environment images and ball images
background_images = load_environment_images()
set_background_images(background_images)
ball_images = load_ball_images()

# Load life image
life_image = pygame.image.load("assets/life.png").convert_alpha()
life_image = pygame.transform.scale(life_image, (30, 30))

# Load sound effects
hit_paddle_sound = pygame.mixer.Sound("assets/sound/ball.mp3")
hit_wall_sound = pygame.mixer.Sound("assets/sound/ball_hit.mp3")
power_up_spawn_sound = pygame.mixer.Sound("assets/sound/powerups.mp3")
game_over_sound = pygame.mixer.Sound("assets/sound/game_over.mp3")
chewing_sound = pygame.mixer.Sound("assets/sound/chewing.mp3")
ball_fall_sound = pygame.mixer.Sound("assets/sound/ball_fall.mp3")

# Load background music
background_music_path = "assets/sound/background_music.mp3"
pygame.mixer.music.load(background_music_path)
pygame.mixer.music.set_volume(0.5)

hit_paddle_sound.set_volume(1.0)  # Full volume
hit_wall_sound.set_volume(1.0)  # Full volume
pygame.mixer.init(frequency=22050, size=-16, channels=2)

# Global variables
difficulty = "medium"
ball_speed_x, ball_speed_y, player_speed, player_width = (0, 0, 0, 0)
ball_pos = [0, 0]
player_pos = [0, 0]
lives = 0
paused = False
power_ups = []
power_up_types = ["speed_boost", "shield", "extra_life"]
power_up_timer = 5000
shield_active = False
score = 0

# Pause button functions
def draw_pause_button():
    pause_button_rect = pygame.Rect(SCREEN_WIDTH - 160, 10, 150, 50)
    pygame.draw.rect(screen, (200, 200, 200), pause_button_rect)
    text_surface = font.render("Pause", True, (0, 0, 0))
    screen.blit(text_surface, (pause_button_rect.x + (150 - text_surface.get_width()) // 2,
                               pause_button_rect.y + (50 - text_surface.get_height()) // 2))
    return pause_button_rect

# Reset game button functions
def reset_game():
    global ball_pos, ball_speed_x, ball_speed_y, player_pos, player_speed, player_width, lives, power_ups, score
    ball_pos = [random.randint(25, SCREEN_WIDTH - 25), SCREEN_HEIGHT // 2]
    ball_speed_x = difficulty_settings[difficulty]["ball_speed_x"]
    ball_speed_y = difficulty_settings[difficulty]["ball_speed_y"]
    player_speed = difficulty_settings[difficulty]["player_speed"]
    player_width = difficulty_settings[difficulty]["paddle_width"]
    player_pos = [SCREEN_WIDTH // 2 - player_width // 2, SCREEN_HEIGHT - 20]
    lives = 3
    power_ups = []
    score = 0

# Powerups display
def spawn_power_up():
    power_up_type = random.choice(power_up_types)
    position = [random.randint(0, SCREEN_WIDTH - 30), random.randint(0, SCREEN_HEIGHT - 30)]
    power_ups.append(PowerUp(power_up_type, position))
    power_up_spawn_sound.play()

# Timer and score
def draw_timer_and_score(start_ticks):
    current_ticks = pygame.time.get_ticks()
    seconds = (current_ticks - start_ticks) // 1000
    timer_text = font.render(f"Time: {seconds}", True, (0, 0, 0))
    screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 10))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 40))

def draw_lives(screen, lives, life_image):
    for i in range(lives):
        screen.blit(life_image, (10 + i * (life_image.get_width() + 10), 10))

def get_player_name(screen, font, screen_width, screen_height):
    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    base_font = pygame.font.SysFont(None, 48)
    prompt_text = "Enter your name"
    prompt_visible = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    prompt_visible = False
                else:
                    active = False
                    prompt_visible = True if text == '' else False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text  # Return the entered text when Enter is pressed
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    prompt_visible = False if text != '' else True

        screen.fill((0, 0, 0))

        if prompt_visible:
            txt_surface = base_font.render(prompt_text, True, (200, 200, 200))
        else:
            txt_surface = base_font.render(text, True, color)

        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

def game_loop(environment_name, ball_image):
    start_time = time.time()  # Start the timer here
    global paused, shield_active, lives, ball_speed_y, ball_speed_x, ball_pos, player_speed, score

    shield_active = False
    reset_game()

    particle_manager = ParticleManager()
    screen_shake = ScreenShake()

    # Load and scale paddle image after player_width is set
    paddle_image = pygame.image.load("assets/paddle.png").convert_alpha()
    paddle_image = pygame.transform.scale(paddle_image, (player_width, 20))

    # Load the background image for the selected environment
    background_image = background_images[environment_name]

    start_ticks = pygame.time.get_ticks()
    spawn_timer = pygame.time.get_ticks() + 15000
    power_up_expiration = 10000  # Power-up expires after 10 seconds

    # Font for power-up mess6+ages
    message_font = pygame.font.SysFont("Arial", 30)
    power_up_message = ""

    # Play background music
    pygame.mixer.music.load("assets/sound/background_music.mp3")
    pygame.mixer.music.play(-1)

    while True:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pause_button_rect.collidepoint(mouse_pos):
                    paused = not paused
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
            if event.type == pygame.USEREVENT + 1:  # Speed boost timer
                player_speed -= 5
                player_speed = max(player_speed, difficulty_settings[difficulty]["player_speed"])  # Ensure minimum speed
            if event.type == pygame.USEREVENT + 2:  # Shield timer
                shield_active = False

        # Pause menu
        if paused:
            action = show_menu()
            if action == "resume":
                paused = False
            elif action == "restart":
                reset_game()
            elif action == "quit":
                pygame.quit()
                sys.exit()
            elif action == "main_menu":
                return

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_width:
                player_pos[0] += player_speed
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= player_speed
            if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - 20:
                player_pos[1] += player_speed

            # Ensure the paddle does not go out of bounds
            player_pos[0] = max(0, min(player_pos[0], SCREEN_WIDTH - player_width))
            player_pos[1] = max(0, min(player_pos[1], SCREEN_HEIGHT - 20))

            # Update ball position
            ball_pos[0] += ball_speed_x
            ball_pos[1] += ball_speed_y
            ball_rect = pygame.Rect(ball_pos[0] - 25, ball_pos[1] - 25, 50, 50)

            # Update particles and screen shake
            particle_manager.update()
            screen_shake.update()

            # Draw everything with shake applied
            shake_x, shake_y = screen_shake.apply_shake()
            screen.blit(background_image, (shake_x, shake_y))

            # Draw the selected ball image
            screen.blit(ball_image, (ball_pos[0] - 25 + shake_x, ball_pos[1] - 25 + shake_y))

            # Draw player (paddle)
            screen.blit(paddle_image, (player_pos[0] + shake_x, player_pos[1] + shake_y))

            # Draw particles
            particle_manager.draw(screen)

            # Draw the power-up message if it exists
            if power_up_message:
                message_surface = message_font.render(power_up_message, True, (255, 255, 0))
                screen.blit(message_surface, (SCREEN_WIDTH // 2 - message_surface.get_width() // 2,
                                              SCREEN_HEIGHT // 2 - message_surface.get_height() // 2))
                if pygame.time.get_ticks() > message_timer + 2000:  # Display the message for 2 seconds
                    power_up_message = ""

            # Ball collision with walls
            wall_collision = False
            if ball_pos[0] <= 25 or ball_pos[0] >= SCREEN_WIDTH - 25:
                ball_speed_x = -ball_speed_x
                hit_wall_sound.play()  # Play wall hit sound
                score += 1  # Increase score on wall collision
                wall_collision = True

            if ball_pos[1] <= 25:
                ball_speed_y = -ball_speed_y
                hit_wall_sound.play()  # Play wall hit sound
                score += 1  # Increase score on wall collision
                wall_collision = True

            if wall_collision:
                # Start screen shake effect
                screen_shake.start_shake(5, 3)  # Adjust magnitude and duration as needed
                # Emit particles
                particle_manager.emit(ball_pos[0], ball_pos[1])

            # Ball collision with player paddle
            if (player_pos[0] < ball_pos[0] < player_pos[0] + player_width and
                    player_pos[1] < ball_pos[1] + 25 < player_pos[1] + 20):
                ball_speed_y = -ball_speed_y
                hit_paddle_sound.play()  # Play paddle hit sound
                score += 5  # Increase score on paddle collision
                # Emit particles
                particle_manager.emit(ball_pos[0], ball_pos[1])

            # Check if ball falls below the paddle
            if ball_pos[1] > SCREEN_HEIGHT:
                if shield_active:
                    # Reflect the ball back to the screen if shield is active
                    ball_speed_y = -ball_speed_y
                    ball_pos[1] = SCREEN_HEIGHT - 1  # Move the ball just above the screen
                    power_up_message = "Shield protected you!"
                    message_timer = pygame.time.get_ticks()
                else:
                    ball_fall_sound.play()  # Play ball fall sound
                    lives -= 1

                    # Reset the ball's position and speed based on the difficulty level
                    ball_pos = [random.randint(25, SCREEN_WIDTH - 25), SCREEN_HEIGHT // 2]
                    ball_speed_x = difficulty_settings[difficulty]["ball_speed_x"]
                    ball_speed_y = difficulty_settings[difficulty]["ball_speed_y"]

                    # Game over settings
                    if lives == 0:
                        screen.fill((255, 255, 255))
                        game_over_text = font.render("Game Over", True, (255, 0, 0))
                        screen.blit(game_over_text, (
                            SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
                        pygame.display.flip()
                        game_over_sound.play()  # Play game over sound
                        pygame.time.wait(3000)

                        # Calculate elapsed time
                        elapsed_time = int(time.time() - start_time)  # Time in seconds

                        # Prompt for player name
                        player_name = get_player_name(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT)
                        add_score(player_name, score, elapsed_time)
                        # Draw the scoreboard
                        display_leaderboard(screen, font)

                        return

            # Spawn power-ups
            if pygame.time.get_ticks() > spawn_timer:
                spawn_power_up()
                spawn_timer = pygame.time.get_ticks() + random.randint(10000, 20000)

            pause_button_rect = draw_pause_button()
            draw_timer_and_score(start_ticks)
            # Draw lives as images
            draw_lives(screen, lives, life_image)

            # Draw power-ups
            current_time = pygame.time.get_ticks()
            for power_up in power_ups[:]:
                power_up.draw(screen)
                if power_up.is_expired(current_time, power_up_expiration):
                    power_ups.remove(power_up)
                elif power_up.collide_with(pygame.Rect(player_pos[0], player_pos[1], player_width, 20)) or \
                        power_up.collide_with(ball_rect):
                    chewing_sound.play()
                    effect = power_up.apply_effect()
                    if effect == "speed_boost":
                        player_speed += 5
                        pygame.time.set_timer(pygame.USEREVENT + 1, power_up_timer)
                        power_up_message = "Speed increased by 5!"
                        message_timer = pygame.time.get_ticks()
                    elif effect == "shield":
                        shield_active = True
                        pygame.time.set_timer(pygame.USEREVENT + 2, power_up_timer)
                        power_up_message = "Shield activated!"
                        message_timer = pygame.time.get_ticks()
                    elif effect == "extra_life":
                        lives += 1  # Increment lives when the player picks up a life power-up
                        power_up_message = "Extra Life!"
                        message_timer = pygame.time.get_ticks()
                    power_ups.remove(power_up)

            pygame.display.flip()
            pygame.time.Clock().tick(50)

if __name__ == "__main__":
    while True:
        action = show_main_menu()
        if action == "start_game":
            environment_name = show_environment_menu(screen, font)
            if environment_name is None:
                continue

            ball_color = show_ball_menu(screen, font)
            if ball_color is None:
                continue

            selected_ball_image_path = balls[ball_color]
            selected_ball_image = pygame.image.load(selected_ball_image_path).convert_alpha()
            selected_ball_image = pygame.transform.scale(selected_ball_image, (50, 50))

            difficulty = show_difficulty_menu()
            game_loop(environment_name, selected_ball_image)

        elif action == "quit":
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

