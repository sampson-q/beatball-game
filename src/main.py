# main.py
# entry point of the Beatball Game

import pygame, sys
from game import Game
from ui import UI

def main():
    # initialize pygame
    pygame.init()

    # set up game window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Beatball Game")

    # create game objects
    game = Game(screen)
    ui = UI(screen)

    # main game control variable
    running = True
    # clock: to manage the frame rate
    clock = pygame.time.Clock()

    # game's main loop
    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_events(event)
            if ui.state == 'playing':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.move_paddle_left()
                    elif event.key == pygame.K_RIGHT:
                        game.move_paddle_right()

        # update game state
        if ui.state == 'playing':
            # handle continuous paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game.move_paddle_left()
            if keys[pygame.K_RIGHT]:
                game.move_paddle_right()
            
            # update game objects
            game.update()
            # handle game over
            if game.game_over:
                ui.state = 'game_over'
            ui.update(game.score, game.lives)
        elif ui.state == 'game_over' and pygame.key.get_pressed()[pygame.K_RETURN]:
            # reset game state and UI
            game = Game(screen)
            ui.state = 'playing'

        # clear screen
        screen.fill((0, 0, 0))
        
        # render objects
        game.draw()
        ui.draw()

        # update game's display
        pygame.display.flip()

        # cap the frame rate to 60 fps
        clock.tick(60)

    # quit game when loop ends
    pygame.quit()

if __name__ == '__main__':
    main()