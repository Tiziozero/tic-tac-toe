import socket
import pickle
import threading


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = 'localhost', 8888
        self.server.bind((self.ip, self.port))
        


    def start_server(self):
        self.server.listen()
        print(f"Server listening on {self.ip}:{self.port}")
        try:
            while True:
                # Wait for a connection
                client_socket, client_address = self.server.accept()

                try:
                    print(f"Connection from {client_address}")

                    # Send "Hello, World!" to the client
                    message = "Hello, World!"
                    client_socket.sendall(pickle.dumps(message))
                    client_handle_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                    client_handle_thread.start()
                except:
                    print("none")
        except KeyboardInterrupt:
            print("close server")
    def handle_client(self, client_socket, client_address):
        print(f"client socket: , client address: {client_address}")
        try:
            while True:
                if client_socket._closed:
                    break  # Break the loop if the socket is closed
                client_socket.send(pickle.dumps("Hello, Client!"))

        except ConnectionResetError:
            print(f"Connection with {client_address} reset by the client.")
        except Exception as e:
            print(f"Error handling client {client_address}: {str(e)}")
        finally:
            if not client_socket._closed:
                print(f"Closing connection with {client_address}")
                client_socket.close()

if __name__ == "__main__":
    s = Server()
    s.start_server()

