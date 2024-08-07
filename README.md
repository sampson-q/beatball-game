# beatball-game
> Computer Graphics Project

## Introduction
> Beatball Game is an interactive 2D game developed using Python and Pygame. The objective of the game is to prevent the ball from falling off the screen by strategically moving the paddle to bounce it back. The game features a single-player mode with increasing difficulty levels, simple 2D graphics, and engaging gameplay.

## Objectives
>1. Develop a 2D game using Python and Pygame.
>2. Implement game mechanics such as ball movement, collision detection, and scoring.
>3. Design an intuitive and user-friendly interface.
>4. Provide an engaging and fun gameplay experience.

## Features
>- Single-player mode with increasing difficulty levels.
>- Realistic ball movement and collision physics.
>- User-friendly interface including start screen, game screen, and game over screen.
>- Sound effects for ball bounce and scoring.

## Installation
>To run the Beatball Game, you need to have Python and Pygame installed on your system.
1. **Clone the Repository**
   ```
   git clone https://github.com/sampson-q/beatball-game.git
   cd beatball-game
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

## How to Play
1. Run the game using the following command:
   ```
   python src/main.py
   ```
2. Use the arrow keys to move the paddle left and right.
3. Prevent the ball from falling off the bottom of the screen by bouncing it back with the paddle.
4. The game gets progressively harder as you score more points.

## Project Structure
```
beatball-game/
├── assets/
├── docs/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── game.py
│   ├── ui.py
│   ├── sound.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Stucture Details
>1. **assets/**: Contains images, sounds, and other game assets.
>2. **docs/**: Contains project documentation.
>3. **src/**: Contains the source code for the game.
>>  - **main.py**: Entry point of the game.
>>  - **game.py**: Core game logic and mechanics.
>>  - **ui.py**: User interface elements.
>>  - **sound.py**: Sound effects management.
>4. **tests/**: Contains unit tests and other test scripts.
>5. **.gitignore**: Specifies files and directories to be ignored by Git.
>6. **README.md**: Project overview and instructions.
>7. **requirements.txt**: List of dependencies required to run the game.

## Acknowledgements
- Thanks to the Pygame community for their excellent documentation and support.
- Inspired by classic games like Pong and Breakout.