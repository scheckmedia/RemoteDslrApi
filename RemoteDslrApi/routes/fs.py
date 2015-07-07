from flask import Blueprint, request, current_app
import json
from RemoteDslrApi.error import RemoteDslrApiError
from RemoteDslrApi.server import Server

"""
@api {GET} /api/fs/list List File System
@apiName GetFilesystemList
@apiGroup fs
@apiDescription returns a tree containing camera file system

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
"""
fs_files_list = Blueprint('fs_list', __name__)
@fs_files_list.route('/fs/list', methods=['GET'])
@Server.auth
def fs_list():
    camera = current_app.get_camera()
    fs = camera.read_folder('/')
    return current_app.success_response({"fs": fs}), 200


"""
@api {post} /api/fs/previews Preview for Files
@apiName GetFilesystemPreview
@apiGroup fs
@apiDescription returns the preview images for a list of files

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
"""
fs_file_preview = Blueprint('fs_previews', __name__)
@fs_file_preview.route('/fs/previews', methods=['POST'])
@Server.auth
def fs_previews():
    camera = current_app.get_camera()
    data = json.loads(request.data)  
    value = __validate_value(data) 
    previews = camera.preview_for_files(value)
    return current_app.success_response({"previews": previews}), 200

"""
@api {post} /api/fs/file Get File
@apiName GetFilesystemFile
@apiGroup fs
@apiDescription returns an image in full resolution with exif information

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
"""
fs_file = Blueprint('fs_file', __name__)
@fs_file.route('/fs/file', methods=['POST'])
@Server.auth
def fs_previews():
    camera = current_app.get_camera()
    data = json.loads(request.data)
    value = __validate_value(data)
    previews = camera.read_file(value)
    return current_app.success_response({"file": previews}), 200



def __validate_value(data):
    if not ('value' in data):
        raise RemoteDslrApiError("missing parameter", 400)

    return data["value"]
