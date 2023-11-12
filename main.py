import pygame
from pvp_code import pvp_logic
from ai_code import ai_logic 
from online_code import online_logic
mode = int(input("ai[0] or pvp[1] or 'online'[2]? ")) 

pygame.init()

if mode == 0:
    ai_logic.main_ai()
elif mode == 1:
    pvp_logic.main()
elif mode == 2:
    online_logic.main_online()
