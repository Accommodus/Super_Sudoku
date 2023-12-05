from graphics.start_menu.StartMenu import StartMenu
from graphics.game_board.sudokuGUI import GameBoard
from game_logic.sudoku_generator import generate_sudoku
import pygame


def start_easy(screen_width, screen_height):
    pygame.quit()

    game_grid = generate_sudoku(9, 10)

    board = GameBoard(screen_width, screen_height, game_grid)
    board.run()


def start_medium(screen_width, screen_height):
    pygame.quit()

    game_grid = generate_sudoku(9, 20)

    board = GameBoard(screen_width, screen_height, game_grid)
    board.run()


def start_hard(screen_width, screen_height):
    pygame.quit()

    game_grid = generate_sudoku(9, 30)

    board = GameBoard(screen_width, screen_height, game_grid)
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
