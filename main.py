import pygame
from pvp_code import pvp_logic
from ai_code import ai_logic 
mode = int(input("ai[0] or pvp[1]? ")) 

pygame.init()

if not mode:
    ai_logic.main()
else:
    pvp_logic.main_ai()
