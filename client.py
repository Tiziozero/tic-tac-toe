import socket
import threading
import pickle
import sys

class TicTacToeClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.player_number = None

    def run(self):
        while True:
            try:
                self.client_socket.send(pickle.dumps(input("input: ")))
            except:
                pass

if __name__ == "__main__":
    client = TicTacToeClient("localhost", 5555)
    client.run()

