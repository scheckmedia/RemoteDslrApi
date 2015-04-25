import pkgutil
from RemoteDslrApi import routes
from flask.blueprints import Blueprint
from RemoteDslrApi.server import json_app
from RemoteDslrApi.settings import Settings


app = json_app(__name__)

def register_routes():    
    """
    autoload API routes
    """
    package = routes    
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        module = importer.find_module(modname).load_module(modname)
        if ispkg == False:
            for obj in vars(module).values():
                if isinstance(obj, Blueprint):
                    app.register_blueprint(obj, url_prefix='/api')            
        
    

if __name__ == "__main__":         
    register_routes()
    config = Settings().get_config()        
    address = config["server"]["address"]
    port = int(config["server"]["port"])
    debug = config["server"]["port"] in ['True', 'true']    
    app.run(address, port, debug, use_reloader=False, threaded=True)     