# app/services/file_upload.py
from flask import Blueprint, request, jsonify
import requests
import os

bp = Blueprint('file_upload', __name__, url_prefix='/upload')

UPLOAD_URL = os.getenv('UPLOAD_URL')
if not UPLOAD_URL:
    raise ValueError("UPLOAD_URL is not set in the environment variables.")

@bp.route('/', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    response = requests.post(
        UPLOAD_URL,
        files={'file': file.stream},
        data={'convertType': 'PDF'}
    )

    return response.json(), response.status_code