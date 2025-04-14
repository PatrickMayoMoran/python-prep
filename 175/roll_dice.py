import socket
import random

def parse_path(unparsed_path):
    path, parameter_string = unparsed_path.split('?')
    rolls, sides = parameter_string.split('&')
    _, rolls = rolls.split('=')
    _, sides = sides.split('=')
    query_parameters = { 'rolls': int(rolls), 'sides': int(sides) }
    return path, query_parameters

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 3003))
server_socket.listen()
print('Server is running on localhost:3003')

while True:
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')
    request = client_socket.recv(1024).decode()
    if (not request) or ('favicon.io' in request):
        client_socket.close()
        continue

    request_line = request.splitlines()[0]
    request_line_components = request_line.split(' ')
    request_HTTP_method = request_line_components[0]
    unparsed_path = request_line_components[2]
    path, query_parameters = parse_path(unparsed_path)

    response_body = (
        f"Request: {request_line}\n"
        f"HTTP Method: {request_HTTP_method}\n"
        f"Path: {request_path}\n"
        f"Parameters: {query_parameters}\n"
    )

    rolls = 0
    while rolls < query_parameters['roll']:
        roll = random.randint(1, query_parameters['sides'])
        response_body += f"{roll}\n"
        rolls += 1

    response = ("HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plains\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}\n")


    client_socket.sendall(response.encode())
    client_socket.close()

