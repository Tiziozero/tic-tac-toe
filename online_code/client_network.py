import socket
from typing import List
import pickle


#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection = ("localhost", 8888)
#server_connection = ("139.162.200.195", 8888)

# funcs


def setup():
    try:
        client_socket.connect(server_connection)  # use any available network interface and port 8888
        client_socket.send("uwu u".encode())
    except socket.error as e:
        print(str(e))
        print("failed to set up")
        quit()
    print("Set up")

def client_recive():#-> List[List[int]]:
    try:
        data = pickle.loads(client_socket.recv(1024))
        return data
    except pickle.UnpicklingError as e:
        print(f"UnpicklingError: {e}")
        return
    except socket.error as e:
        print(f"Socket Error: {e}")
        return
        # Handle the error appropriately
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return

def client_send(board):
    client_socket.send(pickle.dumps(board))
    
def _test_func():
    try:
        message = [[0,0,0],[0,0,0],[0,0,0]]
        while True:
            try:
                client_socket.send(pickle.dumps(message))
            except:
                print("no data")
            message = client_socket.recv(512)
            
            if message:

                print(f"Received from server: {message}")

    except KeyboardInterrupt:
        print("Client terminated by user.")
        client_socket.send('kys'.encode())

    finally:
        client_socket.close()

if __name__ == '__main__':
    setup()
    _test_func()
