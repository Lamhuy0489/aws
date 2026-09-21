import logging
from flask import Blueprint, request, jsonify, render_template, redirect, session, url_for
from werkzeug.security import check_password_hash

from src.backend.database.db import get_user_by_username, create_user
from src.backend.auth.security import get_current_user

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET"])
def login_page():
    """Trang dang nhap va dang ky."""
    user = get_current_user()
    if user:
        if user.get("role") == "admin":
            return redirect("/admin")
        return redirect("/studio")
    return render_template("login.html")

@auth_bp.route("/logout", methods=["GET"])
def logout_view():
    """Dang xuat va chuyen huong ve trang dang nhap."""
    session.clear()
    return redirect("/login")

@auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    """Xac thuc dang nhap va tra ve URL tu dong chuyen huong theo vai tro."""
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    next_url = request.args.get("next") or data.get("next")

    if not username or not password:
        return jsonify({"error": "Vui long nhap day du ten dang nhap va mat khau"}), 400

    user = get_user_by_username(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Ten dang nhap hoac mat khau khong chinh xac"}), 401

    session["user_id"] = user["id"]

    # Phan dinh ranh gioi: Admin chuyen huong /admin, User chuyen huong /studio
    if user["role"] == "admin":
        redirect_target = "/admin"
    else:
        redirect_target = next_url if (next_url and next_url.startswith("/") and next_url != "/admin") else "/studio"

    return jsonify({
        "message": "Dang nhap thanh cong",
        "redirect_url": redirect_target,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    })

@auth_bp.route("/api/auth/register", methods=["POST"])
def api_register():
    """Dang ky tai khoan nguoi dung moi."""
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Ten dang nhap va mat khau khong duoc de trong"}), 400

    if len(username) < 3:
        return jsonify({"error": "Ten dang nhap phai co it nhat 3 ky tu"}), 400

    if len(password) < 6:
        return jsonify({"error": "Mat khau phai co it nhat 6 ky tu"}), 400

    existing_user = get_user_by_username(username)
    if existing_user:
        return jsonify({"error": "Ten dang nhap da ton tai tren he thong"}), 409

    try:
        user = create_user(username, email, password, role="user")
        session["user_id"] = user["id"]
        return jsonify({
            "message": "Dang ky tai khoan thanh cong",
            "redirect_url": "/studio",
            "user": user
        })
    except Exception as e:
        logger.error(f"Loi tao tai khoan: {str(e)}")
        return jsonify({"error": f"Loi he thong khi tao tai khoan: {str(e)}"}), 500

@auth_bp.route("/api/auth/logout", methods=["POST"])
def api_logout():
    """Dang xuat qua API."""
    session.clear()
    return jsonify({"message": "Da dang xuat thanh cong", "redirect_url": "/login"})

@auth_bp.route("/api/auth/me", methods=["GET"])
def api_me():
    """Lay thong tin tai khoan hien tai."""
    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False})
    return jsonify({
        "authenticated": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    })
