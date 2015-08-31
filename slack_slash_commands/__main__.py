import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer


class CommandHandler(BaseHTTPRequestHandler):
    def _get_parameters(self):
        if not hasattr(self, '__parameters') or not self.__parameters:
            query = urllib.parse.urlparse(self.path).query
            self.__parameters = dict(qc.split('=') for qc in query.split('&')) if query else {}
        return self.__parameters

    def _get_parameter(self, parameter):
        return self._get_parameters().get(parameter)

    def _handle_command(self, command, text):
        return '/{} `{}`'.format(command, text)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        command = self._get_parameter('command')[3:]
        text = self._get_parameter('text')
        reply = self._handle_command(command, text)
        if isinstance(reply, str):
            reply = reply.encode()
        self.wfile.write(b'Reply: ' + reply)


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
