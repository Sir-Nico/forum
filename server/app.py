import os
import time
from flask import Flask, jsonify, request, Response, send_from_directory, redirect  # Flask
from flask_cors import CORS  # CORS WAHOO
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, JWTManager  # Session Tokens
import database_interface as dbInterface  # Functions from Database Mainframe B)
from database_interface import log, Connection   # The Cool Stuff from the mainframe B)
import secrets  # For generating salt
import hashlib  # For Hashing passwords


app = Flask(__name__, static_url_path='', static_folder='../client/build')
CORS(app)

app.config["JWT_SECRET_KEY"] = "endre-meg"
jwt = JWTManager(app)


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
    return {"test": "Hello from the backend!!"}, 200  # 200 is the OK HTTP code, meaning everything is as should be


#####################
## GET SIDE OF API ##
#####################

@app.route('/api/get/messages/', methods=['GET'])
def fetch_messages():
    messages = dbInterface.get_messages_all()
    return {'messages': messages}, 200


######################
## POST SIDE OF API ##
######################

@app.route('/api/register', methods=['POST'])
def register_user():
    request_data = request.get_json()
    username, password = request_data.values()
    salt = secrets.token_hex(16)  # Generates salt for password
    salty_password = password + salt
    hash_password = hashlib.sha256(salty_password.encode("utf-8")).hexdigest()  # Hashes the password + salt with SHA256
    
    if len(password) <= 8:  # Forces password to be 8 characters ore more
        return {"error": "Passord må være minst 8 tegn"}, 400

    with Connection() as db:
        db.c.execute("SELECT * FROM users WHERE username = ?", [username])
        if db.c.fetchall():  # Checks if username matches any existing users
            log(f"ERROR: username {username} was already taken.")
            return {"error": "Brukernavn er tatt"}, 400  # Returns bad request if username is taken

    dbInterface.create_user([username, hash_password, salt])
    dbInterface.create_post("Jeg lagde denne posten nettopp!", dbInterface.CURRENT_USER)

    return {"test": "reg attempt"}, 200

if __name__ == "__main__":
    app.run(debug=True)
