import socket
server_ip = 'localhost'
#server_ip = '139.162.200.195' #when on server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, 8888))
server.listen(5)
