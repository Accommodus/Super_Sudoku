import pygame
import sys
from ..start.MenuOption import MenuOption
from ..start.StartMenu import StartMenu
from .GameBoard import GameBoard


def generate_bottom_button_group(screen_width, screen_height, section_ratio, font, screen, grid,
                                 button_start_x_pos=0,
                                 button_spacing=50):
    """
    Generates UI buttons for sudoku puzzle; returns pygame sprite group

    Parameters:
        screen_width, screen_height (int): Screen dimensions
        section_ratio (float): Ratio for button section
        font (pygame.font.Font): Font for button text
        screen (pygame.Surface): Pygame screen surface
        grid (list): Sudoku grid layout
        button_start_x_pos (int): Starting x position for first button
        button_spacing (int): Spacing between buttons

    Returns:
        pygame.sprite.Group: Group containing button sprites
    """

    # finds the middle y-value of the button space
    y_pos = screen_height - (screen_height * section_ratio) // 2
    x_pos = screen_width // 2

    # lamdas used to prevent premature execution of functions
    bottom_menu_options = {
        "Exit": quit_game,
        "Restart": lambda width=screen_width, height=screen_height, act=restart: act(width, height),
        "Reset": lambda width=screen_width, height=screen_height, grid=grid, act=reset: act(width, height, grid)
    }

    button_group = pygame.sprite.Group()
    current_x_pos = button_start_x_pos
    for option, action in bottom_menu_options.items():
        button = create_button(
            option,
            #  used to prevent the early execution of the functions, by creating references with parameters
            action,
            current_x_pos,
            y_pos,
            font,
            screen
        )

        current_x_pos += button_spacing
        button_group.add(button)

    return button_group


def create_button(text, action, pos_x, pos_y, font, screen, color='black', *parameters):
    button = MenuOption(text, action, pos_x, pos_y, font, color, screen, *parameters)
    return button


def quit_game():
    pygame.quit()
    sys.exit()


def restart(screen_width, screen_height):
    new_menu = StartMenu(screen_width, screen_height)
    new_menu.run()


def reset(screen_width, screen_height, grid):
    pygame.quit()

    new_board = GameBoard(screen_width, screen_height, grid)
    new_board.run()
