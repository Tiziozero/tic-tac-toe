import pygame

class Window:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        print("Created window")
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
