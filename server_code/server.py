import socket
import pickle
import sys 
import threading
import select

games = []

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = 'localhost', 8888
        self.server.bind((self.ip, self.port))
        self.start_server()

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
        self.turn_player = self.c1
        print(f"Game ID: {self.game_id}, Player 1: {address}, Player 2: {address_2}")
        self.start()
    
    def _game(self):
        try:
            while True:
                print("cycle")
                self.turn_player =self.c1
                self.send(self.turn_player, self.game_board)
                self.receive(self.turn_player)
                self.changeturn()
        except KeyboardInterrupt:
            print("ki")
            quit()
    def changeturn(self):
        if self.turn_player == self.c1:
            self.turn_player = self.c2
        else:
            self.turn_player = self.c1
    def stop_connection(self):
        while self.ongoing:
            pass

    def send(self, client, data):
        while self.ongoing:
            try:
                data = pickle.dumps(data)
                try:
                    client.send(data)
                    return
                except socket.error as e:
                    print(f"Socket eerror -> {str(e)}")
            except pickle.UnpicklingError as e:
                print(f"Unpicking error -> {str(e)}")


    def receive(self, client):
        while True:
            try:
                data = client.recv(1024)
                if data:
                    try:
                        data = pickle.loads(data)
                        print(f"received: {str(data):_<50}[]")
                        return
                    except pickle.PickleError as e:
                        print(f"Pickling Error -> {str(e)}")
            except socket.error as e:
                    print(f"Socket eerror -> {str(e)}")
 
    def start(self):
        print("Game started")
        _game_thread = threading.Thread(target=self._game, args=())
        _game_thread.start()

if __name__ == "__main__":
    s = Server()
