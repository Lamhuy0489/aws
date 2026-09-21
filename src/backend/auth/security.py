from functools import wraps
from flask import session, jsonify, request, redirect, render_template
from typing import Optional, Dict
from src.backend.database.db import get_user_by_id

def get_current_user() -> Optional[Dict]:
    """Lay thong tin nguoi dung dang dang nhap tu Flask session."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    user = get_user_by_id(user_id)
    if not user:
        session.clear()
        return None
    return user

def login_required(f):
    """Decorator yeu cau nguoi dung phai dang nhap truoc khi goi API."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Vui long dang nhap de thuc hien thao tac nay", "code": "UNAUTHORIZED"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator yeu cau quyen Quan tri vien (Admin) cho API."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Vui long dang nhap", "code": "UNAUTHORIZED"}), 401
        if user.get("role") != "admin":
            return jsonify({"error": "Ban khong co quyen quan tri vien (Admin required)", "code": "FORBIDDEN"}), 403
        return f(*args, **kwargs)
    return decorated_function

def login_required_view(f):
    """Decorator cho View HTML: Chuyen huong ve /login neu chua dang nhap."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return redirect(f"/login?next={request.path}")
        return f(*args, **kwargs)
    return decorated_function

def admin_required_view(f):
    """Decorator cho View HTML: Chuyen huong ve /login neu chua dang nhap hoac hien thi 403 neu khong phai Admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return redirect(f"/login?next={request.path}")
        if user.get("role") != "admin":
            return render_template("403.html", user=user), 403
        return f(*args, **kwargs)
    return decorated_function

