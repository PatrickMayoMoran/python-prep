import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 3003))
server_socket.listen()
print('Server is running on localhost:3003')

while True:
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')
    request = client_socket.recv(1024).decode()

