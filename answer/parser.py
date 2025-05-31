def parse_http_request(request: str) -> dict:
    """
    Parse http request
    If request is correct, will return {method, path, http_version, headers, body}
    If request is invalid will return {'invalid_request' : request}
    """
    # separate header from body (\r\n\r\n is standart separator in http)
    try:
        header_part, body = request.split('\r\n\r\n', 1)
    except ValueError:
        header_part = request
        body = ''

    # separate header lines
    lines = header_part.split('\r\n')
    # first line is METHOD PATH HTTP_VERSION
    try:
        method, path, http_version = lines[0].split(' ', 2)
    except ValueError:
        # if request not in standart, it's probably come from telnet
        return {'invalid_request' : request}
    
    # other lines are headers
    headers = {}
    for line in lines[1:]:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key.lower()] = value

    return {
        'method' : method,
        'path' : path,
        'http_version' : http_version,
        'headers' : headers,
        'body' : body
    }

def define_instrument(request):
    """
    Extends parse_http_request functions
    Define is request sended by curl, telnet, browser or something else
    If request is correct, will return {method, path, http_version, headers, body, instrument}
    Else will return {'invalid_request' : request, instument : 'unknown'}
    """
    parsed = parse_http_request(request)


    if 'invalid_request' in parsed:
        parsed['instrument'] = 'telnet'

    else:
        try:
            user_agent = parsed['headers']['user-agent'].lower()
        except (KeyError, AttributeError):
            parsed['instrument'] = 'unknown'
            return parsed
        
        if 'curl' in user_agent:
            parsed['instrument'] = 'curl'
        elif 'mozilla' in user_agent or 'chrome' in user_agent:
            parsed['instrument'] = 'browser'
        else:
            parsed['instrument'] = 'unknown'


    return parsed

def parsed_to_text(parsed):
        """
        Prints parsed request
        If request is correct it will print out every key(method, path, etc.)
        """
        text = 'PARSED:\n'
        if 'invalid_request' in parsed:
            text += f'{parsed}\n'
            return text

        else:
            try:
                text += f'Instrument: {parsed["instrument"]}\n'
            except (KeyError, AttributeError):
                pass
            text += f'Method:{parsed["method"]}\n'
            text += f'Path: {parsed["path"]}\n'
            text += f'Headers: {parsed["headers"]}\n'
            text += f'Body: {parsed["body"]}'
        

        return text


if __name__ == '__main__':
    raw1 = (
        'POST /submit HTTP/1.1\r\n'
        'Host: localhost\r\n'
        'Content-Type: application/x-www-form-urlencoded\r\n'
        'User-Agent: Curl 5.5\r\n'
        'Content-Length: 13\r\n'
        '\r\n'
        'name=Misha'
    )
    raw2 = 'aboba'

    parsed1 = define_instrument(raw1)
    parsed2 = define_instrument(raw2)
    print(parsed_to_text(parsed1))
    print(parsed_to_text(parsed2))
