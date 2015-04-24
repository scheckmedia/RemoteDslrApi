from flask import Blueprint, request, current_app, Response
import json

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
    
    
camera_start_liveview = Blueprint('camera_liveview_start', __name__)
@camera_start_liveview.route('/camera/liveview/start', methods=['GET'])
def start_liveview():
    camera = current_app.get_camera()
    def frame_build():
        camera.start_preview()
        while camera.preview_running:     
            data = camera.read_liveview_frame()
            print data
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')        
        
    return Response(frame_build(), mimetype='multipart/x-mixed-replace; boundary=frame')    

camera_stop_liveview = Blueprint('camera_liveview_stop', __name__)
@camera_stop_liveview.route('/camera/liveview/stop', methods=['GET'])
def stop_liveview():
    camera = current_app.get_camera()
    camera.stop_preview()    
    return current_app.success_response({}), 200
