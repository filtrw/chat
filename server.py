from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import re
from utils import format_room_message
from database import get_all_rooms, get_room_messages, create_message, create_new_room, delete_message


class _RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/rooms":
            room_list = get_all_rooms()
            self._set_headers()
            self.wfile.write(json.dumps(room_list).encode('utf-8'))
            return

        room_id = re.findall(r'/api/rooms/(\d+)/messages', self.path)
        if len(room_id) > 0:
            message_list = list(map(format_room_message, get_room_messages(room_id[0])))
            self._set_headers()
            self.wfile.write(json.dumps(message_list).encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        payload = json.loads(self.rfile.read(length))
        if self.path == "/api/create-room":
            room_response = create_new_room(payload['roomName'])
            self._set_headers()
            self.wfile.write(json.dumps(room_response).encode('utf-8'))
            return

        room_id = re.findall(r'/api/rooms/(\d+)/message', self.path)
        if len(room_id) > 0:
            message_response = format_room_message(create_message(room_id[0], payload['text']))
            self._set_headers()
            self.wfile.write(json.dumps(message_response).encode('utf-8'))
            return

    def do_DELETE(self):
        message_id = re.findall(r'/api/messages/(\d+)', self.path)
        if len(message_id) > 0:
            delete_message(message_id[0])
            self.send_response(HTTPStatus.OK.value)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()


def run_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
