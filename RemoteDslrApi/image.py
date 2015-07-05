import base64
from enum import IntEnum
from PIL import Image as pImage
from io import BytesIO
from flask.json import JSONEncoder
from gi.repository import GExiv2


class PreviewSize(IntEnum):
    small = 0
    medium = 1
    big = 2


class ImagePath():
    def __init__(self, folder, name):
        self.folder = folder
        self.name = name
        self.exif = {}


class Image(JSONEncoder):
    """
    Representation of an Image from a camera
    """
    def __init__(self, data=None, path="", preview_size=PreviewSize.big):    
        """
        Initializes this instance of an image

        :param data: byte data which representing an image
        :type data: str
        :param path: path of an image
        :type path: RemoteDslrApi.image.ImagePath
        :param preview_size:
        :type preview_size: RemoteDslrApi.image.PreviewSize
        """
        self.__path = path.folder + '/' + path.name
        if data is not None:            
            self.__to_jpeg(preview_size, data)            
    
    @property
    def base64(self):
        """
        retruns an image as base64 encoded string
        :return: base64 encoded string
        :rtype: str
        """
        return base64.b64encode(self.__data)
    
    @property
    def path(self):
        """
        returns the path of a camera for an image

        :return: image path
        :rtype: str
        """
        return self.__path
    
    @property
    def serialize(self):
        """
        serializes an image to an dictionary

        :return: serialized image
        :rtype: dict
        """
        return {
            "image" : self.base64,
            "metadata" : self.exif
        }
    
    def __to_jpeg(self, preview_size, data):
        exif = GExiv2.Metadata()
        exif.open_buf(data)
        props = exif.get_preview_properties()
        prop = props[preview_size]
        raw = exif.get_preview_image(prop)
        
        data = BytesIO(raw.get_data())
        write_data = BytesIO()        
        pImage.open(data).save(write_data, "JPEG")        
        self.__data = write_data.getvalue()  
        self.__extract_exif(exif)   
        
    def __extract_exif(self, exif):
        self.exif = {
            "date": str(exif.get_date_time()),
            "exposure_time": str(exif.get_exposure_time()),
            "fnumber": float(exif.get_fnumber()),
            "focal_length": float(exif.get_focal_length()),
            "iso": int(exif.get_iso_speed()),
            "mime_type": str(exif.get_mime_type()),
            "orientation": str(exif.get_orientation().value_nick),
            "height": int(exif.get_pixel_height()),
            "width": int(exif.get_pixel_width()),
            "gps": {
                "info": str(exif.get_gps_info()),
                "altitude": float(exif.get_gps_altitude()),
                "latitude": float(exif.get_gps_latitude()),
                "longitude": float(exif.get_gps_longitude())
            }
        }