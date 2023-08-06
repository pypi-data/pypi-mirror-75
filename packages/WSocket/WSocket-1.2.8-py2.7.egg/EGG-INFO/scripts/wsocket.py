#!python
# -*- coding: utf-8 -*-

"""# WSocket
**HTTP and Websocket both supported server(WSGI)**

Server(WSGI) creates and listens at the HTTP
socket, dispatching the requests to a handler. 
this is only use standard python libraries. 
also: 
this is a plugin to ServerLight Framework.
"""

try:
    from sl.server import WSGIRequestHandler, ServerHandler
except ImportError:
    from wsgiref.simple_server import WSGIRequestHandler, ServerHandler

import sys
import struct
from base64 import b64encode
from hashlib import sha1
import logging
from socket import error as SocketError
import errno

logger = logging.getLogger(__name__)
logging.basicConfig()

__all__ = ['WebSocketHandler']
__version__ = '1.0.0'

'''
+-+-+-+-+-------+-+-------------+-------------------------------+
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
'''

FIN    = 0x80
OPCODE = 0x0f
MASKED = 0x80
PAYLOAD_LEN = 0x7f
PAYLOAD_LEN_EXT16 = 0x7e
PAYLOAD_LEN_EXT64 = 0x7f

OPCODE_CONTINUATION = 0x0
OPCODE_TEXT         = 0x1
OPCODE_BINARY       = 0x2
OPCODE_CLOSE_CONN   = 0x8
OPCODE_PING         = 0x9
OPCODE_PONG         = 0xA


