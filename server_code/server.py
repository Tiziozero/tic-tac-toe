import socket
import pickle
import threading
import select

games = []

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = 'localhost', 8888
        self.server.bind((self.ip, self.port))

    def start_server(self):
        game_id = 0
        self.server.listen()
        print(f"Server listening on {self.ip}:{self.port}")
        try:
            while True:
                # Wait for a connection
                client, address = self.server.accept()
                client_2, address_2 = self.server.accept()

                try:
                    print(f"Connection from {address}, {address_2}")

                    # Send a welcome message to the client
                    message = "Hello, World!"
                    client.sendall(pickle.dumps(message))
                    client_2.sendall(pickle.dumps(message))

                    # Start a new game
                    game = Game(game_id, self.server, client, client_2, address, address_2)
                    game.start()
                    games.append(game)
                    game_id += 1
                except:
                    print("Error handling client connection")
                
        except KeyboardInterrupt:
            print("Server closed")

class Game:
    def __init__(self, game_id, server, client, client_2, address, address_2):
        self.game_board = [[0,0,0],[0,0,0],[0,0,0]]
        self.game_id = game_id
        self.server = server
        self.c1 = client
        self.c2 = client_2
        self.ongoing = True
        print(f"Game ID: {self.game_id}, Player 1: {address}, Player 2: {address_2}")

    def stop_connection(self):
        while self.ongoing:
            try:
                _, _, exceptional = select.select([self.c1, self.c2], [], [], 0)
                if exceptional:
                    print(f"Connection from Player 1 or Player 2 closed. Closing all connections")
                    self.ongoing = False
                    self.c1.close()
                    self.c2.close()
                    self.server.close()
                    break
            except KeyboardInterrupt:
                print("Keyboard Interrupt. Closing connection")
                self.ongoing = False
                self.server.close()
                break
        print("end stop_connection thread")
        quit()

    def send(self):
        while self.ongoing:
            try:
                self.c1.sendall(pickle.dumps(self.game_board))
                self.c2.sendall(pickle.dumps(self.game_board))
            except (socket.error, ConnectionResetError):
                print("Connection closed by the client.")
                self.ongoing = False
                break
        print("end send thread")

    def receive(self, client):
        while self.ongoing:
            try:
                data = client.recv(1024)
                try:
                    data = pickle.loads(data)
                except:
                    continue
                if data == "quit_server_connection":
                    self.ongoing = False
                    self.c1.sendall(pickle.dumps(self.game_board))
                    self.c2.sendall(pickle.dumps(self.game_board))
                    self.c1.close()
                    self.c2.close()
                    if client == self.c1:
                        print(f"recived message to quit server connection from {self.c1}. Quitting connection")
                    else:
                        print(f"recived message to quit server connection from {self.c2}. Quitting connection")
                    self.server.close()
                    break


            except (socket.error, ConnectionResetError):
                print("Connection closed by the client.")
                self.ongoing = False
                break
        print("end receive thread")

    def start(self):
        print("Game started")
        send_thread = threading.Thread(target=self.send, args=())
        stop_con_thread = threading.Thread(target=self.stop_connection, args=())
        recive_thread_c1 = threading.Thread(target=self.receive, args=(self.c1,))
        recive_thread_c2 = threading.Thread(target=self.receive, args=(self.c2,))
        send_thread.start()
        stop_con_thread.start()
        recive_thread_c1.start()
        recive_thread_c2.start()

if __name__ == "__main__":
    s = Server()
    s.start_server()

