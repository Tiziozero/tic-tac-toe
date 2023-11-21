import socket
import pickle
import threading
import sys

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = 'localhost', 8889
        self.self_player = 0
        self.winning_player = 0
        self.ongoing = True
        self.turn_player = 0
        self.connect()

    def connect(self):
        try:
            self.client.connect((self.ip, self.port))
            print(f"Successfully connected to {self.ip}:{self.port}")
            message = pickle.loads(self.client.recv(1024))
            print(f"Server: {message}")
            recv_thread = threading.Thread(target=self.test, args=())
            recv_thread.start()
        except socket.error as e:
            print(f"ERROR: {str(e)}")

    def stop_connection(self):
        pass
    def test(self):
        try:
            while True:
                self.send()
                self.receive()
        except KeyboardInterrupt:
            print("ik")
    def receive(self):
        while self.ongoing:
            try:
                data = self.client.recv(2048)
                if data:
                    try:
                        data = pickle.loads(data)
                        if data == "game won":
                            data = pickle.loads(self.client.recv(1024))
                            self.winning_player = int(data)
                            return self.winning_player
                        if data == "2_p" or data == "1_p":
                            self.turn_player = data[0]
                    except pickle.UnpicklingError as e:
                        print("Unpickling Error ->", str(e))
                        continue
                    print(f"Received: {str(data):_<50}[]")
                    
                else:
                    continue
            except socket.error as e:
                print(f"Socket error -> {str(e)}")

        print("3nd recive thread")

    def send(self):
        while self.ongoing:
            try:
                if self.turn_player == self.self_player:
                    i = input("enter coords [xy]")
                    x, y = int(i[0]), int(i[1])
                    try:
                        data = pickle.dumps((x,y))
                        try:
                            self.client.send(data)
                        except socket.error as e:
                            print(f"Socket error -> {str(e)}")
                    except pickle.PickleError as e:
                        print(f"picklee error -> {str(e)}")
            except:
                print("Invalid input")

if __name__ == '__main__':
    c = Client()

