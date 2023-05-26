import os
import time
from flask import Flask, jsonify, request, Response, send_from_directory, redirect
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, JWTManager
import database_interface as dbInterface
from database_interface import log, Connection


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


@app.route('/api', methods=['GET'])
def api():
    return {"test": "Hello from the backend!!"}


@app.route('/api/get/messages/', methods=['GET'])
def fetch_messages():
    messages = dbInterface.get_messages_all()
    return {'messages': messages}


@app.route('/api/register', methods=['POST'])
def register_user():
    request_data = request.get_json()
    print(request_data)
    return {"test": "bruker"}



if __name__ == "__main__":
    app.run(debug=True)
