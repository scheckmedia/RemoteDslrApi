from flask import Blueprint, jsonify
from RemoteDslrApi.camera_controller import CameraController

status_page = Blueprint('status', __name__)
@status_page.route('/status', methods=['GET'])

def get_status():
    camera = CameraController()    
    message = { "camera" : camera.has_camera(), "state" : "ok"}
    if(message["camera"] == False) :
        message["error"] = camera.get_last_error()
    return jsonify(message)
