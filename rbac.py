from functools import wraps
from flask import request, jsonify

ROLE_HIERARCHY = {"admin": 3, "moderator": 2, "user": 1}

def require_role(min_role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from users import users_db
            user = users_db.get(request.user_id)
            if not user:
                return jsonify({"error": "user not found"}), 404
            user_level = ROLE_HIERARCHY.get(user["role"], 0)
            required_level = ROLE_HIERARCHY.get(min_role, 0)
            if user_level < required_level:
                return jsonify({"error": "insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
