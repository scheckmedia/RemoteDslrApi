from flask import Flask, jsonify   
from werkzeug.exceptions import default_exceptions
from RemoteDslrApi.camera import Camera
from RemoteDslrApi.error import RemoteDslrApiError

__all__ = ['json_app']


class Server(Flask):
    def __init__(self, import_name):        
        Flask.__init__(self, import_name)
        self.__camera = Camera()

    def get_camera(self):
        return self.__camera
    
    def success_response(self, param):
        if type(param) is dict:
            param["state"] = "ok"
            return jsonify(param)
    
    def fail_response(self, param):
        if type(param) is dict:
            param["state"] = "fail"
            return jsonify(param)
    
    
def json_app(import_name, **kwargs):    
    app = Server(import_name, **kwargs)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = RemoteDslrApiError.handle
    return app