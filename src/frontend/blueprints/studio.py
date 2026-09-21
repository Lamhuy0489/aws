import os
import io
import uuid
import logging
from flask import Blueprint, request, jsonify, render_template, send_file

from src.backend.config.settings import AppSettings
from src.backend.parsers.hybrid_engine import HybridDocumentEngine, DocumentResult
from src.backend.exporters.docx_exporter import DocxExporter
from src.backend.database.db import create_document
from src.backend.auth.security import get_current_user, login_required, login_required_view
from src.backend.llm.key_tour_manager import KeyTourManager

logger = logging.getLogger(__name__)

studio_bp = Blueprint("studio_bp", __name__)

@studio_bp.route("/studio", methods=["GET"])
@login_required_view
def studio_page():
    """Trang OCR Studio bóc tách tài liệu."""
    user = get_current_user()
    return render_template("studio.html", user=user, active_page="studio")

@studio_bp.route("/api/process", methods=["POST"])
@login_required
def api_process():
    """Xu ly boc tach tai lieu voi co che Fast-Path va Tour xoay Key."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Vui long dang nhap de thuc hien thao tac"}), 401

    if "file" not in request.files:
        return jsonify({"error": "Khong tim thay tep tai len"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "Chua chon tep"}), 400

    model_choice = request.form.get("model_choice", "auto")
    doc_lang = request.form.get("language", "vi")
    fast_path = request.form.get("fast_path", "true").lower() == "true"

    # Xac dinh che do bóc tách dua tren lua chon mo hinh
    mode = "STANDALONE"
    gemini_key = ""
    gemini_model = "gemini-3.6-flash"
    kaggle_url = ""
    active_key_id = None

    if model_choice == "kaggle":
        mode = "HYBRID_KAGGLE"
        picked = KeyTourManager.get_next_key("kaggle")
        if picked:
            kaggle_url = picked["key_value"]
            active_key_id = picked["id"]
    elif model_choice in ["gemini-flash", "gemini-pro", "gemini-3.6-flash"]:
        mode = "STANDALONE"
        picked = KeyTourManager.get_next_key("gemini")
        if picked:
            gemini_key = picked["key_value"]
            gemini_model = picked.get("model_name") or "gemini-3.6-flash"
            active_key_id = picked["id"]
    elif model_choice == "groq":
        mode = "STANDALONE"
        picked = KeyTourManager.get_next_key("groq")
        if picked:
            active_key_id = picked["id"]
    elif model_choice == "mock":
        mode = "LOCAL_MOCK"
    else:  # auto
        mode = "STANDALONE"
        picked = KeyTourManager.get_next_key("gemini")
        if picked:
            gemini_key = picked["key_value"]
            gemini_model = picked.get("model_name") or "gemini-3.6-flash"
            active_key_id = picked["id"]

    settings = AppSettings(
        ocr_mode=mode,
        fast_path_enabled=fast_path,
        kaggle_endpoint=kaggle_url,
        gemini_api_key=gemini_key,
        gemini_model=gemini_model
    )

    engine = HybridDocumentEngine(settings=settings)
    file_bytes = uploaded_file.read()
    file_size = len(file_bytes)
    doc_id = str(uuid.uuid4())[:8]

    try:
        result = engine.process_document(
            file_bytes=file_bytes,
            filename=uploaded_file.filename,
            document_id=doc_id
        )

        # Ghi nhan luot dung cho API Key trong tour xoay
        if active_key_id:
            KeyTourManager.record_usage(active_key_id)

        # Luu vao CSDL gan chat voi user_id cua nguoi dung dang dang nhap
        try:
            create_document(
                user_id=user["id"],
                filename=result.filename,
                file_size=file_size,
                total_pages=result.total_pages,
                digital_pages=result.digital_pages_count,
                scanned_pages=result.scanned_pages_count,
                full_markdown=result.full_markdown,
                model_used=model_choice if model_choice != "auto" else ("Fast-Path + " + mode),
                language=doc_lang,
                processing_time=result.processing_time_seconds
            )
        except Exception as db_err:
            logger.warning(f"Khong the luu tai lieu vao CSDL: {db_err}")

        return jsonify({
            "document_id": result.document_id,
            "filename": result.filename,
            "total_pages": result.total_pages,
            "digital_pages_count": result.digital_pages_count,
            "scanned_pages_count": result.scanned_pages_count,
            "full_markdown": result.full_markdown,
            "processing_time_seconds": result.processing_time_seconds,
            "page_images": result.page_images
        })
    except Exception as e:
        logger.error(f"Loi xu ly tai lieu: {str(e)}")
        return jsonify({"error": str(e)}), 500

@studio_bp.route("/api/download/docx", methods=["POST"])
@login_required
def api_download_docx():
    """Xuat tep ket qua boc tach ra dinh dang Microsoft Word (.docx)."""
    data = request.get_json() or {}
    try:
        doc_res = DocumentResult(
            document_id=data.get("document_id", "doc-1"),
            filename=data.get("filename", "document.pdf"),
            total_pages=data.get("total_pages", 1),
            digital_pages_count=data.get("digital_pages_count", 1),
            scanned_pages_count=data.get("scanned_pages_count", 0),
            full_markdown=data.get("full_markdown", ""),
            processing_time_seconds=0.0,
            pages=[]
        )

        docx_bytes = DocxExporter.export_to_bytes(doc_res)
        return send_file(
            io.BytesIO(docx_bytes),
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=f"{doc_res.filename}.docx"
        )
    except Exception as e:
        logger.error(f"Loi xuat file Word: {e}")
        return jsonify({"error": str(e)}), 500
