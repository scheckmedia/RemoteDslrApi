from flask import Blueprint, jsonify

status_page = Blueprint('status', __name__)
@status_page.route('/status', methods=['POST'])
def get_status():
    return jsonify({'status' : 'cool'})
