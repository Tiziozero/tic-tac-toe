import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection = ("localhost", 8888)
try:
    client_socket.connect(server_connection)  # Use any available network interface and port 8888
except socket.error as e:
    print(str(e))
    quit()


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

finally:

    client_socket.close()
