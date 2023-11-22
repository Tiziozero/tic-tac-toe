import socket
import pickle
import sys 
import threading
import select

games = []

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = 'localhost', 8889
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
        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.game_id = game_id
        self.server = server
        self.c1 = client
        self.c2 = client_2
        self.ongoing = True
        self.turn_player = self.c1
        self.winning_player = 0
        print(f"Game ID: {self.game_id}, Player 1: {address}, Player 2: {address_2}")
        self.lock = threading.Lock()
        self.start()

    def check_win( self, board ):
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

    def game_logic(self,pos):
        try:
            if self.game_board[pos[1]][pos[0]] == 0:
                if self.turn_player == self.c1:
                    self.game_board[pos[1]][pos[0]] = 1
                    self.turn_player = self.c2
                    self.c1.send(pickle.dumps(f"2_p"))
                    self.c2.send(pickle.dumps(f"2_p"))
                    return True
               elif self.turn_player == self.c2:
                    self.game_board[pos[1]][pos[0]] = 2
                    self.turn_player = self.c1
                    self.c1.send(pickle.dumps(f"1_p"))
                    self.c2.send(pickle.dumps(f"1_p"))
                    return True
            else:
                print("not valid cell")
                return False
        except:
            print("invalid cell")
            return False



    def _game(self):
        self.c1.send(pickle.dumps("game on"))
        self.c2.send(pickle.dumps("game on"))
        try:
            self.turn_player = self.c1
            while self.ongoing:
                print("cycle")
                self.send(self.turn_player, self.game_board)
                pos = self.receive(self.turn_player)
                if self.game_logic(pos):
                    print(f"{self.winning_player} won")
                    print(self.game_board[0])
                    print(self.game_board[1])
                    print(self.game_board[2])
                    self.winning_player, self.ongoing = self.check_win(self.game_board)
                    if not self.ongoing:
                        break
                else:
                    pass

            self.c1.send(pickle.dumps(f"game won"))
            self.c2.send(pickle.dumps(f"game won"))
            self.c1.send(pickle.dumps(self.winning_player))
            self.c2.send(pickle.dumps(self.winning_player))

        except KeyboardInterrupt:
            print("ki")
            quit()

    def changeturn(self):
        print("Changing turns")
        if self.turn_player == self.c1:
            self.turn_player = self.c2
            print("turn player = 2")
            self.c1.send(pickle.dumps(f"2_p"))
            self.c2.send(pickle.dumps(f"2_p"))
            
        elif self.turn_player == self.c2:
            self.turn_player = self.c1
            print("turn player = 1")
            self.c1.send(pickle.dumps(f"1_p"))
            self.c2.send(pickle.dumps(f"1_p"))
        print(f"                    player = {self.turn_player}")


    def stop_connection(self):

        while self.ongoing:
            pass

    def send(self, client, data):
            try:
                data = pickle.dumps(data)
                try:
                    self.c1.send(data)
                    self.c2.send(data)
                    return

                except socket.error as e:
                    print(f"Socket error -> {str(e)}")

            except pickle.PickleError as e:
                print(f"Pickle error -> {str(e)}")


    def receive(self, client):
            try:
                data = client.recv(1024)
                if data:
                    try:
                        data = pickle.loads(data)
                        print(f"received: {str(data):_<50}[]")
                        return data
                    except pickle.PickleError as e:

                        print(f"Pickle Error -> {str(e)}")

            except socket.error as e:
                print(f"Socket error -> {str(e)}")


    def start(self):
        print("Game started")
        #_game_thread = threading.Thread(target=self._game, args=())
        #_game_thread.start()
        self._game()
        self.c1.close()
        self.c2.close()
        
if __name__ == "__main__":
    s = Server()
