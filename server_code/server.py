import online_logic
import threading
import pickle
# Function to start the server
def start_server():
    print("Server listening on port 8888")
    try:
        while True:
            # Accept a connection from a client
            client_socket, addr = online_logic.server.accept()

            # Receive data from the client
            data = pickle.loads(client_socket.recv(1024))

            # Start a new thread to handle the client
            client_handler = threading.Thread(target=online_logic.handle_client, args=(client_socket, addr, data))
            client_handler.start()
    except KeyboardInterrupt:
        print("Closed server")
        online_logic.server.close()
        quit()

# Start the server
online_logic.start_server()


