from zeroconf import Zeroconf, ServiceInfo
import socket
import logging
import RemoteDslrApi

class AutoAnnounce(object):
    
    def __init__(self, port, run=True):
        try:
            self.__running = True
            self.zeroconf = Zeroconf()
            ip, hostname = self.get_local_ip()                        
            desc = {'version': RemoteDslrApi.__version__, 'api_url': 'http://' + ip + ':' + str(port) + '/api/', 'url': 'http://' + ip + ':' + str(port)}
            self.service = ServiceInfo("_http._tcp.local.",
                       "RemoteDslrApi._http._tcp.local.",
                       socket.inet_aton(ip), port, 0, 0,
                       desc, hostname)
            
            # logging.basicConfig(level=logging.DEBUG)
            # logging.getLogger('zeroconf').setLevel(logging.DEBUG)
                            
            if run:
                self.run()
        except Exception as ex:
            print ex 
    
    def run(self):        
        self.zeroconf.register_service(self.service)
                    
    def close(self):
        self.zeroconf.unregister_all_services()
        self.zeroconf.close()
        self.__running = False

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
        s.close()
        
        hostname = socket.gethostname()        
        return ip, hostname