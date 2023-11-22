import socket
import threading
import pickle

class TicTacToeServer:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = ip, port
        self.server.bind((self.ip, self.port))
        self.start_server()
        self.games = []

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
                    game = TicTacToeGame(game_id, client, client_2)
                    game.func()
                    self.games.append(game)
                    game_id += 1
                except:
                    print("Error handling client connection")
                
        except KeyboardInterrupt:
            print("Server closed")

class TicTacToeGame:
    def __init__(self, game_id, client1, client2):
        self.game_id = game_id
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.current_player = client1
        self.players = {client1: 1, client2: 2}
        self.winner = 0
        self.lock = threading.Lock()

    def func(self):
        while True:
            try:
                data = pickle.loads(self.current_player.recv(1024))
                if data:
                    print(f"data: {str(data):_<50}")
                    self.switch_player()
            except:
                pass

    def switch_player(self):
        self.current_player = next(k for k, v in self.players.items() if v != self.players[self.current_player])

if __name__ == "__main__":
    server = TicTacToeServer("localhost", 5555)

