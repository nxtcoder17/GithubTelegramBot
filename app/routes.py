from app import app
from flask import request
import json


@app.route('/')
def index():
    print("Flask, Web server is UP")
    return "Flask is running"


@app.route('/github', methods=['POST'])
def github_event():
    if request.headers['content-type'] == 'application/json':
        print(request.json)
        return request.json
    return json.dumps({"msg": "No Response"})
