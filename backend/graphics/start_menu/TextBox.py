import pygame


class TextBox(pygame.sprite.Sprite):
    """
    Represents an interactive text box for user input

    Attributes
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

    Methods
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
