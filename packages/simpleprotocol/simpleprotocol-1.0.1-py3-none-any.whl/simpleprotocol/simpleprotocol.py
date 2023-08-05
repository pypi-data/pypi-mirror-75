from . import socketwrapper
from . import message

LOG = False

class SimpleServer():

    def __init__(self, port):
        self.port = port
        self.socket = socketwrapper.ServerSocket(port=port)

    def accept(self):
        return _SimpleProtocolForServer(self.socket.getClientObject())

class SimpleProtocol():

    def __init__(self, port):
        self.socket = socketwrapper.ClientSocket(port=port)
        self.message = message.Message(socket=self.socket)

    def send(self, *args, **kwargs):
        return self.message.send(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.message.get(*args, **kwargs)

class _SimpleProtocolForServer(SimpleProtocol):

    def __init__(self, socket):
        self.socket = socket
        self.message = message.Message(socket=self.socket)
