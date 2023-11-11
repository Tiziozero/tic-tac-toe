import pygame
from pvp_code import logic, settings
from ai_code import logic, settings


mode = int(input("ai[0] or pvp[1]? ")) 

pygame.init()
settings.setup()

if not mode:
    logic.main()

