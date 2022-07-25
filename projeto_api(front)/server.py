
def app(amb, start_response):
    arq = open('cadastro.html', 'rb')
    data = arq.read()
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [data]

#waitress-serve --listen=127.0.0.1:5002 server:app

def app2(amb, start_response):
    arq = open('login.html', 'rb')
    data = arq.read()
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [data]

#waitress-serve --listen=127.0.0.1:5003 server:app2

def app3(amb, start_response):
    arq = open('home.html', 'rb')
    data = arq.read()
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [data]


#waitress-serve --listen=127.0.0.1:5004 server:app3

