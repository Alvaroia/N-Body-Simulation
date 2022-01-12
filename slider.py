import pygame
import math


class Slider:

    def __init__(self, init, height, width, min_value, max_value, color, default_value):
        self.slider_init_position = init
        self.slider_height = height
        self.slider_width = width
        self.min_value = min_value
        self.max_value = max_value
        self.slider_color = color
        self.default_value = default_value  # %
        # Used for hitbox
        self.rect = pygame.Rect(self.slider_init_position[0], self.slider_init_position[1] - self.slider_height/2,
                                self.slider_width, self.slider_height)
        # Representation of current value in slider
        self.cursor = (round(width / 100 * default_value) + self.slider_init_position[0], self.slider_init_position[1])

        # Actual value contained in slider in log scale
        self.value = math.pow(10,
                    (self.cursor[0] - self.slider_init_position[0])
                     / self.slider_width * (math.log(self.max_value, 10) - math.log(self.min_value, 10))
                              + math.log(self.min_value, 10))

        # Used to decide when can be used
        self.enabled = False


    def update_cursor_position(self, cursor_position):
        x = cursor_position[0]

        new_position = min(max(self.slider_init_position[0], x), self.slider_init_position[0] + self.slider_width)

        self.cursor = (new_position, self.cursor[1])

        self.value = math.pow(10,
                    (self.cursor[0] - self.slider_init_position[0])
                     / self.slider_width * (math.log(self.max_value, 10) - math.log(self.min_value, 10))
                              + math.log(self.min_value, 10))

    def draw(self, screen):
        pygame.draw.line(screen, self.slider_color, self.slider_init_position,
                         (self.slider_init_position[0] + self.slider_width - 1, self.slider_init_position[1]), 3)
        pygame.draw.circle(screen, self.slider_color, self.cursor, 8)
