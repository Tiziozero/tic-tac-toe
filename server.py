import socket
import threading
import pickle

class TicTacToeServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)

        print(f"Server is listening on {host}:{port}")

        self.clients = []
        self.games = {}

        self.accept_connections()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")
            client_socket1, client_address1 = self.server_socket.accept()
            print(f"Accepted connection from {client_address1}")
            self.start_game(110, client_socket, client_socket1)



    def start_game(self, game_id, client1, client2):
        game = TicTacToeGame(game_id, client1, client2)
        self.games[game_id] = game
        game.func()

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
                data = pickle.loads(self.players[self.current_player].recv(1024))
                if data:
                    print("data")
                    self.switch_player()
            except:
                pass

    def switch_player(self):
        self.current_player = next(k for k, v in self.players.items() if v != self.players[self.current_player])

if __name__ == "__main__":
    server = TicTacToeServer("localhost", 5555)

