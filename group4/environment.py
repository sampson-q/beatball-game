import sys
import pygame

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Environment themes
environments = {
    "forest": {
        "background_color": (34, 139, 34),  # Forest green
        "background_image": "assets/forest.jpg"
    },
    "desert": {
        "background_color": (210, 180, 140),  # Tan
        "background_image": "assets/desert.jpg"
    },
    "space": {
        "background_color": (0, 0, 0),  # Black
        "background_image": "assets/space.jpg"
    }
}

# Ball options
balls = {
    "basketball": "assets/bball.png",
    "football": "assets/fball.png",
    "designed": "assets/sball.png",
    "gold": "assets/sgball.png"
}


def load_environment_images():
    images = {}
    for theme, props in environments.items():
        try:
            image = pygame.image.load(props["background_image"]).convert()
            image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            images[theme] = image
        except pygame.error as e:
            print(f"Error loading image {props['background_image']}: {e}")
            images[theme] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create a blank surface as fallback
    return images


def load_ball_images():
    images = {}
    for color, path in balls.items():
        try:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (50, 50))
            images[color] = image
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            images[color] = pygame.Surface((50, 50))  # Create a blank surface as fallback
    return images


def set_background_images(images):
    global background_images
    background_images = images


def show_environment_menu(screen, font):
    environment_options = list(background_images.keys())
    selected_environment = None

    while True:
        screen.fill((255, 255, 255))
        title = font.render("Select Environment", True, (0, 0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, environment in enumerate(environment_options):
            color = (0, 0, 0)
            text = font.render(environment, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150 + i * 50))

        # Return button
        return_button = font.render("Return", True, (255, 0, 0))
        return_button_rect = return_button.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(return_button, return_button_rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if Return button was clicked
                if return_button_rect.collidepoint(mouse_pos):
                    return None

                for i, environment in enumerate(environment_options):
                    text_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 150 + i * 50, 200, 50)
                    if text_rect.collidepoint(mouse_pos):
                        selected_environment = environment
                        return selected_environment


def show_ball_menu(screen, font):
    menu_running = True
    selected_ball = None

    while menu_running:
        screen.fill((255, 255, 255))
        title_text = font.render("Select Ball", True, (0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        y_offset = 120
        for color, image_path in balls.items():
            ball_image = pygame.image.load(image_path).convert_alpha()
            ball_image = pygame.transform.scale(ball_image, (50, 50))
            screen.blit(ball_image, (SCREEN_WIDTH // 2 - 25, y_offset))
            ball_text = font.render(color.capitalize(), True, (0, 0, 0))
            ball_rect = ball_text.get_rect(center=(SCREEN_WIDTH // 3, y_offset + 20))
            pygame.draw.rect(screen, (200, 200, 255), ball_rect.inflate(20, 10))  # Button background color
            screen.blit(ball_text, ball_rect)
            y_offset += 70

        # Add a "Return" button
        return_button_text = font.render("Return", True, (255, 0, 0))
        return_button_rect = return_button_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 50))
        pygame.draw.rect(screen, (200, 200, 255), return_button_rect.inflate(20, 10))  # Button background color
        screen.blit(return_button_text, return_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                y_offset = 150
                for color, _ in balls.items():
                    ball_rect = pygame.Rect(SCREEN_WIDTH // 2 - 10, y_offset - 20, 100, 40)
                    if ball_rect.collidepoint(mouse_pos):
                        selected_ball = color
                        print(f"Selected ball: {selected_ball}")  # Debug print
                        menu_running = False
                        break
                    y_offset += 70
                # Check if the "Return" button was clicked
                if return_button_rect.collidepoint(mouse_pos):
                    return None

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    return selected_ball
