import pygame
window = pygame.display.set_mode((800, 500))

b_image = pygame.image.load("graphics/board_1.jpg").convert_alpha()
b_rect = b_image.get_rect(center=(400, 250))
print(f"created window, background image and background rectange")
def setup():
    print(f"created window, background image and background rectange")#it didn't

#test settings

test_board = [#col 0, 1, 2
                 [ 0, 0, 0 ],#row 0
                 [ 0, 0, 0 ],#row 1
                 [ 0, 0, 0 ] #row 2
             ]
test_coords = ( 1, 2 )
test_current_player = 1


