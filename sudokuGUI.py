import pygame
from constant import *

pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
chip_font = pygame.font.Font(None, CHIP_FONT)  # 'X' or 'O' font
font = pygame.font.Font(None, GAME_OVER_FONT)

# initialize game state
player = 1
chip = 'x'
winner = 0
game_over = False


def draw_grid():
    # draw horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * SQUARE_SIZE),
            (WIDTH, i * SQUARE_SIZE),
            LINE_WIDTH
        )

    # draw vertical lines
    for j in range(1, BOARD_COLS):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (j * SQUARE_SIZE, 0),
            (j * SQUARE_SIZE, HEIGHT),
            LINE_WIDTH
        )




screen.fill(BG_COLOR)
draw_grid()


while True:
    x = 1
    pygame.display.update()
