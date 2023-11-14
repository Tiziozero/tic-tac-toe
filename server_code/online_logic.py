import socket
import threading
import pickle
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

def handle_user_message(data):
    """
    send board to all
    get p1 input 
    chack win
    send board to all
    get p2 input
    check win
    """
    data = TicTacToeAI.AI(data)
    return data
        


# Function to handle a client connection
def handle_client(client_socket1, addr1, client_socket2 = None, addr2 = None):

    print(f"Accepted connection from {addr1}, {addr1} is player 1")
    print(f"Accepted connection from {addr2}, {addr2} is player 1")
    # defina local variavbels
    game_on = True
    local_board = [[0,0,0],[0,0,0],[0,0,0]]

    # define local functions
    def send_all(data):
        client_socket1.send(pickle.dumps(data))
        if client_socket2:
            client_socket2.send(pickle.dumps(data))

    while game_on:
        try:
            send_all(local_board) # will need do decode 
            while True:
                try:
                    local_board = pickle.loads(client_socket1.recv(512))
                    recived_data = local_board 
                    print(f"            data: {recived_data}")
                    break
                except:
                    pass
                
            if local_board:
                game_on = not check_win(local_board, 0)
            else:
                print(f"recived {recived_data}")
                break

            handle_user_message(local_board)
                
            send_all(local_board)
            sent_data = local_board
            print(f"recived {str(recived_data):_<50}, sending {str(sent_data):_<50}")
            while True:
                try:                                        #chould be 2
                    local_board = pickle.loads(client_socket1.recv(512))
                    recived_data = local_board 
                    break
                except:
                    pass
                
            if local_board:
                game_on = check_win(local_board, 0)
            else:
                print(f"recived {recived_data}")
                break

            handle_user_message(local_board)

        except socket.error as e:
            print(str(e))
            break
   
    print(f"closed connection with {addr1}, {addr2}")
    client_socket1.close()
    if client_socket2:
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
            
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, client_socket, addr))
            client_handler.start()

    except KeyboardInterrupt:
        print("Closed server")
        server.close()
        quit()
