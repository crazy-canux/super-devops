.. _socket:

SocketServer
============

SocketServer
python2叫SocketServer,python3改名为socketserver.

一般的socket server的类, client可以通过socket来实现．

usage
-----

import::

    import SocketServer

class BaseRequestHandler::

    BaseRequestHandler(self, request, client_address, server)

class BaseServer::

    BaseServer(?)

class StreamRequestHandler::

    StreamRequestHandler(BaseRequestHandler)
    self.rfile
    self.wfile
    # methods:
    handle(self) # 子类重写该方法
    finish(self)
    setup(self)

class TCPServer::

    TCPServer(BaseServer)
    TCPServer(server_address, RequestHandlerClass, bind_and_activate=True)
    # methods:
    serve_forever(poll_interval=0.5)
    shutdown()
    handle_request()
    fileno()
    ...
    # Instance variables:
    server_address
    RequestHandlerClass
    socket
    # Class variables:
    timeout
    ...

class DatagramRequestHandler::

    DatagramRequestHandler(BaseRequestHandler)
    self.request
    self.client_address
    self.server
    # methods:
    handle(self) # 子类重写该方法
    finish(self)
    setup(self)

class UDPServer::

    UDPServer(TCPServer)
    UDPServer(server_address, RequestHandlerClass, bind_and_activate=True)
    # methods:
    serve_forever(self, poll_interval
