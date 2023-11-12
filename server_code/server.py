import socket
import threading
import ast
import TicTacToeAI
import online_logic
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("139.162.200.195", 8888))
server.listen(5)


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
    board = string_to_2d_array(data)
    counter = 0
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
        return table_to_str(TicTacToeAI.AI(board))


# Function to handle a client connection
def handle_client(client_socket, address, data):
    print(f"Accepted connection from {address}")
    while True:
        try:
            recive_data = client_socket.recv(512).decode()
            if recive_data:
                if data == 'kys':
                    break
                send_data = handle_user_message(recive_data)
                client_socket.send(send_data.encode())
                print(f"recived {recive_data:_<50}, sending {send_data:_<50}")
        except socket.error as e:
            print(str(e))
            break
   
    print(f"closed connection with {address}")
    client_socket.close()
    

# Function to start the server
def start_server():
    print("Server listening on port 8888")
    try:
        while True:
            # Accept a connection from a client
            client_socket, addr = server.accept()

            # Receive data from the client
            data = client_socket.recv(1024).decode()

            # Start a new thread to handle the client
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, data))
            client_handler.start()
    except KeyboardInterrupt:
        print("Closed server")
        server.close()
        quit()

# Start the server
start_server()

