# main_menu.py
import pygame
from src.leaderboard import display_leaderboard

def show_main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Arial", 30)

    while True:
        screen.fill((255, 255, 255))
        start_button = pygame.Rect(325, 150, 150, 50)
        leaderboard_button = pygame.Rect(325, 250, 150, 50)
        quit_button = pygame.Rect(325, 350, 150, 50)

        pygame.draw.rect(screen, (200, 200, 200), start_button)
        pygame.draw.rect(screen, (200, 200, 200), leaderboard_button)
        pygame.draw.rect(screen, (200, 200, 200), quit_button)

        start_text = font.render("Start Game", True, (0, 0, 0))
        leaderboard_text = font.render("Leaderboard", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))

        screen.blit(start_text, (start_button.x + (150 - start_text.get_width()) // 2,
                                 start_button.y + (50 - start_text.get_height()) // 2))
        screen.blit(leaderboard_text, (leaderboard_button.x + (150 - leaderboard_text.get_width()) // 2,
                                       leaderboard_button.y + (50 - leaderboard_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (150 - quit_text.get_width()) // 2,
                                quit_button.y + (50 - quit_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return "start_game"
                if leaderboard_button.collidepoint(mouse_pos):
                    display_leaderboard(screen, font)  # Display the leaderboard
                if quit_button.collidepoint(mouse_pos):
                    return "quit"