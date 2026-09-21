from functools import wraps
from flask import session, jsonify, request
from typing import Optional, Dict
from src.backend.database.db import get_user_by_id

def get_current_user() -> Optional[Dict]:
    """Lấy thông tin người dùng đang đăng nhập từ Flask session."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    user = get_user_by_id(user_id)
    if not user:
        session.clear()
        return None
    return user

def login_required(f):
    """Decorator yêu cầu người dùng phải đăng nhập trước khi gọi API."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Vui lòng đăng nhập để thực hiện thao tác này", "code": "UNAUTHORIZED"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator yêu cầu quyền Quản trị viên (Admin)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Vui lòng đăng nhập", "code": "UNAUTHORIZED"}), 401
        if user.get("role") != "admin":
            return jsonify({"error": "Bạn không có quyền quản trị viên (Admin required)", "code": "FORBIDDEN"}), 403
        return f(*args, **kwargs)
    return decorated_function