class WebSocketHandler(WSGIRequestHandler):

    """Simple HTTP and WebSocket Handler.

    This can communicate through websocket using wsgi framework. And 
    handle HTTP requests with wsgi framework as normal server.

    Automatically upgrades the connection to a websocket.
    """
    
    ws=False
    
    def get_environ(self):
        """
        Add websocket to WSGI environment.
        """
        env = WSGIRequestHandler.get_environ(self)
        if self.handshake_done:
            env['wsgi.websocket_version'] = \
                env.get('HTTP_SEC_WEBSOCKET_VERSION')
            env['wsgi.websocket'] = self
        return env
    
    def setup(self):
        WSGIRequestHandler.setup(self)
        self.keep_alive = True
        self.handshake_done = False
        self.valid_client = False
    
    def handle(self):
        """Handle a single HTTP request"""
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return
        if not self.parse_request(): # An error code has been sent, just exit
            return
        if not self.handshake_done:
            self.handshake()
        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())
    
    def handshake(self):
        headers = self.headers

        try:
            assert headers['upgrade'].lower() == 'websocket'
        except:
            self.keep_alive = False
            return

        try:
            key = headers['sec-websocket-key']
        except KeyError:
            logger.warning("Client tried to connect but was missing a key")
            self.keep_alive = False
            return

        response = self.make_handshake_response(key)
        self.handshake_done = self.request.send(response.encode())
        self.valid_client = True
    
    @classmethod
    def make_handshake_response(cls, key):
        return \
          'HTTP/1.1 101 Switching Protocols\r\n'\
          'Upgrade: websocket\r\n'              \
          'Connection: Upgrade\r\n'             \
          'Sec-WebSocket-Accept: %s\r\n'        \
          '\r\n' % cls.calculate_response_key(key)
    
    @classmethod
    def calculate_response_key(cls, key):
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        hash = sha1(key.encode() + GUID.encode())
        response_key = b64encode(hash.digest()).strip()
        return response_key.decode('ASCII')

    def receive(self):
        try:
            b1, b2 = self.read_bytes(2)
        except SocketError as e:  # to be replaced with ConnectionResetError for py3
            if e.errno == errno.ECONNRESET:
                logger.info("Client closed connection.")
                self.keep_alive = 0
                return
            b1, b2 = 0, 0
        except ValueError as e:
            b1, b2 = 0, 0

        fin    = b1 & FIN
        opcode = b1 & OPCODE
        masked = b2 & MASKED
        payload_length = b2 & PAYLOAD_LEN

        if opcode == OPCODE_CLOSE_CONN:
            logger.debug('Client asked to close connection.')
            self.keep_alive = 0
            return
        if not masked:
            logger.debug('Client must always be masked.')
            self.keep_alive = 0
            return
        if opcode == OPCODE_CONTINUATION:
            logger.debug('Continuation frames are not supported.')
            return
        elif opcode == OPCODE_BINARY:
            logger.debug('Binary frames are not supported.')
            return
        elif opcode == OPCODE_TEXT:
            opcode_handler = self._message_received_
        elif opcode == OPCODE_PING:
            opcode_handler = self.send_pong
        elif opcode == OPCODE_PONG:
            opcode_handler = self._pong_received_
        else:
            logger.debug('Unknown opcode %#x.' % opcode)
            self.keep_alive = 0
            return

        if payload_length == 126:
            payload_length = struct.unpack(">H", self.rfile.read(2))[0]
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", self.rfile.read(8))[0]

        masks = self.read_bytes(4)
        message_bytes = bytearray()
        for message_byte in self.read_bytes(payload_length):
            message_byte ^= masks[len(message_bytes) % 4]
            message_bytes.append(message_byte)
        try:
            return opcode_handler(str(message_bytes.decode('utf8')))
        except:
            return opcode_handler(unicode(message_bytes.decode('utf8')))

    def _message_received_(self, msg):
        return msg

    def send_pong(self, msg):
        self.send(message, OPCODE_PONG)
        return

    def fake(self, *args, **kwargs):
        pass

    def _pong_received_(self, msg):
        return

    def read_bytes(self, num):

        # python3 gives ordinal of byte directly

        bytes = self.rfile.read(num)
        if sys.version_info[0x0] < 3:
            return map(ord, bytes)
        else:
            return bytes

    def send(self, message, opcode=OPCODE_TEXT):
        """
        Important: Fragmented(=continuation) messages are not supported since
        their usage cases are limited - when we don't know the payload length.
        """
        # Validate message
        if isinstance(message, bytes):
            message = try_decode_UTF8(message)  # this is slower but ensures we have UTF-8
            if not message:
                logger.warning("Can\'t send message, message is not valid UTF-8")
                return False
        elif sys.version_info < (3,0) and (isinstance(message, str) or isinstance(message, unicode)):
            pass
        elif isinstance(message, str):
            pass
        else:
            logger.warning('Can\'t send message, message has to be a string or bytes. Given type is %s' % type(message))
            return False
        header  = bytearray()
        payload = encode_to_UTF8(message)
        payload_length = len(payload)

        # Normal payload
        if payload_length <= 125:
            header.append(FIN | opcode)
            header.append(payload_length)

        # Extended payload
        elif payload_length >= 126 and payload_length <= 65535:
            header.append(FIN | opcode)
            header.append(PAYLOAD_LEN_EXT16)
            header.extend(struct.pack(">H", payload_length))

        # Huge extended payload
        elif payload_length < 18446744073709551616:
            header.append(FIN | opcode)
            header.append(PAYLOAD_LEN_EXT64)
            header.extend(struct.pack(">Q", payload_length))

        else:
            raise Exception("Message is too big. Consider breaking it into chunks.")
            return

        self.request.send(header + payload)

    def finish_response(self):
        if hasattr(self.s.result, 'close'):
            self.s.result.close()
        self.s.close()
    
    def __del__(self):
        try:
            self.close()
        except:
            # close() may fail if __init__ didn't complete
            pass

    @property
    def current_app(self):
        return self.server.get_app()

    @property
    def origin(self):
        return self.env.get('HTTP_ORIGIN')

    @property
    def protocol(self):
        return self.env.get('HTTP_SEC_WEBSOCKET_PROTOCOL')

    @property
    def version(self):
        return self.env.get('HTTP_SEC_WEBSOCKET_VERSION')

    @property
    def logger(self):
        return logger

def encode_to_UTF8(data):
    try:
        return data.encode('UTF-8')
    except UnicodeEncodeError as e:
        logger.debug('Could not encode data to UTF-8 -- %s' % e)
        return False
    except Exception as e:
        raise e
        return False


def try_decode_UTF8(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return False
    except Exception as e:
        raise e
