"""
Authentication routes for Forest Fire Detection
"""

import json
import os
from pathlib import Path
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import requests

auth = Blueprint('auth', __name__)

BASE_DIR = Path(__file__).resolve().parents[1]
USERS_FILE = BASE_DIR.joinpath('data', 'users.json')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')


def load_users():
    if not USERS_FILE.exists():
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        USERS_FILE.write_text(json.dumps({}))
    try:
        return json.loads(USERS_FILE.read_text())
    except json.JSONDecodeError:
        return {}


def save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2))


def get_user(email):
    users = load_users()
    return users.get(email.lower())


def set_user(email, user_data):
    users = load_users()
    users[email.lower()] = user_data
    save_users(users)


@auth.route('/signup', methods=['POST'])
def signup():
    payload = request.json or {}
    name = payload.get('name', '').strip()
    email = payload.get('email', '').strip().lower()
    password = payload.get('password', '')

    if not name or not email or not password:
        return jsonify({'success': False, 'error': 'Name, email, and password are required.'}), 400

    if get_user(email):
        return jsonify({'success': False, 'error': 'Email already registered.'}), 400

    password_hash = generate_password_hash(password)
    user = {'name': name, 'email': email, 'password_hash': password_hash, 'auth_provider': 'local'}
    set_user(email, user)

    return jsonify({'success': True, 'user': {'name': name, 'email': email}})


@auth.route('/login', methods=['POST'])
def login():
    payload = request.json or {}
    email = payload.get('email', '').strip().lower()
    password = payload.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required.'}), 400

    user = get_user(email)
    if not user or not check_password_hash(user.get('password_hash', ''), password):
        return jsonify({'success': False, 'error': 'Invalid credentials.'}), 401

    return jsonify({'success': True, 'user': {'name': user.get('name'), 'email': email}})


@auth.route('/google', methods=['POST'])
def google_login():
    payload = request.json or {}
    id_token = payload.get('id_token', '').strip()

    if not id_token:
        return jsonify({'success': False, 'error': 'Google id_token is required.'}), 400

    token_info = verify_google_token(id_token)
    if not token_info:
        return jsonify({'success': False, 'error': 'Invalid Google token.'}), 401

    email = token_info.get('email')
    name = token_info.get('name') or email.split('@')[0]

    user = get_user(email)
    if not user:
        user = {
            'name': name,
            'email': email,
            'auth_provider': 'google',
            'password_hash': ''
        }
        set_user(email, user)

    return jsonify({'success': True, 'user': {'name': user.get('name'), 'email': email}})


def verify_google_token(id_token):
    try:
        response = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': id_token},
            timeout=5
        )
        if response.status_code != 200:
            return None

        data = response.json()
        aud = data.get('aud')
        if not aud or GOOGLE_CLIENT_ID == 'YOUR_GOOGLE_CLIENT_ID':
            return None
        if aud != GOOGLE_CLIENT_ID:
            return None

        return data
    except requests.RequestException:
        return None
