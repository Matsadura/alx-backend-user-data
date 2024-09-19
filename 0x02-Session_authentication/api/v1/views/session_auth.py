#!/usr/bin/env python3
"""Handle all routes for the Session authentication"""
import os
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=True)
def login():
    """Login route"""
    email = request.form.get('email')
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or password == '':
        return jsonify({"error": "password is missing"}), 400

    user = User.search({'email': email})
    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    valid = user[0].is_valid_password(password)
    if not valid:
        return jsonify({"error": "wrong password"})

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    session_name = os.getenv('SESSION_NAME')
    resp = jsonify(user[0].to_json())
    resp.set_cookie(session_name, session_id)
    return resp
