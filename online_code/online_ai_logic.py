import pygame
from test_dir import test_
#import TicTacToeAI
from online_code import client_network
test_.test_player_turn = True

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
            if test_.test_board[y][x] == 0:
                    pygame.draw.rect(test_.window,(255, 0, 0), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

            if test_.test_board[y][x] == 1:
                    pygame.draw.rect(test_.window,(0, 255, 0), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

            if test_.test_board[y][x] == 2:
                    pygame.draw.rect(test_.window,(0, 0, 255), pygame.Rect((x * 50 + 275, y * 50  ), (50, 50)))

def hover_over():
    mouse_pos = pygame.mouse.get_pos()
    for y in range(3):
        for x in range(3):
            #if test_.test_board[y][x] == 0:
                if mouse_pos[0] >= x * 50 + 275 and mouse_pos[0] <= x * 50 + 275 + 50:
                    if mouse_pos[1] >= y * 50  and mouse_pos[1] <= y * 50 + 50:
                                print(f"collision with {x}, {y}")
                                return (x, y)

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            game_logic(hover_over(), test_.test_current_player)

def update_window():
    test_.window.blit(test_.b_image, test_.b_rect)
    blit_board()
    pygame.display.flip()

def game_logic(pos, current_player):
    if test_.test_board[pos[1]][pos[0]] == 0:
        test_.test_board[pos[1]][pos[0]] = current_player
        test_.test_player_turn = False

def main():
    client_network.setup()
    winning_player = 0
    game_is_on = True
    while game_is_on:
        events()
        if not test_.test_player_turn:
            client_network.client_send(test_.test_board)
            test_.test_board = client_network.client_recive()
            test_.test_player_turn = True
            print(f"board {test_.test_board}, player turn {test_.test_player_turn}")
        
        winning_player, game_is_on = check_win(test_.test_board, (0,0))
        update_window()
        
    print(f"{winning_player} won") 
    pygame.quit()

