import socket
import pickle
import threading

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = 'localhost', 8888
        self.ongoing = True

    def connect(self):
        try:
            self.client.connect((self.ip, self.port))
            print(f"Successfully connected to {self.ip}:{self.port}")
            message = pickle.loads(self.client.recv(1024))
            print(f"Server: {message}")

            recv_thread = threading.Thread(target=self.receive, args=())
            send_thread = threading.Thread(target=self.send, args=())
            stop_con_thread = threading.Thread(target=self.stop_connection, args=())

            recv_thread.start()
            send_thread.start()
            stop_con_thread.start()

        except socket.error as e:
            print(f"ERROR: {str(e)}")

    def stop_connection(self):
        while self.ongoing:
            try:
                pass
            except KeyboardInterrupt:
                print("Keyboard Interrupt. Closing connection")
                self.ongoing = False
                self.client.close()
                break
        print("end stop_connection thread")
        quit()

    def receive(self):
        while self.ongoing:
            if self.ongoing:
                try:
                    data = self.client.recv(1024)
                    try:
                        decoded_data = pickle.loads(data)
                        print(f"Received: {decoded_data}")
                    except:
                        pass
                except (socket.error, ConnectionResetError):
                    print("Connection closed by the server.")
                    self.ongoing = False
                    self.client.close()
                    #break
                except pickle.UnpicklingError as e:
                    print(f"ERROR -> UnpicklingError: {str(e)}")
                except EOFError:
                    print("Connection closed by the server.")
                    self.ongoing = False
                    self.client.close()
                    #break
                except Exception as e:
                    print(f"ERROR: {str(e)}")
                except:
                    print("no")
        print("3nd recive thread")

    def send(self):
        while self.ongoing:
            try:
                coords = input("Enter coordinates (e.g., x,y): ")
                if coords == 'quit':
                    self.client.send(pickle.dumps("quti_server_connection"))
                    self.ongoing = False
                    self.client.close()
                    break
                coords = tuple(map(int, coords.split(',')))

                self.client.sendall(pickle.dumps(coords))
            except (socket.error, ConnectionResetError):
                print("Connection closed by the server.")
                self.ongoing = False
                break
            except Exception as e:
                print(f"ERROR: {str(e)}")
        print("end send thread")

if __name__ == '__main__':
    c = Client()
    c.connect()

