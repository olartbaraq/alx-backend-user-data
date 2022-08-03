#!/usr/bin/env python3

"""basic flask app"""

from flask import Flask, jsonify, request, make_response, abort
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def payload():
    """returns a json payload of the form"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """returns a JSON payload of users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": f'{email}', "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login() -> str:
    """returns the JSON payload of logged in user"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email=email)
    resp = jsonify({"email": f'{email}', "message": "logged in"})
    resp.set_cookie('session_id', session_id)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
