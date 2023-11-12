import socket
import threading
from typing import List
import ast

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection = ("localhost", 8888)

# funcs


def setup():
    try:
        client_socket.connect(server_connection)  # use any available network interface and port 8888
        client_socket.send("uwu u".encode())
    except socket.error as e:
        print(str(e))
        quit()
    print("Set up")

def table_to_str(table):
    return "[" + ",".join("[{}]".format(",".join(map(str, row))) for row in table) + "]"

def string_to_2d_array(input_str):
    try:
        # Safely evaluate the string using ast.literal_eval
        array_2d = ast.literal_eval(input_str)
        
        # Ensure the result is a list of lists
        if isinstance(array_2d, list) and all(isinstance(row, list) for row in array_2d):
            return array_2d

        else:
            raise ValueError("Invalid input: Not a list of lists")
    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}")
        return None

def client_recive():#-> List[List[int]]:
    board = client_socket.recv(512).decode()
    return string_to_2d_array(board)

def client_send(board):
    client_socket.send(table_to_str(board).encode())
    
def _test_func():
    try:
        while True:
            message = input("Enter a message (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode())
            response = client_socket.recv(512).decode()
            print(f"Received from server: {response}")

    except KeyboardInterrupt:
        print("Client terminated by user.")
        client_socket.send('kys'.encode())

    finally:
        client_socket.close()

if __name__ == '__main__':
    setup()
    _test_func()
