import pygame
import sys

from .cell import Cell
from ...game_logic.ValidSudoku import is_valid_sudoku
from .winLose import EndGameScreen

class GameBoard:
    def __init__(self, default_screen_width, default_screen_height, game_grid,
                 caption='Sudoku',
                 cell_number=9,
                 cell_boarder_thickness=6,
                 background_color='white'):

        self.initial_game_grid = game_grid

        pygame.init()
        self.screen_width = default_screen_width
        self.screen_height = default_screen_height
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.background_color = background_color

        FONT_SIZE_PROPORTION = 0.05  # % of the average screen dimension
        MIN_FONT_SIZE = 1

        average_screen_dimension = (self.screen_width + self.screen_height) // 2
        font_size = max(int(average_screen_dimension * FONT_SIZE_PROPORTION), MIN_FONT_SIZE)
        self.font = pygame.font.Font(None, font_size)

        HORIZONTAL_RATIO = self.screen_width // cell_number
        VERTICAL_RATIO = (self.screen_height - 150) // cell_number  # adds space to bottom for GUI

        CELL_WIDTH = HORIZONTAL_RATIO - cell_boarder_thickness
        CELL_HEIGHT = VERTICAL_RATIO - cell_boarder_thickness
        CELL_PARAMETERS = (CELL_WIDTH, CELL_HEIGHT, self.font, self.screen,)

        self.cell_group = pygame.sprite.Group()
        # Create a cell for each position in the grid
        for y, row in enumerate(game_grid):
            for x, number in enumerate(row):
                cell_x_pos = x * HORIZONTAL_RATIO
                cell_y_pos = y * VERTICAL_RATIO

                if number != 0 and number is not None:
                    text = str(number)
                    cell = Cell(cell_x_pos, cell_y_pos, True, text, *CELL_PARAMETERS)

                else:
                    text = ''
                    cell = Cell(cell_x_pos, cell_y_pos, False, text, *CELL_PARAMETERS)

                self.cell_group.add(cell)

    def run(self):
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for cell in self.cell_group:
                    cell.handle_event(event)

                every_celled_filled_in = all([cell.filled_in for cell in self.cell_group])

                if every_celled_filled_in:
                    game_grid = []
                    current_row = []
                    for cell in self.cell_group:
                        current_row.append(int(cell.text))

                        if len(current_row) == 9:
                            game_grid.append(current_row)
                            current_row = []  # Reset current_row here

                    is_winner = is_valid_sudoku(game_grid)

                    pygame.quit()
                    game_over_screen = EndGameScreen(self.screen_width,
                                                     self.screen_height,
                                                     is_winner,
                                                     self.initial_game_grid)

                    game_over_screen.run()

            self.cell_group.update()
            self.screen.fill(self.background_color)
            self.cell_group.draw(self.screen)

            pygame.display.flip()
