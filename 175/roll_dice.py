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
    unparsed_path = request_line_components[1]
    request_path, query_parameters = parse_path(unparsed_path)

    response_body = ("<html><head><title>Dice Rolls</title></head><body>"
                      "<h1>HTTP Request Information</h1>"
                      f"<p><strong>Request Line:</strong> {request_line}</p>"
                      f"<p><strong>HTTP Method:</strong> {request_HTTP_method}</p>"
                      f"<p><strong>Path:</strong> {request_path}</p>"
                      f"<p><strong>Parameters:</strong> {query_parameters}</p>"
                      "<h2>Dice Rolls</h2>"
                      "<ul>")

    rolls = 0
    while rolls < query_parameters['rolls']:
        roll = random.randint(1, query_parameters['sides'])
        response_body += f"<li>Roll: {roll}</li>"
        rolls += 1

    response_body += "</ul></body></html>"

    response = ("HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}\n")


    client_socket.sendall(response.encode())
    client_socket.close()

