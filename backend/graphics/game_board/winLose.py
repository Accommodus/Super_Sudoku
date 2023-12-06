import pygame


class WinLose:

    def __init__(self):
        self.GAME_WIDTH = 500
        self.GAME_HEIGHT = 500
        self.screen = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.FONT = 400
        self.BG_COLOR = (255, 255, 245)
        self.LINE_COLOR = (0, 0, 0)

    def draw_game_over(self, winner):
        self.screen.fill(self.BG_COLOR)
        if winner:
            end_text = "You Win!"
        else:
            end_text = "You Lose!"
        end_surf = self.FONT.render(end_text, 0, self.LINE_COLOR)
        end_rect = end_surf.get_rect(center=(self.GAME_WIDTH // 2, self.GAME_HEIGHT // 2 - 50))
        self.screen.blit(end_surf, end_rect)

        restart_text = "Press r to play the game again..."
        restart_surf = self.FONT.render(restart_text, 0, self.LINE_COLOR)
        restart_rect = restart_surf.get_rect(center=(self.GAME_WIDTH // 2, self.GAME_HEIGHT // 2 + 200))
        self.screen.blit(restart_surf, restart_rect)
