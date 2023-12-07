import pygame


class Cell(pygame.sprite.Sprite):
    """
    Interactive Sudoku cell sprite for Pygame application

    Attributes:
        font (pygame.font.Font): Font for cell text
        default_background_color, highlight_color, default_text_color, sketched_text_color (tuple): Color configurations
        current_color (tuple): Current color of cell
        screen (pygame.Surface): Surface to draw cell on
        filled_in (bool): Indicates if cell is pre-filled
        text (str): Text content of cell
        active (bool): Active state of cell
        image (pygame.Surface): Surface for cell representation
        rect (pygame.Rect): Rectangular area of cell
        outline_color (tuple): Color of cell border
        outline_width (int): Thickness of cell border

    Methods:
        update(): Redraws the cell with updated properties
        handle_event(event): Handles events like mouse clicks and key presses
        set_active(boole): Sets the active state of the cell
    """

    def __init__(self, pos_x, pos_y, filled_in, text, width, height, font, screen,
                 highlight_color='red',
                 outline_color=(0, 0, 0),
                 outline_width=2,
                 default_background_color='white',
                 default_text_color='black',
                 sketched_text_color='grey'):

        super().__init__()
        self.font = font
        self.default_background_color = default_background_color
        self.highlight_color = highlight_color
        self.default_text_color = default_text_color
        self.sketched_text_color = sketched_text_color
        self.current_color = self.default_text_color
        self.screen = screen
        self.filled_in = filled_in
        self.text = str(text)
        self.active = False

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.outline_color = outline_color
        self.outline_width = outline_width

    def update(self, *args, **kwargs):
        self.image.fill(self.current_color)
        pygame.draw.rect(self.image, self.outline_color, self.image.get_rect(), self.outline_width)

        text_color = self.default_text_color if self.filled_in else self.sketched_text_color

        pygame.font.init()

        text_surface = self.font.render(self.text, True, pygame.Color(text_color))
        text_rect = text_surface.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
        self.image.blit(text_surface, text_rect)

        if not self.active:
            self.current_color = self.default_background_color

    def handle_event(self, event):
        # Allow highlighting for all cells
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.set_active(True)
            else:
                self.set_active(False)

        # Allow editing only active if not filled in
        if not self.filled_in and self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                    self.text = event.unicode
                elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.text != '':
                    self.filled_in = True
                    self.set_active(False)

    def set_active(self, boole):
        self.active = boole
        self.current_color = self.highlight_color if self.active else self.default_background_color
