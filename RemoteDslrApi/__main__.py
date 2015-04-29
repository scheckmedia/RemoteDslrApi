import pkgutil
from RemoteDslrApi import routes
from flask.blueprints import Blueprint
from RemoteDslrApi.server import json_app
from RemoteDslrApi.settings import Settings
from RemoteDslrApi.auto_announce import AutoAnnounce
 
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
    auto_announce = config["general"]["auto_announce"] in ['True', 'true']
    if(auto_announce):
        announce = AutoAnnounce(port)
        
    app.run(address, port, debug, use_reloader=False, threaded=True)     