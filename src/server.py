import socket

from config import HOST, PORT, LOGGER_NAME
from log import get_logger
# get my custom rainbow logger
logger = get_logger(LOGGER_NAME)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

