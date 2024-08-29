# leaderboard.py

import os
import json
import pygame

LEADERBOARD_FILE = "leaderboard.json"


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    return []


def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file)


def add_score(name, score, elapsed_time):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score, "time": str(elapsed_time)})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10 scores
    save_leaderboard(leaderboard)


def display_leaderboard(screen, font):
    leaderboard = load_leaderboard()
    screen.fill((0, 0, 0))

    # Headers
    title_text = font.render("Leaderboard", True, (255, 255, 255))
    name_header = font.render("Name", True, (255, 255, 255))
    score_header = font.render("Score", True, (255, 255, 255))
    time_header = font.render("Time", True, (255, 255, 255))

    screen.blit(title_text, (400 - title_text.get_width() // 2, 50))
    screen.blit(name_header, (200, 100))
    screen.blit(score_header, (400, 100))
    screen.blit(time_header, (600, 100))

    # Display leaderboard entries
    for index, entry in enumerate(leaderboard):
        name_text = font.render(entry["name"], True, (255, 255, 255))
        score_text = font.render(str(entry["score"]), True, (255, 255, 255))
        time_text = font.render(str(entry["time"]), True, (255, 255, 255))

        screen.blit(name_text, (200, 150 + index * 30))
        screen.blit(score_text, (400, 150 + index * 30))
        screen.blit(time_text, (600, 150 + index * 30))

    # Draw the "Back to Main Menu" button
    button_font = pygame.font.SysFont("Arial", 25)
    button_text = button_font.render("Back to Main Menu", True, (0, 0, 0))
    button_rect = pygame.Rect(300, 500, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), button_rect)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                              button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    pygame.display.flip()

    # Event loop to handle button click or key press
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Return to main menu when button is clicked
            if event.type == pygame.KEYDOWN:
                return  # Return to main menu when any key is pressed
