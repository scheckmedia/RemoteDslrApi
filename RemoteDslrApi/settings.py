from os import getcwd, sep, chdir
from ConfigParser import ConfigParser

class Settings:
    def __init__(self):
        self.__config = {
            "server" : {
                "Address" : "127.0.0.1",
                "Port" : 6666,
                "Debug" : False                                
            }         
        }
                
        self.__config.update(self.__parse_config())
    
    def get_config(self):
        return self.__config
    
    def add_config(self, values):
        self.__config.update(values)
    
    def __parse_config(self):
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