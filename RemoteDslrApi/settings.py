from os import path
from ConfigParser import ConfigParser


class Settings:
    """
    Responsible for parsing configuration values
    """
    def __init__(self):
        self.__config = {
            "general": {
                "auto_announce": True
            },
            "server": {
                "address": "127.0.0.1",
                "port": 6666,
                "debug": False,
                "ssl": False,
                "ssl_key": "ssl/server.key",
                "ssl_crt": "ssl/server.crt"
            },
            "security": {
                "protected": False,
                "username": "admin",
                "password": "123456"
            }
        }
                
        self.__config.update(self.__parse_config())
    
    @property
    def get_config(self):
        """
        returns the current configuration

        :return: configuration
        :rtype: dict
        """
        return self.__config

    def __parse_config(self):
        abs_path = path.dirname(path.abspath(__file__)) + "/"
        config_file = "%sconfig.ini" % abs_path        
        parser = ConfigParser()
        parser.read(config_file)
        config = {}
        for section in parser.sections():
            config.update({section: {}})
            for option in parser.options(section):
                val = parser.get(section, option)
                if val != -1:
                    config[section][option] = val 
        return config
