import pygame
import sys
import math

from .Cell import Cell
from ...logic.ValidSudoku import is_valid_sudoku
from .EndGameScreen import EndGameScreen


class GameBoard:
    """
    Sudoku game board in Pygame; handles GUI, game logic, and event loop.

    Attributes:
        initial_game_grid (list): Initial Sudoku puzzle configuration
        screen_width, screen_height (int): Pygame window dimensions
        screen (pygame.Surface): Main drawing surface
        background_color (tuple): Game board background color
        font (pygame.font.Font): Text rendering font
        line_color (tuple): Grid line color
        cell_boarder_thickness (int): Grid cell border thickness
        cell_number (int): Cells per row/column in Sudoku grid
        SPACE_FOR_BUTTONS_RATIO (float): Screen portion for GUI buttons
        bottom_buttons (pygame.sprite.Group): Sprite group for GUI buttons
        cell_group (pygame.sprite.Group): Sprite group for Sudoku cells

    Methods:
        run(): Main game loop; event handling and GUI updates
        move_highlight(key): Highlight movement between cells
        draw_grid(): Draws Sudoku grid lines, GUI adjusted
    """

    def __init__(self, default_screen_width, default_screen_height, game_grid,
                 caption='Sudoku',
                 cell_number=9,
                 cell_boarder_thickness=6,
                 background_color='white',
                 line_color='black'):

        self.initial_game_grid = game_grid

        # begins pygame and screen
        pygame.init()
        self.screen_width = default_screen_width
        self.screen_height = default_screen_height
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # generates GUI
        self.background_color = background_color
        FONT_SIZE_PROPORTION = 0.05  # % of the average screen dimension
        MIN_FONT_SIZE = 1
        average_screen_dimension = (self.screen_width + self.screen_height) // 2
        font_size = max(int(average_screen_dimension * FONT_SIZE_PROPORTION), MIN_FONT_SIZE)
        self.font = pygame.font.Font(None, font_size)
        self.line_color = line_color
        self.cell_boarder_thickness = cell_boarder_thickness
        self.cell_number = cell_number

        self.SPACE_FOR_BUTTONS_RATIO = 0.1  # % percent of screen dedicated to button space

        HORIZONTAL_RATIO = self.screen_width // cell_number
        VERTICAL_RATIO = (self.screen_height - self.screen_height * self.SPACE_FOR_BUTTONS_RATIO) // cell_number

        #  makes bottom sprite group and runs the method to generate the area
        BUTTON_START_POS = default_screen_width // 4
        BUTTON_SPACING = default_screen_width // 4

        #  Creates the bottom GUI
        from .BottomButtons import generate_bottom_button_group  # Prevents circular import
        self.bottom_buttons = generate_bottom_button_group(self.screen_width,
                                                           self.screen_height,
                                                           self.SPACE_FOR_BUTTONS_RATIO,
                                                           self.font,
                                                           self.screen,
                                                           self.initial_game_grid,
                                                           BUTTON_START_POS,
                                                           BUTTON_SPACING)

        # Creates cell grid
        CELL_WIDTH = HORIZONTAL_RATIO
        CELL_HEIGHT = VERTICAL_RATIO
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

                #  Used for arrow key activation
                self.current_row = 0
                self.current_col = 0

                cells = list(self.cell_group)
                cells[0].set_active(True)

    def run(self):
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for cell in self.cell_group:
                    cell.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        self.move_highlight(event.key)

                for button in self.bottom_buttons:
                    button.handle_event(event)

                # Game Over screen
                every_celled_filled_in = all([cell.filled_in for cell in self.cell_group])
                if every_celled_filled_in:
                    game_grid = []
                    current_row = []
                    for cell in self.cell_group:
                        current_row.append(int(cell.text))

                        if len(current_row) == 9:
                            game_grid.append(current_row)
                            current_row = []

                    is_winner = is_valid_sudoku(game_grid)

                    pygame.quit()
                    game_over_screen = EndGameScreen(self.screen_width,
                                                     self.screen_height,
                                                     is_winner)

                    game_over_screen.run()

            self.screen.fill(self.background_color)

            #  updates the cell group
            self.cell_group.update()
            self.cell_group.draw(self.screen)

            # updates the grid
            self.draw_grid()

            # updates the bottom GUI
            self.bottom_buttons.update(event_list)
            self.bottom_buttons.draw(self.screen)

            pygame.display.flip()

    def move_highlight(self, key):
        # Deactivate all other cells
        for cell in self.cell_group:
            cell.set_active(False)

        if key == pygame.K_UP and self.current_row > 0:
            self.current_row -= 1
        elif key == pygame.K_DOWN and self.current_row < 8:
            self.current_row += 1
        elif key == pygame.K_LEFT and self.current_col > 0:
            self.current_col -= 1
        elif key == pygame.K_RIGHT and self.current_col < 8:
            self.current_col += 1

        cells = list(self.cell_group)
        # Activate the new cell, by finding the index of the cell
        cells[self.current_row * self.cell_number + self.current_col].set_active(True)

    def draw_grid(self):
        amount_of_lines = int(math.sqrt(self.cell_number))  # will generate sqrt of amount of cells - 1
        grid_height = self.screen_height - (self.screen_height * self.SPACE_FOR_BUTTONS_RATIO)

        # Draw vertical lines
        for i in range(1, amount_of_lines):
            pygame.draw.line(self.screen, self.line_color,
                             (i * self.screen_width // amount_of_lines, 0),
                             (i * self.screen_width // amount_of_lines, grid_height),
                             self.cell_boarder_thickness)

        # draw horizontal lines
        for i in range(1, amount_of_lines):
            pygame.draw.line(self.screen, self.line_color,
                             (0, i * grid_height // amount_of_lines),
                             (self.screen_width, i * grid_height // amount_of_lines),
                             self.cell_boarder_thickness)


