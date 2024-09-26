#!/usr/bin/env python3
"""Basic Flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route('/', methods=['GET'])
def home():
    """Home route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Register a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST', 'DELETE'])
def login() -> str:
    """Login a user"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response
        abort(401)
    elif request.method == 'DELETE':
        session_id = request.cookies.get('session_id')
        if not session_id:
            abort(403)
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        AUTH.destroy_session(user.id)
        return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """Return user profile"""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST', 'PUT'])
def get_reset_password_token():
    """Reset a user password"""
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            abort(403)
        try:
            user = AUTH._db.find_user_by(email=email)
        except Exception as e:
            abort(403)
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    elif request.method == 'PUT':
        email = request.form.get('email')
        token = request.form.get('reset_token')
        new_pwd = request.form.get('new_password')
        if not email or not token or not new_pwd:
            abort(403)
        try:
            AUTH.update_password(reset_token=token, password=new_pwd)
        except ValueError:
            abort(403)
        return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
