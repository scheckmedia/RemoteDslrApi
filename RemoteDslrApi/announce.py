from zeroconf import Zeroconf, ServiceInfo
import socket
import RemoteDslrApi


class AutoAnnounce(object):
    def __init__(self, port, ssl=False, run=True):
        
        """
        Announces network settings via mdns

        :type self: AutoAnnounce
        :type port: int
        :type ssl: bool
        :type run: bool
        """
        try:
            self.__running = True
            
            protocol = 'http'
            if ssl:
                protocol = 'https'
                
            self.zeroconf = Zeroconf()
            ip, hostname = self.get_local_ip()                        
            desc = {'version': RemoteDslrApi.__version__, 'api_url': protocol + '://' + ip + ':' + str(port) + '/api/', 'url': protocol + '://' + ip + ':' + str(port)}
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
        """
        announces current configuration via mdns

        :type self: AutoAnnounce
        """
        self.zeroconf.register_service(self.service)
                    
    def close(self):
        """
        stop announcing

        :type self: AutoAnnounce
        """
        self.zeroconf.unregister_all_services()
        self.zeroconf.close()
        self.__running = False

    @staticmethod
    def get_local_ip():
        """
        returns current ip and hostname

        :rtype : (string, string)
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
        s.close()
        
        hostname = socket.gethostname()        
        return ip, hostname