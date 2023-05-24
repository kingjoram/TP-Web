def parameters(environ, start_response):
    status = '200 OK'
    print(environ)
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return

application = parameters
