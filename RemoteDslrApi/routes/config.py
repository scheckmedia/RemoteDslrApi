from flask import Blueprint, jsonify, request, current_app
import json
from RemoteDslrApi.error import RemoteDslrApiError


"""
@api {get} /api/config/list List
@apiName GetConfig
@apiGroup Config
@apiDescription Returns a list of the current configuration

@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK    
"""
list_config_page = Blueprint('list_config', __name__)
@list_config_page.route('/config/list', methods=['GET'])
def list_config():     
    camera = current_app.get_camera()
    print camera.has_camera()
    return jsonify(camera.get_config())

"""
@api {get} /api/config Value by key
@apiName GetConfigByKey
@apiGroup Config
@apiDescription Returns a value of a key or a list of values for a list of keys

@apiParam {Array} value    settings key(s) to get value
@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK
    
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
@config_by_value.route('/config', methods=['GET'])
def get_config_by_key():
    camera = current_app.get_camera()
    data = json.loads(request.data)    
    return jsonify(camera.get_config())



"""
@api {put} /api/config/aperture Aperture
@apiName SetAperture
@apiGroup Config
@apiDescription Updates Aperture value for a connected Camera

@apiParam {String} value    ISO value
@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK
    
@apiParamExample {json} Request-Example:
{
    "value" : "f\/10"
}
"""
config_aperture_page = Blueprint('config_aperture', __name__)
@config_aperture_page.route('/config/aperture/', methods=['PUT'])
def aperture():    
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data)
    
    camera.set_aperture(value)  
    
    
    return jsonify({"state" : "ok"}), 201



"""
@api {put} /api/config/iso ISO
@apiName SetISO
@apiGroup Config
@apiDescription Updates ISO value for a connected Camera

@apiParam {String} value    ISO value
@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK

@apiParamExample {json} Request-Example:
{
    "value" : "400"
}
"""
config_iso_page = Blueprint('config_iso', __name__)
@config_iso_page.route('/config/iso/', methods=['PUT'])
def iso():    
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data)
    
    camera.set_iso(value)  
    return jsonify({"state" : "ok"}), 201


"""
@api {put} /api/config/shutterspeed Shutter speed
@apiName SetShutterSpeed
@apiGroup Config
@apiDescription Updates Shutter speed value for a connected Camera 

@apiParam {String} value    shutter speed value
@apiSuccessExample Success-Response:
    HTTP/1.1 201 OK

@apiParamExample {json} Request-Example:
{
    "value" : "1\/128"
}
"""
config_shutter_speed_page = Blueprint('config_shutter_speed', __name__)
@config_shutter_speed_page.route('/config/shutterspeed/', methods=['PUT'])
def shutter_speed():    
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data)
    
    camera.set_shutter_speed(value)  
    
    return jsonify({"state" : "ok"}), 201


def __validate_value(data):
    if(('value' in data) == False):
        raise RemoteDslrApiError("missing parameter", 400)
    
    return data["value"]
