from flask import Blueprint, request, current_app, Response
import json
from RemoteDslrApi.error import RemoteDslrApiError
import time
from time import sleep

"""
@api {get} /api/camera/capture Capture
@apiName GetCapture
@apiGroup Camera
@apiDescription Takes a picture and returns an image (optional)

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""

"""
@api {post} /api/camera/capture Capture
@apiName PostCapture
@apiGroup Camera
@apiDescription Takes a picture without returning the image

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""
camera_capture = Blueprint('capture', __name__)
@camera_capture.route('/camera/capture', methods=['GET','POST'])
def capture():     
    camera = current_app.get_camera()
    if(request.method == "GET"):
        image = camera.capture()        
        return current_app.success_response({"image" : image.base64}), 200
    else:
        camera.capture(False)
        return current_app.success_response({}), 200
    

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
def start_live_view():            
    camera = current_app.get_camera()
    
    def frame_build():
        camera.start_preview()  
        while camera.preview_running:
            frame = camera.read_liveview_frame()
            print "frame %r -- is-busy: %r" % (bool(frame), camera.is_busy)
                        
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
@api {get} /api/camera/liveview/stop Live View stop
@apiName GetLiveviewStop
@apiGroup Camera
@apiDescription Stops mjpeg stream and camera Live View

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""

camera_stop_live_view = Blueprint('camera_live_view_stop', __name__)
@camera_stop_live_view.route('/camera/liveview/stop', methods=['GET'])
def stop_live_view():
    camera = current_app.get_camera()
    camera.stop_preview()    
    return current_app.success_response({}), 200

"""
@api {get} /api/camera/focus/manual Manual focus
@apiName GetFocusManual
@apiGroup Camera
@apiDescription Manual focus in live view

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK    
"""

camera_focus_manual = Blueprint('camera_focus_manual', __name__)
@camera_focus_manual.route('/camera/focus/manual', methods=['PUT'])
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
