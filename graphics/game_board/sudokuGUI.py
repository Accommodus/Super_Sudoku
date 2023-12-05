import pygame
import sys
from .constant import *
from .cell import Cell


class GameBoard:
    def __init__(self, default_screen_width, default_screen_height, game_grid,
                 caption='Sudoku',
                 cell_number=9,
                 cell_boarder_thickness=6):

        pygame.init()
        self.screen_width = default_screen_width
        self.screen_height = default_screen_height + 70
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.font = pygame.font.Font(None, CHIP_FONT)

        HORIZONTAL_RATIO = self.screen_width // cell_number
        VERTICAL_RATIO = self.screen_height // cell_number

        CELL_WIDTH = HORIZONTAL_RATIO - cell_boarder_thickness
        CELL_HEIGHT = VERTICAL_RATIO - cell_boarder_thickness
        CELL_PARAMETERS = (CELL_WIDTH, CELL_HEIGHT, self.font, 'green', self.screen,)

        self.cell_group = pygame.sprite.Group()

        # Create a cell for each position in the grid
        for x in range(cell_number):
            for y in range(cell_number):
                cell_x_pos = x * HORIZONTAL_RATIO
                cell_y_pos = y * VERTICAL_RATIO
                cell = Cell(cell_x_pos, cell_y_pos, *CELL_PARAMETERS)
                self.cell_group.add(cell)

        self.screen.fill(BG_COLOR)

        #  Game stats
        self.game_grid = game_grid
        self.chip = 'x'
        self.winner = 0
        self.game_over = False

        #  initialize the game screen
        self.screen.fill(BG_COLOR)

    def run(self):
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.cell_group.update()
            self.screen.fill(BG_COLOR)
            self.cell_group.draw(self.screen)

            pygame.display.flip()

