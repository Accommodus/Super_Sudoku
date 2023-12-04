import pygame
import sys
from .constant import *


class GameBoard:
    def __init__(self, default_screen_width, default_screen_height, caption='Sudoku'):
        pygame.init()
        self.screen_width = default_screen_width
        self.screen_height = default_screen_height
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.chip_font = pygame.font.Font(None, CHIP_FONT)  # 'X' or 'O' font
        self.font = pygame.font.Font(None, GAME_OVER_FONT)

        #  Game stats
        self.chip = 'x'
        self.winner = 0
        self.game_over = False

        #  initialize the game screen
        self.screen.fill(BG_COLOR)
        self.draw_grid()

    def run(self):
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

    def draw_grid(self):
        # draw horizontal lines
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, i * SQUARE_SIZE),
                (WIDTH, i * SQUARE_SIZE),
                LINE_WIDTH
            )

        # draw vertical lines
        for j in range(1, BOARD_COLS):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (j * SQUARE_SIZE, 0),
                (j * SQUARE_SIZE, HEIGHT),
                LINE_WIDTH
            )
