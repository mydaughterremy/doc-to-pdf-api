# app/services/file_download.py
from flask import Blueprint, jsonify, request

import requests
import os


bp = Blueprint('file_download', __name__, url_prefix='/download')

DOWNLOAD_URL = os.getenv('DOWNLOAD_URL')
if not DOWNLOAD_URL:
    raise ValueError("DOWNLOAD_URL is not set in the environment variables.")

@bp.route('/<id>.pdf', methods=['POST'])
def download_file(id):
    stamp = request.form.get('stamp')
    output_dir = "./converted_file"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{id}.pdf"

    response = requests.post(f"{DOWNLOAD_URL}/{id}.pdf", data={'stamp': stamp}, stream=True)

    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return jsonify({"message": "File downloaded", "path": output_path})
    else:
        return jsonify({"error": "Download failed"}), response.status_code