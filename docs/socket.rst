.. _socket:

SocketServer
============

python3改名为socketserver.

sockeet 服务器开发的框架.

usage
-----

import::

    import SocketServer

class BaseRequestHandler::

    BaseRequestHandler(self, request, client_address, server)

class StreamRequestHandler::

    StreamRequestHandler(BaseRequestHandler)
    self.rfile
    self.wfile
    # methods:
    handle(self) # 子类重写该方法
    finish(self)
    setup(self)
    
 class DatagramRequestHandler::

    DatagramRequestHandler(BaseRequestHandler)
    self.request
    self.client_address
    self.server
    # methods:
    handle(self) # 子类重写该方法
    finish(self)
    setup(self)
    
class BaseServer::

    BaseServer(?)

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

class UDPServer::

    UDPServer(TCPServer)
    UDPServer(server_address, RequestHandlerClass, bind_and_activate=True)
    # methods:
    serve_forever(self, poll_interval
 
