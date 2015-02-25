from SocketServer import ThreadingTCPServer
class Server(SocketServer.ThreadingTCPServer):
    def __init__(self, address, port):
        try:
            self.allow_reuse_address = True
        except Exception as ex:
            print 'Exit'