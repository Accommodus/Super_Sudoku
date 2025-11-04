import sys
import pygame
from .TextBox import TextBox
from .MenuOption import MenuOption
from ...logic.sudoku_generator import generate_sudoku
from ..board.GameBoard import GameBoard


class StartMenu:
    """
    Manages the overall game menu

    Attributes:
    - screen_width: The width of the screen
    - screen_height: The height of the screen
    - screen: The main Pygame screen for rendering
    - font: font for menu items
    - bold_font: A bold font for highlighted menu items
    - menu_options: group containing all menu options and text boxes
    - error_message: A string to display error messages
    - start_menu_options: str and function to call in start game menu

    Methods:
    - create_menu_option(): Creates and adds a new menu option
    - apply_screen_size(): Handles the resizing of the screen
    - run(): The main loop
    - start_easy()/medium()/hard(): methods for different menu actions
    - quit_game(): method to handle game quitting action
    """

    def __init__(self, default_screen_width, default_screen_height):
        self.screen_width = default_screen_width
        self.screen_height = default_screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.font.init()
        FONT_SIZE_PROPORTION = 0.1  # % of the average screen dimension
        MIN_FONT_SIZE = 1

        average_screen_dimension = (self.screen_width + self.screen_height) // 2
        font_size = max(int(average_screen_dimension * FONT_SIZE_PROPORTION), MIN_FONT_SIZE)

        self.font = pygame.font.Font(None, font_size)  # Regular font
        self.bold_font = pygame.font.Font(None, font_size)  # Bold font
        self.bold_font.set_bold(True)
        self.menu_options = pygame.sprite.Group()

        START_MENU_OPTIONS_POS_Y = self.screen_height // 8
        START_MENU_OPTIONS_BUFFER = self.screen_height // 20
        # Game menu items

        # {"menu_label": menu_function}
        start_menu_options = {
            "Easy": start_easy,
            "Medium": start_medium,
            "Hard": start_hard
        }
        self.start_menu_options = start_menu_options

        current_y_pos = START_MENU_OPTIONS_POS_Y  # variable that keeps track of the y_pos of each menu item
        for option, action in self.start_menu_options.items():
            self.create_menu_option(
                option,
                #  used to prevent the early execution of the functions, by creating references with parameters
                lambda width=self.screen_width, height=self.screen_height, act=action: act(width, height),
                self.screen_width // 2,
                current_y_pos,
                self.font
            )

            _, text_height = self.font.size(option)
            current_y_pos += text_height + START_MENU_OPTIONS_BUFFER

        #  Quit Game menu item
        current_y_pos += self.screen_height // 12
        self.create_menu_option("Quit Game", self.quit_game, self.screen_width // 2,
                                current_y_pos, self.bold_font, (255, 0, 0))

        #  Screen size menu items
        TEXT_BOX_WIDTH = self.screen_width // 3 + font_size + 10
        TEXT_BOX_HEIGHT = TEXT_BOX_WIDTH // 4

        current_y_pos += self.screen_height // 6
        self.width_box = TextBox(self.screen_width // 4,  # 1/4
                                 current_y_pos,
                                 TEXT_BOX_WIDTH,
                                 TEXT_BOX_HEIGHT,
                                 self.font,
                                 'Width: ',
                                 (255, 255, 255, 0),
                                 self.screen,
                                 self.screen_width)

        self.height_box = TextBox(3 * self.screen_width // 4,  # 3/4
                                  current_y_pos,
                                  TEXT_BOX_WIDTH,
                                  TEXT_BOX_HEIGHT,
                                  self.font,
                                  'Height: ',
                                  (255, 255, 255, 0),
                                  self.screen,
                                  self.screen_height)

        self.menu_options.add(self.width_box, self.height_box)

        # Apply button menu item
        current_y_pos += self.screen_height // 8
        self.create_menu_option("Apply", self.apply_screen_size, self.screen_width // 2, current_y_pos, self.font)

        self.error_message = None

    def create_menu_option(self, text, action, pos_x, pos_y, font, color=(0, 0, 0), *parameters):
        option = MenuOption(text, action, pos_x, pos_y, font, color, self.screen, *parameters)
        self.menu_options.add(option)

    def apply_screen_size(self):
        try:
            new_width = int(self.width_box.get_text())
            new_height = int(self.height_box.get_text())

            if new_width < 300 or new_height < 300:
                raise ValueError("New screen size is too small")
            elif new_width > 1000 or new_height > 1000:
                raise ValueError("New screen size is too large")

        except Exception as e:
            self.error_message = str(e)
            return

        pygame.quit()
        new_menu = StartMenu(new_width, new_height)
        new_menu.run()

    def run(self):
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle events for each menu option and text box
                for option in self.menu_options:
                    option.handle_event(event)

            self.screen.fill((255, 255, 255))
            if self.error_message:
                error_surf = self.font.render(self.error_message, True, (255, 0, 0))
                self.screen.blit(error_surf, (10, 10))  # Display the error message at the top

            self.menu_options.update(event_list)
            self.menu_options.draw(self.screen)
            pygame.display.flip()

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()


def start_easy(screen_width, screen_height):
    pygame.quit()

    game_grid = generate_sudoku(9, 30)

    board = GameBoard(screen_width, screen_height, game_grid)
    board.run()


def start_medium(screen_width, screen_height):
    pygame.quit()

    game_grid = generate_sudoku(9, 40)

    board = GameBoard(screen_width, screen_height, game_grid)
    board.run()


def start_hard(screen_width, screen_height):
    pygame.quit()

    game_grid = generate_sudoku(9, 50)

    board = GameBoard(screen_width, screen_height, game_grid)
    board.run()
