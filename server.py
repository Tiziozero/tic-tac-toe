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
                # Wait for a connection from client 1
                client1, address1 = self.server.accept()

                # Wait for a connection from client 2
                client2, address2 = self.server.accept()

                try:
                    print(f"Connection from {address1}, {address2}")

                    try:
                        client1.sendall(pickle.dumps(1))
                    except socket.error as e:
                        print(f"ERROR: -> {str(e)}")
                    try:
                        client2.sendall(pickle.dumps(2))
                    except socket.error as e:
                        print(f"ERROR: -> {str(e)}")

                    game = TicTacToeGame(game_id, client1, client2)
                    #game.func()
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
        self.c1 = client1
        self.c2 = client2
        self.wp = 0
        self.current_player = client1
        self.players = {client1: 1, client2: 2}
        self.index = 0
        self.players__ = [client1, client2]
        self.winner = 0
        self.lock = threading.Lock()
        self.ongoing = True
        rthread = threading.Thread(target=self.func1, args=())
        rthread.start()

    def check_win( self, board ):
        with self.lock:
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

    def game_logic(self, pos):
        try:
            if self.board[pos[1]][pos[0]] == 0:
                with self.lock:
                    self.board[pos[1]][pos[0]] = self.players[self.current_player]
                    return True
            else:
                print("not valid cell")
                return False
        except:
            print("invalid cell")
            return False

    def func(self):
        print("func")
        print(f"player 1: {str(self.c1)}")
        print(f"player 2: {str(self.c2)}")
        while self.ongoing:
            try:
                data = pickle.loads(self.c1.recv(1024))
                if data:
                    print(f"data: {str(data):_<50}")
                    if isinstance(data, tuple):
                        if self.game_logic(data):
                            self.wp, self.ongoing = self.check_win(self.board)
                            self.switch_player()
                            print(self.board[0])
                            print(self.board[1])
                            print(self.board[2])
                            if not self.ongoing:
                                break
                    elif isinstance(data, str):
                        print("string")
                        if data == 'quit':
                            p = pickle.loads(self.current_player.recv(1024))
                            if p == 1:
                                self.ongoing = False
                            elif p == 2:
                                self.ongoing = False
            except socket.error as e:
                print(f"ERROR: -> {str(e)}")
            except pickle.UnpicklingError as e:
                print(f"ERROR: -> {str(e)}")
            except KeyboardInterrupt:
                self.ongoing = False
                break
            except:
                pass
            try:
                data = pickle.loads(self.c2.recv(1024))
                if data:
                    print(f"data: {str(data):_<50}")
                    if isinstance(data, tuple):
                        if self.game_logic(data):
                            self.wp, self.ongoing = self.check_win(self.board)
                            self.switch_player()
                            print(self.board[0])
                            print(self.board[1])
                            print(self.board[2])
                            if not self.ongoing:
                                break
                    elif isinstance(data, str):
                        print("string")
                        if data == 'quit':
                            p = pickle.loads(self.current_player.recv(1024))
                            if p == 1:
                                self.ongoing = False
                            elif p == 2:
                                self.ongoing = False
            except socket.error as e:
                print(f"ERROR: -> {str(e)}")
            except pickle.UnpicklingError as e:
                print(f"ERROR: -> {str(e)}")
            except KeyboardInterrupt:
                self.ongoing = False
                break
            except:
                pass
        print("Closing server")
        self.c1.send(pickle.dumps(f"player {self.wp} won"))
        self.c1.close()
        self.c2.close()

    def func1(self):
        print("func1")
        while self.ongoing:
            try:
                data = pickle.loads(self.current_player.recv(1024))
                if data:
                    print(f"data: {str(data):_<50}")
                    if isinstance(data, tuple):
                        if self.game_logic(data):
                            self.wp, self.ongoing = self.check_win(self.board)
                            self.switch_player()
                            print(self.board[0])
                            print(self.board[1])
                            print(self.board[2])
                            self.players__[0].send(pickle.dumps(self.board))
                            self.players__[1].send(pickle.dumps(self.board))
                            if not self.ongoing:
                                break
                    elif isinstance(data, str):
                        print("string")
                        if data == 'quit':
                            p = pickle.loads(self.current_player.recv(1024))
                            if p == 1:
                                self.ongoing = False
                            elif p == 2:
                                self.ongoing = False
            except socket.error as e:
                print(f"ERROR: -> {str(e)}")
            except pickle.UnpicklingError as e:
                print(f"ERROR: -> {str(e)}")
            except KeyboardInterrupt:
                self.ongoing = False
                break
            except:
                pass
        print("Closing server")
        self.c1.send(pickle.dumps(f"player {self.wp} won"))
        self.c2.send(pickle.dumps(f"player {self.wp} won"))
        self.c1.close()
        self.c2.close()

    def switch_player(self):
        #self.current_player = next(k for k, v in self.players.items() if v != self.players[self.current_player])
        self.index += 1
        self.current_player = self.players__[ self.index % 2 ]
        print(f"         switching players: index = {str(self.index): <3}, index % 2 = {str(self.index % 2): <3}")

if __name__ == "__main__":
    server = TicTacToeServer("localhost", 5555)

