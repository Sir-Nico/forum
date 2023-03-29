import os
import time
import sqlite3
from django.shortcuts import redirect
from flask import Flask, jsonify, request, Response, send_from_directory, redirect
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, JWTManager
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

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
