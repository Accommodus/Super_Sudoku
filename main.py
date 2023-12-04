from graphics import start_menu
from graphics.game_board import sudokuGUI
import pygame


def start_easy(menu):
    pygame.quit()
    board = sudokuGUI.GameBoard(menu.screen_width, menu.screen_height, 10)
    board.run()


def start_medium(menu):
    pygame.quit()
    board = sudokuGUI.GameBoard(menu.screen_width, menu.screen_height, 20)
    board.run()


def start_hard(menu):
    pygame.quit()
    board = sudokuGUI.GameBoard(menu.screen_width, menu.screen_height, 30)
    board.run()


# {"menu_label": menu_function}
start_menu_options = {
            "Easy": lambda: start_easy(menu),
            "Medium": lambda: start_medium(menu),
            "Hard": lambda: start_hard(menu)
        }

if __name__ == '__main__':
    menu = start_menu.StartMenu(500, 500, start_menu_options)
    menu.run()
