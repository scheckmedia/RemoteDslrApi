from StringIO import StringIO
import tempfile
import rawpy
import imageio
import base64


class Image:
    def __init__(self, data):                   
        rawfile = tempfile.NamedTemporaryFile()        
        try:            
            io = StringIO(data)
            rawfile.write(io.getvalue())
            rawfile.seek(0)            
            raw = rawpy.imread(rawfile.name)
            rgb = raw.postprocess()
            self.__data = imageio.imwrite(imageio.RETURN_BYTES, rgb, 'jpeg')            
        finally:
            rawfile.close()
    
    @property
    def base64(self):
        return base64.b64encode(self.__data)
