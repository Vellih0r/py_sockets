import socket

from log import get_logger
from parser import define_instrument, parsed_to_text

from config import HOST, PORT, LOGGER_NAME

def main():
    # get my custom rainbow logger
    logger = get_logger(LOGGER_NAME, filename='src/logs.log', mode='w')

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info('server socket created successfuly')
    except socket.error :
        logger.exception('[x] socket creation failed with error')
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    logger.info(f'[*] server is up on {HOST}:{PORT}')

    while True:
        client_socket, client_address = server_socket.accept() # connect client
        logger.info(f'[+] Connection from {client_address}')

        request = client_socket.recv(1024).decode() # get client request
        parsed_text = parsed_to_text(define_instrument(request))
        logger.info(f'[>] Request\n{parsed_text}')

        response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html><body><h1>What's a craic?</h1></body></html>
"""

        client_socket.send(response.encode())
        client_socket.close()

if __name__ == '__main__':
    main()