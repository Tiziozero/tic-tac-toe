#from test_dir import test_
#import TicTacToeAI
import socket
import threading
import ast
import TicTacToeAI 
server_ip = 'localhost'
#server_ip = '139.162.200.195' #when on server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, 8888))
server.listen(5)

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

def string_to_2d_array(input_str):
    try:
        array_2d = ast.literal_eval(input_str)
        
        if isinstance(array_2d, list) and all(isinstance(row, list) for row in array_2d):
            return array_2d

        else:
            raise ValueError("Invalid input: Not a list of lists")
    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}")
        return None

def table_to_str(table):
    return "[" + ",".join("[{}]".format(",".join(map(str, row))) for row in table) + "]"

def handle_user_message(data) -> str:
    """board = string_to_2d_array(data)
    counter = 0
    check_win(board, None)
    for r in range(0, 3):
        for c in range(0, 3):
            if board[r][c] == 0:
                counter += 1
    if counter == 1:
        for r in range(0, 3):
            for c in range(0, 3):
                if board[r][c] == 0:
                    board[r][c] = 2
                    return table_to_str(board)
    else:
        try:
            return table_to_str(TicTacToeAI.AI(board))
        except:
            print("Error returning board !!! -> table_to_str(TicTacToeAI.AI(board))")
    """
    """
    send board to all
    get p1 input 
    chack win
    send board to all
    get p2 input
    check win
    """
    return data
        


# Function to handle a client connection
def handle_client(client_socket1, addr1, client_socket2, addr2):

    print(f"Accepted connection from {addr1}, {addr1} is player 1")
    print(f"Accepted connection from {addr2}, {addr2} is player 1")
    # defina local variavbels
    game_on = True
    local_board = [[0,0,0],[0,0,0],[0,0,0]]
    
    # define local functions
    def send_all(data):
        client_socket1.send(data)
        client_socket2.send(data)

    # game loop
    while game_on:
        try:
            
            # send board to all players
            send_all(table_to_str(local_board).encode()) # will need do decode 

            # recive new board from player
            local_board = string_to_2d_array(client_socket1.recv(512).decode())
            recive_data = table_to_str(local_board) 
            # if recived data
            if local_board:
                # check if data closes connection
                #if recive_data == 'kys':
                #    break
                # check win
                game_on = check_win(local_board, 0)
            else:
                break
                
            # handel game data
            handle_user_message(local_board)
            
                
            # loop for player 2

            # send board to all players
            send_all(table_to_str(local_board).encode()) # will need do decode 
            send_data = table_to_str(local_board)
            print(f"recived {recive_data:_<50}, sending {send_data:_<50}")

            
            # send board to all players
            send_all(table_to_str(local_board).encode()) # will need do decode 

            # recive new board from player
            local_board = string_to_2d_array(client_socket1.recv(512).decode())
            recive_data = table_to_str(local_board) 
            # if recived data
            if local_board:
                # check if data closes connection
                #if recive_data == 'kys':
                #    break
                # check win
                game_on = check_win(local_board, 0)
            else:
                break
                
            # handel game data
            handle_user_message(local_board)
            
                
            # loop for player 2

            # send board to all players
            send_all(table_to_str(local_board).encode()) # will need do decode 
            send_data = table_to_str(local_board)
            print(f"recived {recive_data:_<50}, sending {send_data:_<50}")

        except socket.error as e:
            print(str(e))
            break
   
    print(f"closed connection with {addr1}, {addr2}")
    client_socket1.close()
    client_socket2.close()
    
client_sockets = []
client_addrs = []
# Function to start the server
def start_server():
    list_index = 0
    print("Server listening on port 8888")
    try:
        # scrap this
        # check if two or more connection
        while True:
            client_socket, addr = server.accept()
            client_sockets.append(client_socket)
            client_addrs.append(addr)
            list_index += 1

        while True:
            # Accept a connection from a client
            # accept player 1
            client_socket1, addr1 = server.accept()
            print(f"accepted connection to {addr1}, recived:{client_socket1.recv(512):_<50}")
            
            # accept player 2
            client_socket2, addr2 = server.accept()
            print(f"accepted connection to {addr2}, recived:{client_socket2.recv(512):_<50}")
            
            # append to lists
            client_sockets.append(client_socket1)
            client_addrs.append(addr1)
            client_sockets.append(client_socket2)
            client_addrs.append(addr2)

            # Receive data from the client
            data1 = client_socket1.recv(1024).decode()
            data2 = client_socket2.recv(1024).decode()

            # Start a new thread to handle the client
            client_handler = threading.Thread(target=handle_client, args=(client_socket1, addr1, client_socket2, addr2))
            client_handler.start()
            list_index += 1
    except KeyboardInterrupt:
        print("Closed server")
        server.close()
        quit()
