import socket

HOST = '0.0.0.0'  # слушаем на всех интерфейсах
PORT = 8080       # можно не быть root (порт 80 без root нельзя взять)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET — протокол уровня IPv4; SOCK_STREAM = TCP 
server_socket.bind((HOST, PORT)) # сервер слушает порт 8080 со всех хостов (замечу: bind принимает кортеж)
server_socket.listen(5) # ждет запросы от клиентов, они становяться в очередь длиной 5

print(f"[*] Сервер запущен на {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept() # accept возвращает данные
    # client_address — это кортеж (ip, port) клиента
    # (пока не придет инфа в accept - поток остановлен и ждет)
    print(f"[+] Подключение от {client_address}")

    request = client_socket.recv(1024).decode() #recv(1024) читает до 1024 байт данных из клиентского соединения. Возвращает байты
    print("[>] Запрос:")
    print(request)

    response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html><body><h1>Привет от Python-сервера!</h1></body></html>
"""
    client_socket.send(response.encode())
    client_socket.close()

