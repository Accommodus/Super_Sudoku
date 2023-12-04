import pygame
import sys


class MenuOption(pygame.sprite.Sprite):
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
    def __init__(self, pos_x, pos_y, width, height, font, prompt_text, color, screen):
        super().__init__()  # creates a pygame sprite
        self.font = font
        self.prompt_text = prompt_text
        self.color = color
        self.screen = screen
        self.text = ''
        self.active = False

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self, *args, **kwargs):
        self.image.fill(self.color)
        text_surface = self.font.render(self.prompt_text + self.text, True, (0, 0, 0))
        self.image.blit(text_surface, (5, (self.rect.height - text_surface.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            if self.active and not self.text:
                self.text = ''
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def get_text(self):
        return self.text


class GameMenu:
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

        # Determine the y position and buffer for the menu options
        start_menu_options_pos_y = self.screen_height // 8
        start_menu_options_buffer = self.screen_height // 20  # Fixed buffer space between items

        # Calculate the position of each menu option
        current_y_pos = start_menu_options_pos_y
        for option, action in start_menu_options.items():
            self.create_menu_option(option, action, self.screen_width // 2, current_y_pos, self.font)
            _, text_height = self.font.size(option)
            current_y_pos += text_height + start_menu_options_buffer

        current_y_pos += self.screen_height // 12  # Additional space
        self.create_menu_option("Quit Game", self.quit_game, self.screen_width // 2,
                                current_y_pos, self.bold_font, (255, 0, 0))

        # Add TextBoxes for width and height inputs
        current_y_pos += self.screen_height // 12
        self.width_box = TextBox(self.screen_width // 4,  # 1/4
                                 current_y_pos,
                                 140,
                                 30,
                                 self.font,
                                 'Width: ',
                                 (255, 255, 255, 0),
                                 self.screen)

        self.height_box = TextBox(3 * self.screen_width // 4,  # 3/4
                                  current_y_pos,
                                  140,
                                  30,
                                  self.font,
                                  'Height: ',
                                  (255, 255, 255, 0),
                                  self.screen)

        self.menu_options.add(self.width_box, self.height_box)

        # Add Apply button for changing screen size
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
            self.screen = pygame.display.set_mode((new_width, new_height))

            if new_width < 100 or new_height < 100: raise "New screen size is too small"
            elif new_width > 1000 or new_height > 1000: raise "New screen size is too large"

            self.screen_width = new_width
            self.screen_height = new_height
            self.error_message = None
        except Exception as e:
            self.error_message = str(e)

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
        print("Starting Easy mode...")

    def start_medium(self):
        print("Starting Medium mode...")

    def start_hard(self):
        print("Starting Hard mode...")

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()
