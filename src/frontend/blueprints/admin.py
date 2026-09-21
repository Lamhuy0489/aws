import logging
from flask import Blueprint, request, jsonify, render_template

from src.backend.database.db import (
    get_all_api_keys, create_api_key, toggle_api_key_status, delete_api_key,
    get_all_users, get_admin_system_stats
)
from src.backend.auth.security import get_current_user, admin_required, admin_required_view

logger = logging.getLogger(__name__)

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/admin", methods=["GET"])
@admin_required_view
def admin_page():
    """Trang Bang Quan Tri He Thong danh rieng cho Admin."""
    user = get_current_user()
    return render_template("admin.html", user=user, active_page="admin")

@admin_bp.route("/api/admin/stats", methods=["GET"])
@admin_required
def api_admin_stats():
    """Lay chi so thong ke tong quan toan he thong."""
    stats = get_admin_system_stats()
    return jsonify({"stats": stats})

@admin_bp.route("/api/admin/keys", methods=["GET"])
@admin_required
def api_admin_keys():
    """Lay danh sach tat ca API Keys voi khoa duoc che mask bao mat."""
    keys = get_all_api_keys()
    sanitized = []
    for k in keys:
        item = dict(k)
        val = item.get("key_value", "")
        if len(val) > 8:
            item["key_masked"] = val[:4] + "..." + val[-4:]
        else:
            item["key_masked"] = "***"
        sanitized.append(item)
    return jsonify({"keys": sanitized})

@admin_bp.route("/api/admin/keys", methods=["POST"])
@admin_required
def api_admin_add_key():
    """Them API Key moi vao co che xoay tour."""
    data = request.get_json() or {}
    provider = data.get("provider", "gemini").lower()
    alias = data.get("key_alias", "").strip()
    key_val = data.get("key_value", "").strip()
    model = data.get("model_name", "gemini-1.5-flash").strip()
    base_url = data.get("base_url", "").strip()
    priority = int(data.get("priority", 1))

    if not alias or not key_val:
        return jsonify({"error": "Vui long nhap ten goi nho (alias) va gia tri API Key"}), 400

    try:
        new_key = create_api_key(
            provider=provider,
            key_alias=alias,
            key_value=key_val,
            model_name=model,
            base_url=base_url,
            priority=priority
        )
        return jsonify({"message": "Them API Key moi vao tour xoay thanh cong", "key": new_key})
    except Exception as e:
        logger.error(f"Loi khi them key: {e}")
        return jsonify({"error": f"Loi he thong khi them key: {str(e)}"}), 500

@admin_bp.route("/api/admin/keys/<key_id>/toggle", methods=["POST"])
@admin_required
def api_admin_toggle_key(key_id):
    """Chuyen doi trang thai Kich hoat / Tam dung cua key trong tour xoay."""
    new_status = toggle_api_key_status(key_id)
    if new_status is None:
        return jsonify({"error": "Khong tim thay khoa API voi ID tuong ung"}), 404
    return jsonify({
        "message": f"Da {'kich hoat' if new_status == 1 else 'tam dung'} khoa API",
        "is_active": new_status
    })

@admin_bp.route("/api/admin/keys/<key_id>", methods=["DELETE"])
@admin_required
def api_admin_delete_key(key_id):
    """Xoa khoa API khoi co che xoay tour."""
    success = delete_api_key(key_id)
    if not success:
        return jsonify({"error": "Khong tim thay khoa API de xoa"}), 404
    return jsonify({"message": "Da xoa khoa API thanh cong"})

@admin_bp.route("/api/admin/users", methods=["GET"])
@admin_required
def api_admin_users():
    """Lay danh sach tat ca tai khoan nguoi dung trong CSDL."""
    users = get_all_users()
    return jsonify({"users": users})
