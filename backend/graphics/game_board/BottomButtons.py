import pygame

def __init__(self, text, action, pos_x, pos_y, font, color, screen, *parameters):
    super().__init__()  # creates a pygame sprite
    self.text = text
    self.action = action
    self.font = font
    self.color = color
    self.screen = screen
    self.parameters = parameters

    self.image = self.font.render(self.text, True, self.color)
    self.rect = self.image.get_rect(center=(pos_x, pos_y))


def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
        self.action(*self.parameters)


    def bottom_GUI(self):
        # finds the middle y-value of the button space
        y_pos = self.screen_height - (self.screen_height * self.SPACE_FOR_BUTTONS_RATIO) // 2
        x_pos = self.screen_width // 2

        buttom_menu_options = {
            "Quit Game": quit_game,
            "Restart": restart

        }

        for option, action in buttom_menu_options.items():
            self.create_menu_option(
                option,
                #  used to prevent the early execution of the functions, by creating references with parameters
                lambda: action,
                x_pos,
                y_pos,
                self.font
            )

    def create_menu_option(self, text, action, pos_x, pos_y, font, color='black', *parameters):
        option = MenuOption(text, action, pos_x, pos_y, font, color, self.screen, *parameters)
        self.bottom_buttons.add(option)

@staticmethod
def quit_game():
    pygame.quit()
    sys.exit()


def restart(screen_width, screen_height):
        new_menu = StartMenu(screen_width, screen_height)
        new_menu.run()