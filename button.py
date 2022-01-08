import pygame


class Button:

    def __init__(self, init_pos, width, height, color, hover_color):
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(init_pos, (width, height))
        self.hover = False

    def draw(self, screen):
        if self.hover:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

