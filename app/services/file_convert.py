# app/services/file_convert.py
from flask import Blueprint, jsonify
import requests
import os

bp = Blueprint('file_convert', __name__, url_prefix='/convert')

CONVERT_URL = os.getenv('CONVERT_URL')
if not CONVERT_URL:
    raise ValueError("CONVERT_URL is not set in the environment variables.")

@bp.route('/<id>', methods=['GET'])
def convert_status(id):
    response = requests.get(f"{CONVERT_URL}/{id}")
    return response.json(), response.status_code