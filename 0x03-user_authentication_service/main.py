#!/usr/bin/env python3
"""End-to-end integration test"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Test register user"""
    response_1 = requests.post('http://0.0.0.0:5000/users',
                               data={'email': email, 'password': password})
    assert response_1.json() == {"email": email, "message": "user created"}

    response_2 = requests.post('http://0.0.0.0:5000/users',
                               data={'email': email, 'password': password})
    assert response_2.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password"""
    response = requests.post('http://0.0.0.0:5000/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Test unauthorized profile access"""
    response = requests.get('http://0.0.0.0:5000/profile')
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """Test login"""
    response = requests.post('http://0.0.0.0:5000/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    return response.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    """Test authorized profile access"""
    response = requests.get('http://0.0.0.0:5000/profile',
                            cookies={'session_id': session_id})
    assert response.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    """Test log out"""
    response = requests.delete('http://0.0.0.0:5000/sessions',
                               cookies={'session_id': session_id})
    assert response.status_code == 200

    response_2 = requests.delete('http://0.0.0.0:5000/sessions',
                                 cookies={'session_id': 'fake'})
    assert response_2.status_code == 403


def reset_password_token(email: str) -> str:
    """Test reset token"""
    response_1 = requests.post('http://0.0.0.0:5000/reset_password',
                               data={'email': email})
    payload = response_1.json()
    token = payload.get('reset_token')
    assert response_1.json() == {'email': email,
                                 'reset_token': token}

    response_2 = requests.post('http://0.0.0.0:5000/reset_password',
                               data={'email': 'fake'})
    assert response_2.status_code == 403


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """Test update password"""
    response = requests.put('http://0.0.0.0:5000/reset_password',
                            data={'email': email, 'reset_token': reset_token,
                                  'password': new_password})
    assert response.json() == {"email": email, "message": "Password updated"}

    response = requests.put('http://0.0.0.0:5000/reset_password',
                            data={'email': email, 'reset_token': 'fake',
                                  'password': new_password})
    assert response.status_code == 403


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
