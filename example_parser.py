def parse_http_request(raw_request: str):
    # Разделяем заголовки и тело
    try:
        header_part, body = raw_request.split('\r\n\r\n', 1)
        """HTTP-протокол основан на стандартахи он требует именно \r\n как разделитель строк
        не просто \n. Это из-за исторических причин (ещё с времён Telnet и Windows)."""
    except ValueError:
        header_part = raw_request
        body = ''

    # Разделяем строки заголовков
    lines = header_part.split('\r\n')
    
    # Первая строка — это стартовая строка запроса: METHOD PATH HTTP/VERSION
    request_line = lines[0]
    method, path, http_version = request_line.split(' ', 2)
    
    # Остальные строки — это заголовки
    headers = {}
    for line in lines[1:]:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key.lower()] = value

    return {
        'method': method,
        'path': path,
        'http_version': http_version,
        'headers': headers,
        'body': body
    }

if __name__ == '__main__':
    raw = (
        'POST /submit HTTP/1.1\r\n'
        'Host: localhost\r\n'
        'Content-Type: application/x-www-form-urlencoded\r\n'
        'Content-Length: 13\r\n'
        '\r\n'
        'name=Misha'
    )

    parsed = parse_http_request(raw)
    print('Method:', parsed['method'])
    print('Path:', parsed['path'])
    print('Headers:', parsed['headers'])
    print('Body:', parsed['body'])
