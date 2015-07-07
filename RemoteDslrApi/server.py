from os import path
from flask import Flask, jsonify, request, Response
from werkzeug.exceptions import default_exceptions
from RemoteDslrApi import routes
from RemoteDslrApi.camera import Camera
from RemoteDslrApi.error import RemoteDslrApiError
from RemoteDslrApi.announce import AutoAnnounce
from RemoteDslrApi.settings import Settings
from flask.blueprints import Blueprint
from functools import wraps
import pkgutil

__all__ = ['json_app']


class Server(Flask):
    """
     A customized HTTP-Server based on Flask
    """
    def __init__(self, import_name):
        Flask.__init__(self, import_name)
        self.__camera = Camera()
        self.__register_routes()
        self.__configure()

    def __configure(self):
        for code in default_exceptions.iterkeys():
            self.error_handler_spec[None][code] = RemoteDslrApiError.handle

        config = Settings().get_config
        self.address = config["server"]["address"]
        self.port = int(config["server"]["port"])
        self.debug = config["server"]["port"] in ['True', 'true']
        use_ssl = config["server"]["ssl"] in ['True', 'true']
        auto_announce = config["general"]["auto_announce"] in ['True', 'true']
        if auto_announce:
            AutoAnnounce(self.port, use_ssl)

        self.options = {
            'use_reloader': False,
            'threaded': True
        }

        if use_ssl:
            abs_path = path.dirname(path.abspath(__file__)) + "/../"
            cert_file = abs_path + config["server"]["ssl_crt"]
            key_file = abs_path + config["server"]["ssl_key"]
            ssl_context = (cert_file, key_file)
            self.options['ssl_context'] = ssl_context

    def start(self):
        """
        start http services
        """
        self.run(self.address, self.port, self.debug, **self.options)

    def stop(self):
        self.__camera.__exit__()

    def set_camera(self, camera):
        """
        set current camera instance

        :type camera: RemoteDslrApi.Camera
        :param camera: camera instance
        """
        self.__camera = camera

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

    def __register_routes(self):
        """
        autoload API routes
        """
        package = routes
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            module = importer.find_module(modname).load_module(modname)
            if not ispkg:
                for obj in vars(module).values():
                    if isinstance(obj, Blueprint):
                        self.register_blueprint(obj, url_prefix='/api')

    @staticmethod
    def auth(f):
        """
        function decorator to authticate with http basic auth
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            config = Settings().get_config
            enabled = config["security"]["protected"] in ['True', 'true']
            username = config["security"]["username"]
            password = config["security"]["password"]

            auth = request.authorization

            if enabled is True and not (username == auth.username and password == auth.password):
                raise RemoteDslrApiError("invalid login", 401)

            return f(*args, **kwargs)

        return wrapper
