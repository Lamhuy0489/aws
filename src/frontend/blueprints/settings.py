import logging
from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from src.backend.database.db import (
    get_user_by_id,
    get_user_settings,
    update_user_settings,
    update_user_password
)
from src.backend.auth.security import get_current_user, login_required, login_required_view

logger = logging.getLogger(__name__)

settings_bp = Blueprint("settings_bp", __name__)

@settings_bp.route("/settings", methods=["GET"])
@login_required_view
def settings_page():
    """Trang Cài Đặt Cá Nhân Từng Tài Khoản."""
    user = get_current_user()
    user_settings = get_user_settings(user["id"])
    return render_template(
        "settings.html",
        user=user,
        settings=user_settings,
        active_page="settings"
    )

@settings_bp.route("/api/settings", methods=["GET"])
@login_required
def api_get_settings():
    """Lấy thông tin cấu hình hiện tại của người dùng."""
    user = get_current_user()
    settings = get_user_settings(user["id"])
    return jsonify({"settings": settings})

@settings_bp.route("/api/settings", methods=["POST"])
@login_required
def api_update_settings():
    """Cập nhật các tùy chọn cá nhân hóa của tài khoản."""
    user = get_current_user()
    data = request.get_json() or {}

    updated = update_user_settings(user["id"], data)
    return jsonify({
        "message": "Cập nhật cài đặt thành công",
        "settings": updated
    })

@settings_bp.route("/api/settings/password", methods=["POST"])
@login_required
def api_change_password():
    """Đổi mật khẩu tài khoản người dùng với xác thực mật khẩu hiện tại."""
    user = get_current_user()
    data = request.get_json() or {}

    old_password = data.get("old_password", "")
    new_password = data.get("new_password", "")
    confirm_password = data.get("confirm_password", "")

    if not old_password or not new_password:
        return jsonify({"error": "Vui lòng nhập đầy đủ mật khẩu hiện tại và mật khẩu mới"}), 400

    if new_password != confirm_password:
        return jsonify({"error": "Mật khẩu mới và xác nhận mật khẩu không khớp nhau"}), 400

    if len(new_password) < 6:
        return jsonify({"error": "Mật khẩu mới phải có ít nhất 6 ký tự"}), 400

    # Lấy thông tin user đầy đủ từ DB để kiểm tra mật khẩu cũ
    user_db = get_user_by_id(user["id"])
    if not user_db or not check_password_hash(user_db["password_hash"], old_password):
        return jsonify({"error": "Mật khẩu hiện tại không chính xác"}), 400

    new_hash = generate_password_hash(new_password)
    success = update_user_password(user["id"], new_hash)

    if success:
        logger.info(f"Người dùng {user['username']} đã đổi mật khẩu thành công")
        return jsonify({"message": "Đổi mật khẩu thành công"})
    else:
        return jsonify({"error": "Không thể cập nhật mật khẩu, vui lòng thử lại sau"}), 500
