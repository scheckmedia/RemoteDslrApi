from flask import Blueprint, request, current_app, Response
import json
from RemoteDslrApi.error import RemoteDslrApiError
from time import sleep
from RemoteDslrApi.server import Server

"""
@api {post} /api/camera/capture Capture
@apiName GetCapture
@apiGroup Camera
@apiDescription Takes a picture and optional returns an image as base64 encoded string(optional)

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""
camera_capture = Blueprint('capture', __name__)
@camera_capture.route('/camera/capture', methods=['POST'])
@Server.auth
def capture():     
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    with_image = False
    
    if('with_image' in data):
        with_image = data["with_image"]
    
    image = camera.capture(with_image)
    if(with_image):                
        return current_app.success_response(image.serialize), 200
    
    return current_app.success_response({"path" : image.path}), 200
    

"""
@api {get} /api/liveview/start Live View start
@apiName GetLiveviewStart
@apiGroup Camera
@apiDescription Starts a mjpeg stream of camera Live View

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""
camera_start_live_view = Blueprint('camera_live_view_start', __name__)
@camera_start_live_view.route('/camera/liveview/start', methods=['GET'])
@Server.auth
def start_live_view():            
    camera = current_app.get_camera()
    
    def frame_build():
        camera.start_preview()  
        while camera.preview_running:
            frame = camera.read_liveview_frame()
                        
            # another command will be executed
            # so we can wait a little bit more
            if(frame == False or camera.is_busy):
                sleep(0.5)
                continue  
                  
            yield  (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            sleep(1./25)            
            
    return Response(frame_build(), mimetype='multipart/x-mixed-replace; boundary=frame')    


"""
@api {put} /api/camera/liveview/stop Live View stop
@apiName GetLiveviewStop
@apiGroup Camera
@apiDescription Stops mjpeg stream and camera Live View

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""

camera_stop_live_view = Blueprint('camera_live_view_stop', __name__)
@camera_stop_live_view.route('/camera/liveview/stop', methods=['PUT'])
@Server.auth
def stop_live_view():
    camera = current_app.get_camera()
    camera.stop_preview()    
    return current_app.success_response({}), 200

"""
@api {put} /api/camera/focus/manual Manual focus
@apiName GetFocusManual
@apiGroup Camera
@apiDescription Manual focus in live view

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""

camera_focus_manual = Blueprint('camera_focus_manual', __name__)
@camera_focus_manual.route('/camera/focus/manual', methods=['PUT'])
@Server.auth
def focus_manual():
    camera = current_app.get_camera()
    data = json.loads(request.data)
    value = __validate_value(data)
    camera.manual_focus(value)    
    return current_app.success_response({}), 200


def __validate_value(data):
    if(('value' in data) == False):
        raise RemoteDslrApiError("missing parameter", 400)
    
    return data["value"]
