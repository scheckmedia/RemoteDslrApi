import pkgutil
from os import getcwd, sep, chdir
from ConfigParser import ConfigParser
from flask import Flask
from RemoteDslrApi import routes
from flask.blueprints import Blueprint
from RemoteDslrApi.json_app import json_app
    


app = json_app(__name__)

def parseConfig():
    chdir('..')
    path = "%s%sconfig.ini" % (getcwd(), sep)       
    parser = ConfigParser()
    parser.read(path)    
    config = {}
    for section in parser.sections():
        config.update({section : {}})
        for option in parser.options(section):
            val = parser.get(section, option)
            if val != -1:
                config[section][option] = val 
    return config

def registerApi():    
    package = routes
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        module = importer.find_module(modname).load_module(modname)
        for obj in vars(module).values():
            if isinstance(obj, Blueprint):
                app.register_blueprint(obj, url_prefix='/api')            
        
    

if __name__ == "__main__":
    registerApi()
    config = parseConfig()        
    address = config["server"]["address"]
    port = int(config["server"]["port"])    
    app.run(address, port, True, use_reloader=False)    