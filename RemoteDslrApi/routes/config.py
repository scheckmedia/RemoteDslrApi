from flask import Blueprint, request, current_app
import json
from RemoteDslrApi.error import RemoteDslrApiError
from RemoteDslrApi.server import Server

"""
@api {get} /api/config/list List
@apiName GetConfig
@apiGroup Config
@apiDescription Returns a list of the current configuration

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""
list_config_page = Blueprint('list_config', __name__)
@list_config_page.route('/config/list', methods=['GET'])
@Server.auth
def list_config():
    camera = current_app.get_camera()
    return current_app.success_response(camera.get_config()), 200

"""
@api {get} /api/config/get/:key Get Custom Value
@apiName GetConfigByKey
@apiGroup Config
@apiDescription Returns a value of a key or a list of values for a list of keys

@apiParam {Object} value    settings key(s) to get value
@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    
@apiParamExample {json} Request-Example:
{
    "value" : "shutterspeed2"
}

or

{
    "value" : ["shutterspeed2", "iso", "f-number"]
}       
"""
config_by_value = Blueprint('config_by_value', __name__)
@config_by_value.route('/config/get/<key>', methods=['get'])
@Server.auth
def get_config_by_key(key):
    camera = current_app.get_camera()
    data = str(key).split(",")
    return current_app.success_response(camera.get_config_value(data)), 200



"""
@api {put} /api/config/aperture Aperture
@apiName SetAperture
@apiGroup Config
@apiDescription Updates Aperture value for a connected Camera

@apiParam {Object} value    ISO value
@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK
    
@apiParamExample {json} Request-Example:
{
    "value" : "f\/10"
}
"""
config_aperture_page = Blueprint('config_aperture', __name__)
@config_aperture_page.route('/config/aperture/', methods=['PUT'])
@Server.auth
def aperture():    
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data)    
    camera.set_config_value("f-number", value)
    return current_app.success_response({}), 201

"""
@api {put} /api/config/iso ISO
@apiName SetISO
@apiGroup Config
@apiDescription Updates ISO value for a connected Camera

@apiParam {Object} value    ISO value
@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK

@apiParamExample {json} Request-Example:
{
    "value" : "400"
}
"""
config_iso_page = Blueprint('config_iso', __name__)
@config_iso_page.route('/config/iso/', methods=['PUT'])
@Server.auth
def iso():    
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data)    
    camera.set_config_value("iso", value)
    return current_app.success_response({}), 201


"""
@api {put} /api/config/shutterspeed Shutter speed
@apiName SetShutterSpeed
@apiGroup Config
@apiDescription Updates Shutter speed value for a connected Camera 

@apiParam {Object} value    shutter speed value
@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK

@apiParamExample {json} Request-Example:
{
    "value" : "1\/128"
}
"""
config_shutter_speed_page = Blueprint('config_shutter_speed', __name__)
@config_shutter_speed_page.route('/config/shutterspeed/', methods=['PUT'])
@Server.auth
def shutter_speed():    
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data)
    
    camera.set_config_value("shutterspeed2", value)  
    
    return current_app.success_response({}), 201

"""
@api {put} /api/config/set/:key Set Custom Value
@apiName SetKeyValue
@apiGroup Config
@apiDescription Updates Camera configuration with a key value pair from listconfig settings

@apiParam {String} key      configuration key
@apiParam {Object} value    value for key
@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK

@apiParamExample {json} Request-Example:
{
    "value" : "1\/128"
}
"""
config_custom_key_value = Blueprint('config_custom_key_value', __name__)
@config_custom_key_value.route('/config/set/<key>', methods=['PUT'])
@Server.auth
def key_value(key):    
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data)
    
    camera.set_config_value(key, value)  
    
    return current_app.success_response({}), 201


def __validate_value(data):
    if(('value' in data) == False):
        raise RemoteDslrApiError("missing parameter", 400)
    
    return data["value"]
