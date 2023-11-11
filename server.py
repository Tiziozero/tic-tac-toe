import socket
import threading
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8888))  # Use any available network interface and port 8888
server.listen(5)  # Listen for up to 5 connections


def handle_user_message(data) -> str:
    pass


# Function to handle a client connection
def handle_client(client_socket, address, data):
    print(f"Accepted connection from {address}")
    while True:
        try:
            recive_data = client_socket.recv().decode()
            if recive_data:
                send_data = handle_user_message(recive_data)
                client_socket.send(send_data.encode())
                print(f"recived {recive_data:_<30}, sending{send_data:_<30}")
        except socket.error as e:
            print(str(e))
            break
   
    print(f"closed connection with {address}")
    client_socket.close()
    

# Function to start the server
def start_server():
    print("Server listening on port 8888")

    while True:
        # Accept a connection from a client
        client_socket, addr = server.accept()

        # Receive data from the client
        data = client_socket.recv(1024).decode()

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, data))
        client_handler.start()

# Start the server
start_server()

