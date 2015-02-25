"""

"""
from SocketServer import BaseRequestHandler
from commands import command
import json

class Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            data = json.loads(self.request.recv(40960).strip())
            result = self.__buildResponse({})
            self.request.sendall(result)
        except Exception as ex:
            self.request.sendall(json.dumps({'status':'fail', 'message' : ex.message}))

    def __buildResponse(self, data):
        response = { 'status' : 'ok', 'data' : data }
        return json.dumps(response)