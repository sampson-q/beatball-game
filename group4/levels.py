import pygame
import sys


difficulty_settings = {
    "easy": {"ball_speed_x": 6, "ball_speed_y": -6, "player_speed": 7, "paddle_width": 120},
    "medium": {"ball_speed_x": 9, "ball_speed_y": -10, "player_speed": 9, "paddle_width": 120},
    "hard": {"ball_speed_x": 13, "ball_speed_y": -13, "player_speed": 10, "paddle_width": 90}
}


def set_difficulty(level):
    global ball_speed_x, ball_speed_y, player_speed, player_width
    settings = difficulty_settings.get(level, difficulty_settings["medium"])
    ball_speed_x = settings["ball_speed_x"]
    ball_speed_y = settings["ball_speed_y"]
    player_speed = settings["player_speed"]
    player_width = settings["paddle_width"]

