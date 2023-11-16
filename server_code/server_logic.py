import socket
import threading
import pickle
import TicTacToeAI
import _server_class
import _server_settings

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


def handle_client(client_socket1, addr1, client_socket2, addr2):

    print(f"Accepted connection from {addr1}, {addr1} is player 1")
    print(f"Accepted connection from {addr2}, {addr2} is player 2")
    
    # Initialize local variables
    game_on = True
    local_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    players = [1, 2]
    winning_player = 0
    local_index = 0
    clients = [client_socket1, client_socket2]
    
    def send_all(data):
        client_socket1.send(pickle.dumps(data))
        client_socket2.send(pickle.dumps(data))
    
    def receive_move():
        print(local_index)
        try:
            return pickle.loads(clients[local_index].recv(512))
        except pickle.UnpicklingError as e:
            print(f"UnpicklingError: {e}")
        except Exception as e:
            print(f"Error: {e}")



    send_all(local_board)
    while game_on:

        try:
            move = receive_move()
            if move:
                try:
                    print(move[0], ", ", move[1])
                    local_board[move[0]][move[1]] = players[local_index]
                    winning_player, game_on = check_win(local_board, players[local_index])
                    print(local_board[0])
                    print(local_board[1])
                    print(local_board[2])
                except:
                    print("Error")
            
        except socket.error as e:
            print(str(e))
            break

        local_index = 1 - local_index  # Switch players
        send_all(local_board)

    if winning_player == 1:
        print("Player 1 won")
    elif winning_player == 2:
        print("Player 2 won")
    elif winning_player == 3:
        print("Draw")
     
    print(f"Closed connection with {addr1}, {addr2}")
    client_socket1.close()
    client_socket2.close()
    
client_sockets = []
client_addrs = []
games = []
# Function to start the _server_settings.server
def start_server():
    list_index = 0


    print("Server listening on port 8888")

    try:
        while True:
            print("Round")
            # Accept the first client connection
            client_socket1, addr1 = _server_settings.server.accept()
            print(client_socket1.recv(1024).decode())
            client_sockets.append(client_socket1)
            client_addrs.append(addr1)
            list_index += 1
            
            # Accept the second client connection
            client_socket2, addr2 = _server_settings.server.accept()
            print(client_socket2.recv(1024).decode())
            client_sockets.append(client_socket2)
            client_addrs.append(addr2)
            game = _server_class.Server(client_socket1, client_socket2)
            games.append(game)
            # Start a thread to handle the two connected clients
            #client_handler = threading.Thread(target=handle_client, args=(client_sockets[0], client_addrs[0], client_sockets[1], client_addrs[1]))
            client_handler = threading.Thread(target=game.main(), args=())
            client_handler.start()

            # Clear the lists for the next pair of clients
            client_sockets.clear()
            client_addrs.clear()
            print("end")



    except KeyboardInterrupt:
        print("Closed _server_settings.server")
        _server_settings.server.close()
        quit()
