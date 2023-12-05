import pygame
from .constant import *


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