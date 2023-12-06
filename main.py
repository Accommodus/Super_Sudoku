import pygame
import math

from backend.graphics.start_menu.StartMenu import StartMenu
from backend.graphics.game_board.sudokuGUI import GameBoard
from backend.game_logic.sudoku_generator import generate_sudoku

if __name__ == '__main__':
    menu = StartMenu(500, 500)
    menu.run()
