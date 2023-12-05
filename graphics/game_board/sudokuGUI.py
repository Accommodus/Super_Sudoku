import pygame
import sys
from .constant import *
from .cell import Cell


class GameBoard:
    def __init__(self, default_screen_width, default_screen_height, game_grid,
                 caption='Sudoku',
                 cell_number=9,
                 cell_boarder_thickness=2):

        pygame.init()
        self.screen_width = default_screen_width
        self.screen_height = default_screen_height
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.font = pygame.font.Font(None, CHIP_FONT)  # Adjust the font size if necessary

        HORIZONTAL_RATIO = self.screen_width // cell_number
        VERTICAL_RATIO = self.screen_height // cell_number

        CELL_WIDTH = HORIZONTAL_RATIO - cell_boarder_thickness
        CELL_HEIGHT = VERTICAL_RATIO - cell_boarder_thickness
        CELL_PARAMETERS = (CELL_WIDTH, CELL_HEIGHT, self.font, 'yellow', self.screen,)

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
            self.screen.fill('white')
            self.cell_group.draw(self.screen)

            pygame.display.flip()

    def draw_grid(self):
        # draw horizontal lines

        LINE_HEIGHT = self.screen_height
        SQUARE_WIDTH = self.screen_width // 18
        SQUARE_HEIGHT = self.screen_height // 18

        for i in range(1, BOARD_ROWS):

            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, i * SQUARE_HEIGHT),
                (LINE_HEIGHT, i * SQUARE_HEIGHT),
                LINE_WIDTH
            )

        # draw vertical lines
        LINE_LENGTH = self.screen_width
        for j in range(1, BOARD_COLS):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (j * SQUARE_WIDTH, 0),
                (j * SQUARE_WIDTH, LINE_LENGTH),
                LINE_WIDTH
            )

    def draw_numbers(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                value = self.game_grid[row][col]

                if value:
                    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE + SQUARE_SIZE // 2

                    number_text = self.font.render(str(value), True, 'black')
                    number_rect = number_text.get_rect(center=(x, y))
                    self.screen.blit(number_text, number_rect)

