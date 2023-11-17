import pygame
from pyg import gui

# initialise pygame
pygame.init()
pygame.mixer.init()

# game
game = gui.Game(800, 450, 1.5)
game.main()
input()
