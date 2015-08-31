import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer


class CommandHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'You accessed path: ' + urllib.parse.unquote(self.path).encode('utf8'))


def main():
    server_address = ('', 80)
    httpd = HTTPServer(server_address, CommandHandler)
    sa = httpd.socket.getsockname()
    print('Serving HTTP on', sa[0], 'port', sa[1], '...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nKeyboard interrupt received, exiting.')
        httpd.server_close()
        sys.exit(0)


if __name__ == '__main__':
    main()
