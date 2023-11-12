import pygame
from test_dir import test_
from pvp_code import pvp_logic
from ai_code import ai_logic 
from online_code import online_ai_logic

pygame.init()

font = pygame.font.Font(None, 36)  # None uses the default font, 36 is the size
text_a = font.render("'a' for local pvp mode", True, (255, 255, 255))  # (255, 255, 255) is white
text_b = font.render("'b' for local ai mode",True, (255, 255, 255))
text_c = font.render("'c' for online ai mode... idk why but ye", True, (255, 255, 255))  # (255, 255, 255) is white
text_d = font.render("'d' for online pvp mode", True, (255, 255, 255))  # (255, 255, 255) is white

text_rect_a = text_a.get_rect()
text_rect_b = text_b.get_rect()
text_rect_c = text_c.get_rect()
text_rect_d = text_d.get_rect()
text_rect_a.center = (test_.WIDTH // 2, 50)
text_rect_b.center = (test_.WIDTH // 2, 150)
text_rect_c.center = (test_.WIDTH // 2, 250)
text_rect_d.center = (test_.WIDTH // 2, 350)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pvp_logic.main()
                pygame.quit()
                quit()
            elif event.key == pygame.K_b:
                ai_logic.main_ai()
                pygame.quit()
                quit()
            elif event.key == pygame.K_c:
                online_ai_logic.main_online()
                pygame.quit()
                quit()
    test_.window.blit(text_a, text_rect_a)
    test_.window.blit(text_b, text_rect_b)
    test_.window.blit(text_c, text_rect_c)
    test_.window.blit(text_d, text_rect_d)
    pygame.display.flip()
