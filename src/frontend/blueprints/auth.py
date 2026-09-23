import json
import base64
import logging
import urllib.parse
import requests
from flask import Blueprint, request, jsonify, render_template, redirect, session, url_for
from werkzeug.security import check_password_hash

from src.backend.config.settings import get_settings
from src.backend.database.db import get_user_by_username, create_user, get_or_create_cognito_user
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

@auth_bp.route("/api/auth/cognito/login", methods=["GET"])
def cognito_login():
    """Chuyển hướng người dùng tới Cognito Hosted UI để đăng nhập qua Google IdP."""
    settings = get_settings()
    domain = (settings.cognito_domain or "").rstrip("/")
    client_id = settings.cognito_app_client_id or ""
    redirect_uri = settings.cognito_redirect_uri or ""
    
    if not domain or not client_id:
        logger.error("Chưa cấu hình COGNITO_DOMAIN hoặc COGNITO_APP_CLIENT_ID")
        return redirect("/login?error=cognito_not_configured")

    auth_url = (
        f"{domain}/oauth2/authorize?"
        f"identity_provider=Google&"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=openid+email+profile&"
        f"redirect_uri={urllib.parse.quote(redirect_uri, safe='')}"
    )
    return redirect(auth_url)

@auth_bp.route("/api/auth/cognito/callback", methods=["GET"])
def cognito_callback():
    """Tiếp nhận mã ủy quyền (code) từ Cognito, đổi lấy Token và thiết lập phiên đăng nhập."""
    code = request.args.get("code")
    error = request.args.get("error")
    error_desc = request.args.get("error_description", "")

    if error:
        logger.error(f"Lỗi trả về từ Cognito OAuth callback: {error} - {error_desc}")
        return redirect(f"/login?error={urllib.parse.quote(error_desc or error)}")

    if not code:
        logger.error("Không nhận được authorization code từ Cognito")
        return redirect("/login?error=no_code_provided")

    settings = get_settings()
    domain = (settings.cognito_domain or "").rstrip("/")
    client_id = settings.cognito_app_client_id or ""
    client_secret = settings.cognito_app_client_secret or ""
    redirect_uri = settings.cognito_redirect_uri or ""

    token_url = f"{domain}/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if client_secret:
        auth_str = f"{client_id}:{client_secret}"
        headers["Authorization"] = f"Basic {base64.b64encode(auth_str.encode()).decode()}"

    token_data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri
    }

    try:
        token_resp = requests.post(token_url, data=token_data, headers=headers, timeout=15)
        if token_resp.status_code != 200:
            logger.error(f"Lỗi đổi token với Cognito: {token_resp.status_code} - {token_resp.text}")
            return redirect("/login?error=token_exchange_failed")

        token_json = token_resp.json()
        access_token = token_json.get("access_token")

        user_info_url = f"{domain}/oauth2/userInfo"
        user_resp = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=15)

        email = None
        name = None
        sub = None

        if user_resp.status_code == 200:
            user_data = user_resp.json()
            email = user_data.get("email")
            name = user_data.get("name") or user_data.get("username")
            sub = user_data.get("sub")
        else:
            id_token = token_json.get("id_token")
            if id_token:
                jwt_parts = id_token.split(".")
                if len(jwt_parts) >= 2:
                    payload_b64 = jwt_parts[1]
                    padding = "=" * (4 - (len(payload_b64) % 4))
                    payload_json = json.loads(base64.urlsafe_b64decode(payload_b64 + padding).decode("utf-8"))
                    email = payload_json.get("email")
                    name = payload_json.get("name") or payload_json.get("cognito:username")
                    sub = payload_json.get("sub")

        if not email:
            logger.error("Không trích xuất được email hợp lệ từ tài khoản Google/Cognito")
            return redirect("/login?error=email_not_provided")

        user = get_or_create_cognito_user(email=email, name=name, sub=sub)
        session["user_id"] = user["id"]
        logger.info(f"Đăng nhập thành công qua AWS Cognito Google: user_id={user['id']}, email={email}")

        if user.get("role") == "admin":
            return redirect("/admin")
        return redirect("/studio")

    except Exception as e:
        logger.error(f"Lỗi xử lý xác thực Cognito: {str(e)}", exc_info=True)
        return redirect("/login?error=auth_internal_error")
