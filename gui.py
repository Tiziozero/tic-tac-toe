import pygame
import settings
import logic
pygame.init()

window = pygame.display.set_mode((800, 500))

b_image = pygame.image.load("graphics/board_1.jpg").convert_alpha()
b_rect = b_image.get_rect(center=(400, 250))

def blit_board():
    for y in range(3):
        for x in range(3):
            if settings.test_board[y][x] == 0:
                    pygame.draw.rect(window,(255, 0, 0), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

            if settings.test_board[y][x] == 1:
                    pygame.draw.rect(window,(0, 255, 0), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

            if settings.test_board[y][x] == 2:
                    pygame.draw.rect(window,(0, 0, 255), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

def hover_over():
    mouse_pos = pygame.mouse.get_pos()
    for y in range(3):
        for x in range(3):
            #if settings.test_board[y][x] == 0:
                if mouse_pos[0] >= x * 50 + 275 and mouse_pos[0] <= x * 50 + 275 + 50:
                    if mouse_pos[1] >= y * 50  and mouse_pos[1] <= y * 50 + 50:
                                print(f"collision with {x}, {y}")
                                return (x, y)

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            game_logic(hover_over(), settings.test_current_player)

def update_window():
    window.blit(b_image, b_rect)
    blit_board()
    pygame.display.flip()

def game_logic(pos, current_player):
    settings.test_board[pos[1]][pos[0]] = current_player
    if settings.test_current_player == 1:
        settings.test_current_player = 2
    else:
        settings.test_current_player = 1

def main():
    winning_player = 0
    game_is_on = True
    while game_is_on:
        events()
        winning_player, game_is_on = logic.check_win(settings.test_board, (0,0))
        update_window()
        print(f"{winning_player} won") 

main()
