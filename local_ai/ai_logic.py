from test_dir import test_
from local_ai import TicTacToeAI

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

    for row in board:
        for element in row:
            if element == 0:
                return 0,  True

    return 3, False

def get_coords():
    while True:
        coords = input("row, col (eg '0,1'): ")
        try:
            x, y = int(coords[0]), int(coords[2])
            #print(f"x: {x}, y: {y}")
            return x, y
        except:
            print("invalid input")

def game_logic(pos, current_player):
    if test_.test_board[pos[1]][pos[0]] == 0:
        test_.test_board[pos[1]][pos[0]] = current_player
        if test_.test_current_player == 1:
            test_.test_current_player = 2
        else:
            test_.test_current_player = 1
    else:
        print("not valid cell")
def print_board(board):
    for row in board:
        print(row)

def main():
    winning_player = 0
    game_is_on = True
    test_.test_current_player = 1
    while game_is_on:
        print_board(test_.test_board)
        x, y = get_coords()
        game_logic((x,y), test_.test_current_player)
        winning_player, game_is_on = check_win(test_.test_board, (0,0))
        if game_is_on:
            if test_.test_current_player == 2:
                test_.test_board = TicTacToeAI.AI(test_.test_board)
                test_.test_current_player = 1
        winning_player, game_is_on = check_win(test_.test_board, (0,0))

    if winning_player == 3:
        print("Draw")
    elif winning_player == 1 or winning_player == 2:
        print(f"{winning_player} won") 
