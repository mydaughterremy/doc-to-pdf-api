# app/services/file_process.py
from flask import Blueprint, request, jsonify
import requests
import os
import time
import logging

bp = Blueprint('file_process', __name__, url_prefix='/process')

UPLOAD_URL = os.getenv('UPLOAD_URL')
CONVERT_URL = os.getenv('CONVERT_URL')
DOWNLOAD_URL = os.getenv('DOWNLOAD_URL')
DELETE_URL = os.getenv('DELETE_URL')

if not UPLOAD_URL or not CONVERT_URL or not DOWNLOAD_URL or not DELETE_URL:
    raise ValueError("One or more required URLs are not set in the environment variables.")

logger = logging.getLogger(__name__)

@bp.route('/', methods=['POST'])
def process_file():
    file = request.files.get('file')
    if not file:
        logger.error("No file provided")
        return jsonify({"error": "No file provided"}), 400

    # Step 1: Upload the file
    logger.info("Uploading file: %s", file.filename)
    response = requests.post(
        UPLOAD_URL,
        files={'file': file.stream},
        data={'convertType': 'PDF'}
    )

    if response.status_code != 200:
        logger.error("File upload failed: %s", response.json())
        return jsonify({"error": "File upload failed", "details": response.json()}), response.status_code

    upload_data = response.json()
    file_id = upload_data.get("id")
    stamp = upload_data.get("stamp")
    if not file_id or not stamp:
        logger.error("Invalid response from upload API")
        return jsonify({"error": "Invalid response from upload API"}), 500

    logger.info("File uploaded successfully: ID=%s, Stamp=%s", file_id, stamp)

    # Step 2: Check conversion status
    logger.info("Checking conversion status for file ID: %s", file_id)
    while True:
        convert_response = requests.get(f"{CONVERT_URL}/{file_id}")
        if convert_response.status_code != 200:
            logger.error("Conversion status check failed: %s", convert_response.json())
            return jsonify({"error": "Conversion status check failed", "details": convert_response.json()}), convert_response.status_code

        convert_data = convert_response.json()
        if convert_data.get("status") == "S":
            logger.info("Conversion completed for file ID: %s", file_id)
            break

        time.sleep(1)  # Wait for 1 second before checking again

    # Step 3: Download the converted file
    output_dir = "./converted_file"
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{os.path.splitext(file.filename)[0]}.pdf"

    logger.info("Downloading converted file to: %s", output_path)
    download_response = requests.post(f"{DOWNLOAD_URL}/{file_id}.pdf", data={'stamp': stamp}, stream=True)

    if download_response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logger.info("File downloaded successfully: %s", output_path)
    else:
        logger.error("File download failed: %s", download_response.json())
        return jsonify({"error": "File download failed", "details": download_response.json()}), download_response.status_code

    # Step 4: Delete the file from the server
    logger.info("Deleting file from server: ID=%s", file_id)
    delete_response = requests.post(DELETE_URL, data={'id': file_id, 'stamp': stamp})
    if delete_response.status_code != 200:
        logger.error("File deletion failed: %s", delete_response.json())
        return jsonify({"error": "File deletion failed", "details": delete_response.json()}), delete_response.status_code

    logger.info("File processed successfully: %s", output_path)
    return jsonify({"message": "File processed successfully", "download_path": output_path})