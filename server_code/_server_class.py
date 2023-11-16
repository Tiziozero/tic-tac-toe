import socket
import pickle
import _server_settings

class Server:
    def __init__(self, player_1, player_2):
        #self.server_ip = '139.162.200.195'
        #self.server_ip = 'localhost'
        #self.server_port = 8888
        #self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.bind((self.server_ip, self.server_port))
        #self.server.listen()

        self.player_1 = player_1
        self.player_1.send("1".encode())
        self.player_2 = player_2
        self.player_2.send("2".encode())
        self.local_board = [[0,0,0],[0,0,0],[0,0,0]]
        self.turn_player = 1

    def send_all(self, data):
        data = pickle.dumps(data)
        self.player_1.send(data)
        self.player_2.send(data)

    def recive_player_data(self):
        if self.turn_player == 1:
            while True:
                try:
                    data = pickle.loads(self.player_1.recv(1024))
                    if data:
                        return data
                except:
                    pass
    def make_board(self, coords):
        if self.local_board[coords[1]][coords[0]] == 0:
            self.local_board[coords[1]][coords[0]] = self.turn_player
            return True
        else:
            print("not valid cell")
            return False

    
    def main(self):

        self.send_all(self.local_board)
        
        while True:
            try:
                coords = self.recive_player_data()

                if self.make_board(coords):
                    print(self.local_board)
                    self.send_all(self.local_board)
                    if self.turn_player == 1:
                        self.turn_player = 2
                    elif self.turn_player == 2:
                        self.turn_player = 1
                else:
                    pass
            except socket.error as e:
                print(f"ERROR: {e}")
            except KeyboardInterrupt:
                print("Close connection")

                
