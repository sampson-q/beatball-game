import sys

import pygame
from src.levels import set_difficulty

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Arial", 30)
button_width, button_height = 150, 50
BUTTON_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)

def draw_menu(options, selected_option):
    screen.fill((255, 255, 255))  # Clear the screen
    menu_surface = pygame.Surface((button_width, len(options) * button_height + 20))
    menu_surface.fill((255, 255, 255))
    menu_rect = menu_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(menu_surface, menu_rect.topleft)

    for i, option in enumerate(options):
        color = BUTTON_COLOR if i != selected_option else (150, 150, 150)
        text_surface = font.render(option["text"], True, BUTTON_TEXT_COLOR)
        rect = pygame.Rect(menu_rect.x + 10, menu_rect.y + 10 + i * (button_height + 10), button_width, button_height)
        pygame.draw.rect(screen, color, rect)
        screen.blit(text_surface, (rect.x + (button_width - text_surface.get_width()) // 2,
                                   rect.y + (button_height - text_surface.get_height()) // 2))

def handle_menu_events(mouse_pos, options):
    for i, option in enumerate(options):
        rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                           SCREEN_HEIGHT // 2 - (len(options) * button_height) // 2 + i * (button_height + 10),
                           button_width, button_height)
        if rect.collidepoint(mouse_pos):
            return option["action"]
    return None

def show_menu():
    menu_options = [
        {"text": "Resume", "action": "resume"},
        {"text": "Restart", "action": "restart"},
        {"text": "Quit", "action": "quit"},
        {"text": "Main Menu", "action": "main_menu"},
    ]

    selected_option = 0
    while True:
        draw_menu(menu_options, selected_option)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                action = handle_menu_events(mouse_pos, menu_options)
                if action:
                    return action
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    action = menu_options[selected_option]["action"]
                    return action

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def show_difficulty_menu():
    difficulty_options = [
        {"text": "Easy", "action": "easy"},
        {"text": "Medium", "action": "medium"},
        {"text": "Hard", "action": "hard"}
    ]

    selected_option = 0
    while True:
        draw_menu(difficulty_options, selected_option)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                action = handle_menu_events(mouse_pos, difficulty_options)
                if action:
                    set_difficulty(action)
                    return action
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(difficulty_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    action = difficulty_options[selected_option]["action"]
                    set_difficulty(action)
                    return action

        pygame.display.flip()
        pygame.time.Clock().tick(30)
