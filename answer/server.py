import socket

from log import get_logger
from parser import define_instrument, parsed_to_text

from config import HOST, PORT, LOGGER_NAME

def main():
    # get my custom rainbow logger
    logger = get_logger(LOGGER_NAME, filename='answer/logs.log', mode='w')

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
        parsed = define_instrument(request)
        parsed_text = parsed_to_text(parsed)
        logger.debug(f'[>] Request: {parsed_text}')

        if parsed.get('method') == 'GET':
            if parsed.get('path') == '/':
                file = 'answer/static/index.html'
                status = 200
            else:
                file = 'answer/static/not_found.html'
                status = 404
        else:
            file = 'answer/static/server_error.html'
            status = 500
        # read html and send answer
        with open(file, 'r') as f:
                response = f.read()
        
        logger.info(f'[>] Request processed\nIP: {client_address[0]}, Path: {parsed.get("path")}, Status: {status}')

        client_socket.send(response.encode())
        client_socket.close()

if __name__ == '__main__':
    main()
