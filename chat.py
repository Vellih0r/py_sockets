import socket
import threading
import logging

HOST = '0.0.0.0'
PORT = 9090

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%D %H:%m:%S')

def forward_messages(sender, reciver, name):
    # recieve from sender and send to reciever
    try:
        while True:
            data = sender.recv(1024).decode()
            if not data:
                break
            data = f'--\nUser: {name}\n{data}'.encode()
            reciver.sendall(data)
    except Exception as e:
        logging.error(f'[!] Exception in {name}, error - {e}')
    finally:
        sender.close()
        reciver.close()
    
def main():
    # CREATE SERVER SOCKET WICH WILL SERVE CLIENTS
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info('server socket created successfuly')
    except socket.error:
        logging.exception('[x] socket creation failed with error')
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)

    # connect clients
    logging.info('Waiting for Misha...')
    misha, misha_address = server_socket.accept()
    logging.info(f'[+] Misha joined {misha_address}')

    logging.info('Waiting for Tyoma...')
    tyoma, tyoma_address = server_socket.accept()
    logging.info(f'[+] Tyoma joined {misha_address}')

    thread1 = threading.Thread(target=forward_messages, args=(misha, tyoma, "Vellih0r"))
    thread2 = threading.Thread(target=forward_messages, args=(tyoma, misha, "Shadoww"))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    server_socket.close()
    logging.warning('Server closed')

if __name__ == '__main__':
    main()

