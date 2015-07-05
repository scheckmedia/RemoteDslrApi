from flask import Blueprint, current_app
from RemoteDslrApi.error import RemoteDslrApiError
from RemoteDslrApi.server import Server

"""
@api {get} /api/status Status
@apiName GetStatus
@apiGroup Status
@apiDescription Returns the camera state (found or not)

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
    {
        "camera": true,
        "state": "ok"
    }
"""
status_page = Blueprint('status', __name__)
@status_page.route('/status', methods=['GET'])
@Server.auth
def get_status():
    camera = current_app.get_camera()
    message = { "camera" : camera.has_camera}
    if(message["camera"] == False) :
        message["error"] = RemoteDslrApiError.translate(camera.get_last_error())
    return current_app.success_response(message)

"""
@api {get} /api/status/summary Summary
@apiName GetSummary
@apiGroup Status
@apiDescription Returns an array containing camera informations 

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
    {        
        "state": "ok",
        "summary": [
            "Hersteller: Nikon Corporation",
            "Modell: D90",
            " Version: V1.00",
            " Seriennummer: xxxxxx",
            ...
        ]
    }
"""
status_summary = Blueprint('status_summary', __name__)
@status_summary.route('/status/summary', methods=['GET'])
@Server.auth
def get_summary():
    camera = current_app.get_camera()
    return current_app.success_response({"summary" : camera.get_summary()}), 200    

