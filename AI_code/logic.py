import pygame
import settings
import TicTacToeAI

def check_win( board, coords ):
    for row in board:
        if row[0] == row[1] == row[2]:
            if row[0] != 0:
                return row[0], False

    if board[0][0] == board[1][1] == board[2][2]:
        if board[1][1] != 0:
            return board[1][1], False
    if board[0][2] == board[1][1] == board[2][0]:
        if board[1][1] != 0:
            return board[1][1], False

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] != 0:
                return board[0][col], False
    return 0, True

def blit_board():
    for y in range(3):
        for x in range(3):
            if settings.test_board[y][x] == 0:
                    pygame.draw.rect(settings.window,(255, 0, 0), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

            if settings.test_board[y][x] == 1:
                    pygame.draw.rect(settings.window,(0, 255, 0), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

            if settings.test_board[y][x] == 2:
                    pygame.draw.rect(settings.window,(0, 0, 255), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

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
    settings.window.blit(settings.b_image, settings.b_rect)
    blit_board()
    pygame.display.flip()

def game_logic(pos, current_player):
    if settings.test_board[pos[1]][pos[0]] == 0:
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
        winning_player, game_is_on = check_win(settings.test_board, (0,0))
        update_window()
    print(f"{winning_player} won") 
    pygame.quit()

def main_ai():
    winning_player = 0
    game_is_on = True
    while game_is_on:
        events()
        winning_player, game_is_on = check_win(settings.test_board, (0,0))
        update_window()
        
    print(f"{winning_player} won") 
    pygame.quit()

