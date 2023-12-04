import pygame
import sys
from .game_board import sudokuGUI


class MenuOption(pygame.sprite.Sprite):
    """
    Represents a selectable menu item

    - text: The text displayed
    - action: The function to be executed when the menu option is selected
    - font: Font used to render the text
    - color: The color of the text
    - screen: Screen where the menu option is displayed
    - image: The rendered surface
    - rect: The rectangle area for positioning and event handling

    - handle_event(): Checks if the menu option is clicked and triggers the associated action
    """

    def __init__(self, text, action, pos_x, pos_y, font, color, screen):
        super().__init__()  # creates a pygame sprite
        self.text = text
        self.action = action
        self.font = font
        self.color = color
        self.screen = screen

        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()


class TextBox(pygame.sprite.Sprite):
    """
    Represents an interactive text box for user input

    - font: Font used to render the text
    - prompt_text: text displayed before user input
    - default_color: Default background color
    - highlight_color: Background color when it is active (focused)
    - current_color: The current background color
    - screen: screen where the text box is displayed
    - text: The text entered by the user
    - active: A boolean indicating if the text box is active
    - image: The rendered surface
    - rect: The rectangle area for positioning and event handling
    - outline_color: Color of the outline
    - outline_width: Width of the outline

    - update(): Redraws the text box.
    - handle_event(): Handles keyboard and mouse events
    - get_text(): Returns the current text
    """
    def __init__(self, pos_x, pos_y, width, height, font, prompt_text, color, screen, default_text='',
                 highlight_color=(255, 0, 0),
                 outline_color=(0, 0, 0),
                 outline_width=2):

        super().__init__()  # creates a pygame sprite
        self.font = font
        self.prompt_text = prompt_text
        self.default_color = color
        self.highlight_color = highlight_color
        self.current_color = self.default_color
        self.screen = screen
        self.text = str(default_text)
        self.active = False

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.outline_color = outline_color
        self.outline_width = outline_width

    def update(self, *args, **kwargs):
        self.image.fill(self.current_color)

        pygame.draw.rect(self.image, self.outline_color, self.image.get_rect(), self.outline_width)

        text_surface = self.font.render(self.prompt_text + self.text, True, (0, 0, 0))
        self.image.blit(text_surface, (5, (self.rect.height - text_surface.get_height()) // 2))

        if not self.active:
            self.current_color = self.default_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.current_color = self.highlight_color
                if not self.text:
                    self.text = ''
            else:
                self.active = False
                self.current_color = self.default_color

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def get_text(self):
        return self.text


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

        self.font = pygame.font.Font(None, 36)  # Regular font
        self.bold_font = pygame.font.Font(None, 36)  # Bold font
        self.bold_font.set_bold(True)  # Set the font to bold
        self.menu_options = pygame.sprite.Group()

        # {"menu_label": menu_function}
        start_menu_options = {
            "Easy": self.start_easy,
            "Medium": self.start_medium,
            "Hard": self.start_hard
        }

        START_MENU_OPTIONS_POS_Y = self.screen_height // 8
        START_MENU_OPTIONS_BUFFER = self.screen_height // 20

        # Calculate the position of each game menu option
        current_y_pos = START_MENU_OPTIONS_POS_Y  # variable that keeps track of the y_pos of each menu item
        for option, action in start_menu_options.items():
            self.create_menu_option(option, action, self.screen_width // 2, current_y_pos, self.font)
            _, text_height = self.font.size(option)
            current_y_pos += text_height + START_MENU_OPTIONS_BUFFER

        #  Quit Game menu item
        current_y_pos += self.screen_height // 12
        self.create_menu_option("Quit Game", self.quit_game, self.screen_width // 2,
                                current_y_pos, self.bold_font, (255, 0, 0))

        #  Width and height menu items
        TEXT_BOX_WIDTH = self.screen_width // 3 + 40
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

    def create_menu_option(self, text, action, pos_x, pos_y, font, color=(0, 0, 0)):
        option = MenuOption(text, action, pos_x, pos_y, font, color, self.screen)
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

    def start_easy(self):
        pygame.quit()
        board = sudokuGUI.GameBoard(self.screen_width, self.screen_height)
        board.run()

    def start_medium(self):
        pygame.quit()
        board = sudokuGUI.GameBoard(self.screen_width, self.screen_height)
        board.run()

    def start_hard(self):
        pygame.quit()
        board = sudokuGUI.GameBoard(self.screen_width, self.screen_height)
        board.run()

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()
