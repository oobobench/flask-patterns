import hashlib
import secrets
from functools import wraps
from flask import request, jsonify

def hash_password(password):
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return f"{salt}:{hashed.hex()}"

def verify_password(password, stored):
    salt, hash_val = stored.split(":")
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return hashed.hex() == hash_val

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token or token not in sessions:
            return jsonify({"error": "unauthorized"}), 401
        request.user_id = sessions[token]
        return f(*args, **kwargs)
    return decorated

sessions = {}
