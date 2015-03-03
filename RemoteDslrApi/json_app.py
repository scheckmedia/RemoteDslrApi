from flask import Flask    
from werkzeug.exceptions import default_exceptions
from RemoteDslrApi.camera_controller import CameraController
from RemoteDslrApi.error import RemoteDslrApiError

__all__ = ['json_app']

class Server(Flask):
    def __init__(self, import_name):        
        Flask.__init__(self, import_name)
        self.__camera = CameraController()

    def get_camera(self):
        return self.__camera

def json_app(import_name, **kwargs):    
    app = Server(import_name, **kwargs)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = RemoteDslrApiError.handle
    return app