from StringIO import StringIO
import tempfile
import rawpy
import imageio
import base64
import re
from flask.json import JSONEncoder


class Image(JSONEncoder):
    def __init__(self, data = None, path = ""):
        if(data != None):                
            match = re.search('jpeg|jpg', path.name, re.IGNORECASE)                
            if(match):
                self.__data = data
            else:
                self.__data = self.__decode_raw(data)            
        
        self.__path = path.folder + '/' + path.name                                    
    
    @property
    def base64(self):
        return base64.b64encode(self.__data)
    
    @property
    def path(self):
        return self.__path
    
    def __decode_raw(self, data):
        rawfile = tempfile.NamedTemporaryFile()
        try:
            io = StringIO(data)
            rawfile.write(io.getvalue())
            rawfile.seek(0)            
            raw = rawpy.imread(rawfile.name)
            rgb = raw.postprocess()
            return imageio.imwrite(imageio.RETURN_BYTES, rgb, 'jpeg')
        finally:
            rawfile.close()
            return None        
