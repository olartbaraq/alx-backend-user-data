#!/usr/bin/env python3

"""basic flask app"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def payload():
    """returns a json payload of the form"""
    return jsonify({"message": "Bienvenue"})


from auth import Auth


AUTH = Auth()


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
