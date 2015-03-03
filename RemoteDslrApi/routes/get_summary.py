from flask import Blueprint, jsonify, current_app

status_page = Blueprint('summary', __name__)
@status_page.route('/summary', methods=['GET'])
def get_summary():
    camera = current_app.get_camera()
    return jsonify( {"summary" : camera.get_summary(), "state" : "success"} )
