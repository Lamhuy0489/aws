import logging
from flask import Blueprint, jsonify, render_template, request

from src.backend.database.db import get_documents_by_user, get_document_by_id, delete_document
from src.backend.auth.security import get_current_user, login_required, login_required_view

logger = logging.getLogger(__name__)

library_bp = Blueprint("library_bp", __name__)

@library_bp.route("/library", methods=["GET"])
@login_required_view
def library_page():
    """Trang Kho luu tru tai lieu ca nhan."""
    user = get_current_user()
    return render_template("library.html", user=user, active_page="library")

@library_bp.route("/api/documents", methods=["GET"])
@login_required
def api_list_documents():
    """Liet ke danh sach tai lieu cua rieng tai khoan dang dang nhap."""
    user = get_current_user()
    docs = get_documents_by_user(user["id"])
    return jsonify({"documents": docs})

@library_bp.route("/api/documents/<doc_id>", methods=["GET"])
@login_required
def api_get_document(doc_id):
    """Lay chi tiet tai lieu, kiem tra nghiem ngat quyen so huu."""
    user = get_current_user()
    doc = get_document_by_id(doc_id, user_id=user["id"])
    if not doc:
        return jsonify({"error": "Khong tim thay tai lieu hoac ban khong co quyen truy cap"}), 404
    return jsonify({"document": doc})

@library_bp.route("/api/documents/<doc_id>", methods=["DELETE"])
@login_required
def api_delete_document(doc_id):
    """Xoa tai lieu khoi kho ca nhan."""
    user = get_current_user()
    success = delete_document(doc_id, user_id=user["id"])
    if not success:
        return jsonify({"error": "Khong the xoa tai lieu hoac ban khong co quyen so huu"}), 404
    return jsonify({"message": "Da xoa tai lieu thanh cong"})
