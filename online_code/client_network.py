import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = 'localhost', 8888
        self.connection = None

    def connect(self):
        try:
            self.client.connect((self.ip, self.port))
            print(f"Successfully connected to {self.ip}:{self.port}")
            self.connection = self.client
        except socket.error as e:
            print(f"ERROR: {str(e)}")

    def receive(self):
        while True:
            try:
                data = self.connection.recv(1024)

                decoded_data = pickle.loads(data)
                print(f"Received: {decoded_data:_<30}")

            except pickle.UnpicklingError as e:
                print(f"ERROR -> UnpicklingError: {str(e)}")
            except EOFError:
                print("Connection closed by the server.")
                #break
            except Exception as e:
                print(f"ERROR: {str(e)}")

if __name__ == '__main__':
    n = Network()
    n.connect()
    n.receive()

