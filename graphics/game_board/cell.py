import pygame


class Cell(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, width, height, font, color, screen,
                 default_text='',
                 highlight_color=(255, 0, 0),
                 outline_color=(0, 0, 0),
                 outline_width=2):

        super().__init__()  # creates a pygame sprite
        self.font = font
        self.default_color = color
        self.highlight_color = highlight_color
        self.current_color = self.default_color
        self.screen = screen
        self.text = str(default_text)
        self.active = False

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.outline_color = outline_color
        self.outline_width = outline_width

    def update(self, *args, **kwargs):
        self.image.fill(self.current_color)

        pygame.draw.rect(self.image, self.outline_color, self.image.get_rect(), self.outline_width)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
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

    def get_text(self):
        return self.text
