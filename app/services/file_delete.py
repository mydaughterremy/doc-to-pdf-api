# app/services/file_delete.py
from flask import Blueprint, jsonify, request
import requests
import os

bp = Blueprint('file_delete', __name__, url_prefix='/delete')

DELETE_URL = os.getenv('DELETE_URL')
if not DELETE_URL:
    raise ValueError("DELETE_URL is not set in the environment variables.")

@bp.route('/', methods=['POST'])
def delete_file():
    file_id = request.form.get('id')
    stamp = request.form.get('stamp')

    if not file_id or not stamp:
        return jsonify({"error": "Missing id or stamp"}), 400

    response = requests.post(DELETE_URL, data={'id': file_id, 'stamp': stamp})
    return response.json(), response.status_code