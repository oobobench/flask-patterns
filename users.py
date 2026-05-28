from flask import Blueprint, request, jsonify
from auth import hash_password, verify_password, require_auth, sessions
import secrets

users_bp = Blueprint("users", __name__)
users_db = {}

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    if username in users_db:
        return jsonify({"error": "user already exists"}), 409
    
    users_db[username] = {
        "username": username,
        "password_hash": hash_password(password),
        "role": "user",
        "active": True
    }
    return jsonify({"message": "registered", "username": username}), 201

@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    user = users_db.get(username)
    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "invalid credentials"}), 401
    if not user["active"]:
        return jsonify({"error": "account deactivated"}), 403
    
    token = secrets.token_urlsafe(32)
    sessions[token] = username
    return jsonify({"token": token, "username": username})

@users_bp.route("/me", methods=["GET"])
@require_auth
def get_profile():
    user = users_db.get(request.user_id)
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "username": user["username"],
        "role": user["role"],
        "active": user["active"]
    })
