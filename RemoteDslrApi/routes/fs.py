from flask import Blueprint, request, current_app
import json
from RemoteDslrApi.error import RemoteDslrApiError

"""
@api {GET} /api/fs/list List File System
@apiName GetFilesystemList
@apiGroup fs
@apiDescription

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
"""
fs_files_list = Blueprint('fs_list', __name__)
@fs_files_list.route('/fs/list', methods=['GET'])
def fs_list():
    print "inlist"
    camera = current_app.get_camera()
    fs = camera.read_folder('/')
    return current_app.success_response({"fs": fs}), 200


"""
@api {post} /api/fs/previews Preview for Files
@apiName GetFilesystemPreview
@apiGroup fs
@apiDescription

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
"""
fs_file_preview = Blueprint('fs_previews', __name__)
@fs_file_preview.route('/fs/previews', methods=['POST'])
def fs_previews():
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data) 
    previews = camera.preview_for_files(value)
    return current_app.success_response({"previews": previews}), 200



def __validate_value(data):
    if not ('value' in data):
        raise RemoteDslrApiError("missing parameter", 400)

    return data["value"]
