from graphics.start_menu.StartMenu import StartMenu
from graphics.game_board import sudokuGUI
import pygame


def start_easy(screen_width, screen_height):
    pygame.quit()
    board = sudokuGUI.GameBoard(screen_width, screen_height, 10)
    board.run()


def start_medium(screen_width, screen_height):
    pygame.quit()
    board = sudokuGUI.GameBoard(screen_width, screen_height, 10)
    board.run()


def start_hard(screen_width, screen_height):
    pygame.quit()
    board = sudokuGUI.GameBoard(screen_width, screen_height, 10)
    board.run()


# {"menu_label": menu_function}
start_menu_options = {
            "Easy": start_easy,
            "Medium": start_medium,
            "Hard": start_hard
        }

if __name__ == '__main__':
    menu = StartMenu(500, 500, start_menu_options)
    menu.run()
