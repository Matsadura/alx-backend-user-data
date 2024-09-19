#!/usr/bin/env python3
"""Handle all routes for the Session authentication"""
import os
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify, abort


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Login route"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    out = jsonify(user.to_json())
    out.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """Logout user"""
    from api.v1.app import auth
    logout = auth.destroy_session(request)
    if not logout:
        abort(404)
    return jsonify({})
