from flask import current_app
from werkzeug.exceptions import HTTPException
from gphoto2.gphoto2_result import GPhoto2Error

ERROR_MAP = {
    "-102" : { "http_code" : 404, "description" : "Data is corrupt. This error is reported by camera drivers if corrupted data has been received that can not be automatically handled. Normally, drivers will do everything possible to automatically recover from this error."},
    "-103" : { "http_code" : 404, "description" : "An operation failed because a file existed. This error is reported for example when the user tries to create a file that already exists."},
    "-105" : { "http_code" : 404, "description" : "The specified model could not be found. This error is reported when the user specified a model that does not seem to be supported by any driver."},
    "-107" : { "http_code" : 404, "description" : "The specified directory could not be found. This error is reported when the user specified a directory that is non-existent."},
    "-108" : { "http_code" : 404, "description" : "The specified file could not be found. This error is reported when the user wants to access a file that is non-existent."},
    "-109" : { "http_code" : 404, "description" : "The specified directory already exists. This error is reported for example when the user wants to create a directory that already exists."},
    "-110" : { "http_code" : 404, "description" : "Camera I/O or a command is in progress."},
    "-111" : { "http_code" : 404, "description" : "The specified path is not absolute. This error is reported when the user specifies paths that are not absolute, i.e. paths like \"path/to/directory\". As a rule of thumb, in gphoto2, there is nothing like relative paths."},
    "-112" : { "http_code" : 404, "description" : "A cancellation requestion by the frontend via progress callback and GP_CONTEXT_FEEDBACK_CANCEL was successful and the transfer has been aborted."},
    "-113" : { "http_code" : 404, "description" : "The camera reported some kind of error. This can be either a photographic error, such as failure to autofocus, underexposure, or violating storage permission, anything else that stops the camera from performing the operation."},
    "-114" : { "http_code" : 404, "description" : "There was some sort of OS error in communicating with the camera, e.g. lack of permission for an operation."},
    "-115" : { "http_code" : 404, "description" : "There was not enough free space when uploading a file."},    
}


class RemoteDslrApiError(Exception):
    def __init__(self, message, code):        
        self.message = message
        self.code = code
    
    @staticmethod
    def translate(ex):
        message = {}
        if isinstance(ex, GPhoto2Error):
            key = str(ex.code)
            message["message"] = ex.string             
            if ERROR_MAP.has_key(key):
                o = ERROR_MAP[key]
                message["description"] = o["description"]
                
            message["code"] = ex.code            
            
        return message
        
    @staticmethod
    def handle(ex):
        response = {}
        code = 500        
        if isinstance(ex, GPhoto2Error):
            key = str(ex.code)
            response["message"] = ex.string             
            if ERROR_MAP.has_key(key):
                o = ERROR_MAP[key]
                code = o["http_code"]
                response["description"] = o["description"]
                
            response["status_code"] = code            
        else:            
            response["message"] = ex.message
            
            if hasattr(ex, "description"):
                response["description"] = ex.description
            
            if isinstance(ex, HTTPException) or isinstance(ex, RemoteDslrApiError):
                code = ex.code
                                                
            response["status_code"] = code

        return current_app.fail_response(response), response["status_code"]
