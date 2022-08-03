#!/usr/bin/env python3

"""basic flask app"""

from auth import _generate_uuid
from flask import Flask, jsonify, request
from flask import abort, redirect, url_for
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


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ If the user exists destroy the session and
    redirect the user to GET /. If the user does not exist,
    respond with a 403 HTTP status."""
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id=session_id)
        AUTH.destroy_session(user_id=user.id)
        return redirect(url_for('payload'))
    except Exception:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ If the user exist, respond with a 200 HTTP status
    and the following JSON payload"""
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id=session_id)
        return jsonify({"email": f'{user.email}'}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """ generate a token and respond with a 200 HTTP status"""
    email = request.form.get('email')
    try:
        user = AUTH.get_reset_password_token(email=email)
        new_token = _generate_uuid()
        payload = {"email": f'{email}', "reset_token": f'{new_token}'}
        return jsonify(payload), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """ Update the password. If the token is invalid,
    catch the exception and respond with a 403 HTTP code."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        user = AUTH.update_password(reset_token=reset_token,
                                    password=new_password)
        payload = {"email": f'{email}', "message": "Password updated"}
        return jsonify(payload), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
