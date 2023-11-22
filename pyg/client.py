import socket
import threading
import pickle
import sys

class TicTacToeClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.player_number = None
        self.board = [[0,0,0],[0,0,0],[0,0,0]]

    def run(self):
        while True:
            try:
                inp = input("input: ")
                if inp == 'quit':
                    break
                else:    
                    self.client_socket.send(pickle.dumps(inp))
            except KeyboardInterrupt:
                break
            except:
                print("error")
                break
    def rec(self):
        while True:
            try:
                data = pickle.loads(self.client_socket.recv(1024))
                print(f"data: {str(data):_<50}")
            except:
                break



if __name__ == "__main__":
    client = TicTacToeClient("localhost", 5555)
    client.run()

