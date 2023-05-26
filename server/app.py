import os
import time
from flask import Flask, jsonify, request, Response, send_from_directory, redirect
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, JWTManager
import database_interface as dbInterface
from database_interface import log, Connection
import secrets
import hashlib


app = Flask(__name__, static_url_path='', static_folder='../client/build')
CORS(app)


@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/')
def defaultPage():
    print("Hello!!")
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api', methods=['GET', 'POST'])
def api():
    return {"test": "Hello from the backend!!"}


@app.route('/api/get/messages/', methods=['GET'])
def fetch_messages():
    messages = dbInterface.get_messages_all()
    return {'messages': messages}


@app.route('/api/register', methods=['POST'])
def register_user():
    request_data = request.get_json()
    username, password = request_data.values()
    salt = secrets.token_hex(16)
    salty_password = password + salt
    hash_password = hashlib.sha256(salty_password.encode("utf-8")).hexdigest()
    
    dbInterface.create_user([username, hash_password, salt])
    dbInterface.create_post("Jeg lagde denne posten nettopp!", dbInterface.CURRENT_USER)

    return {"test": "reg attempt"}

if __name__ == "__main__":
    app.run(debug=True)
