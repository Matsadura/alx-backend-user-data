#!/usr/bin/env python3
"""Basic Flask app"""
from auth import Auth
from flask import Flask, jsonify, request


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
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
