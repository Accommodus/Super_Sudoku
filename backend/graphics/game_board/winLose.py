import pygame
import sys
from ..start_menu.MenuOption import MenuOption


class EndGameScreen:
    def __init__(self, default_screen_width, default_screen_height, won_game, game_grid):
        self.screen_width = default_screen_width
        self.screen_height = default_screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_grid = game_grid

        pygame.font.init()
        FONT_SIZE_PROPORTION = 0.1  # % of the average screen dimension
        MIN_FONT_SIZE = 24  # Minimum font size for visibility

        average_screen_dimension = (self.screen_width + self.screen_height) // 2
        font_size = max(int(average_screen_dimension * FONT_SIZE_PROPORTION), MIN_FONT_SIZE)

        self.font = pygame.font.Font(None, font_size)
        self.menu_options = pygame.sprite.Group()

        self.message = "Congratulations, You Won!" if won_game else "Game Over, You Lost!"
        self.message_color = (0, 255, 0) if won_game else (255, 0, 0)

        # Menu Options
        menu_y_pos = self.screen_height // 2

        self.add_menu_option("Quit Game", self.quit_game, self.screen_width // 2, menu_y_pos)

    def add_menu_option(self, text, action, pos_x, pos_y):
        option = MenuOption(text, action, pos_x, pos_y, self.font, (0, 0, 0), self.screen)
        self.menu_options.add(option)

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for option in self.menu_options:
                    option.handle_event(event)

            self.screen.fill((255, 255, 255))
            message_surf = self.font.render(self.message, True, self.message_color)
            message_rect = message_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
            self.screen.blit(message_surf, message_rect)

            self.menu_options.update(event_list)
            self.menu_options.draw(self.screen)
            pygame.display.flip()
