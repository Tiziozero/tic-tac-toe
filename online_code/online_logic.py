from online_code import client_network

def get_coords():
    while True:
        coords = input("row, col (eg '0,1'): ")
        try:
            x, y = int(coords[0]), int(coords[2])
            #print(f"x: {x}, y: {y}")
            return x, y
        except:
            print("invalid input")

def game_logic(pos, current_player, board):
    if board[pos[1]][pos[0]] == 0:
        board[pos[1]][pos[0]] = current_player
        return board, True
    else:
        print("not valid cell")
        return board, False
def print_board(board):
    for row in board:
        print(row)

def main():
    client_network.setup()
    winning_player = 0
    player_ = 1
    local_board = client_network.client_recive()
    game_is_on = True
    while game_is_on:
        #print_board(local_board)
        x, y = get_coords()
        if game_logic((x,y), player_, local_board):
            client_network.client_send((x,y))
            try:
                #local_board = client_network.client_recive()
                print(client_network.client_recive())
            except:
                print("not recived new loca_board")

    print(f"{winning_player} won") 
