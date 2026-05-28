from flask import Blueprint, request, jsonify
from auth import require_auth
from rbac import require_role

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/users", methods=["GET"])
@require_auth
@require_role("admin")
def list_users():
    from users import users_db
    return jsonify([
        {"username": u["username"], "role": u["role"], "active": u["active"]}
        for u in users_db.values()
    ])

@admin_bp.route("/users/<username>/role", methods=["PUT"])
@require_auth
@require_role("admin")
def set_role(username):
    from users import users_db
    data = request.get_json()
    new_role = data.get("role")
    
    if username not in users_db:
        return jsonify({"error": "user not found"}), 404
    if username == request.user_id:
        return jsonify({"error": "cannot change own role"}), 400
    if new_role not in ["user", "moderator", "admin"]:
        return jsonify({"error": "invalid role"}), 400
    
    users_db[username]["role"] = new_role
    return jsonify({"message": f"role updated to {new_role}"})

@admin_bp.route("/users/<username>/deactivate", methods=["POST"])
@require_auth
@require_role("admin")
def deactivate_user(username):
    from users import users_db
    if username not in users_db:
        return jsonify({"error": "user not found"}), 404
    if username == request.user_id:
        return jsonify({"error": "cannot deactivate self"}), 400
    
    users_db[username]["active"] = False
    # Revoke all sessions for deactivated user
    from auth import sessions
    to_remove = [t for t, u in sessions.items() if u == username]
    for t in to_remove:
        del sessions[t]
    
    return jsonify({"message": f"{username} deactivated"})
