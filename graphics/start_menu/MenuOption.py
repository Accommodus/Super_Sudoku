import pygame


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
