import socket
import threading
import pickle
import sys

class TicTacToeClient:
    def __init__(self, host, port ):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.player_number = None
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.lock = threading.Lock()
        self.player_number = pickle.loads(self.client_socket.recv(1024))
        self.ongoing = True
        print(f"player number: {self.player_number}")
        self.setup()

        rthread = threading.Thread(target=self.rec, args=())
        rthread.start()
        self.run()

    def return_board(self):
        return self.board

    def return_player_nuber(self):
        return self.player_number

    def setup(self):
        pass
        #self.player_number = pickle.loads(self.client_socket.recv(1024))

    
    def run(self):
        while self.ongoing:
            try:
                inp = input("input: ")
                if inp == 'quit':
                    self.client_socket.send(pickle.dumps('quit'))
                    self.client_socket.send(pickle.dumps(self.player_number))

                else:    
                    self.client_socket.send(pickle.dumps((int(inp[0]), int(inp[1]))))
            except KeyboardInterrupt:
                break
            except:
                print("error")
                break
    def rec(self):
        while self.ongoing:
            try:
                print("----------reciving ...")
                data = pickle.loads(self.client_socket.recv(1024))
                print(f"data: {str(data):_<50}")
                if isinstance(data, list) and len(data) == 3 and isinstance(data[0], list) and len(data[0]) == 3:
                    with self.lock:
                        self.board = data
                elif isinstance(data, str):
                    if data[:5] == 'player':
                        print(f"player {data[7]} won!")
                        self.ongoing = False
                        print("break, quit")
                        sys.exit()
                        break
                        quit()

            except:
                break




if __name__ == "__main__":
    client = TicTacToeClient("localhost", 5555)
    client.run()

