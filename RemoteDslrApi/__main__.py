import pkgutil
from os import path
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
    use_ssl = config["server"]["ssl"] in ['True', 'true']  
    auto_announce = config["general"]["auto_announce"] in ['True', 'true']
    if auto_announce:
        announce = AutoAnnounce(port)
    
    options = {
               'debug': debug,
               'use_reloader': False,
               'threaded': True,
               
               }
    
    if use_ssl:
        abs_path = path.dirname(path.abspath(__file__)) + "/../"
        cert_file = abs_path + config["server"]["ssl_crt"]
        key_file = abs_path + config["server"]["ssl_key"]        
        ssl_context = (cert_file, key_file)
        options['ssl_context'] = ssl_context
                    
    app.run(address, port, **options)     