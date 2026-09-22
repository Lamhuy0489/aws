import os
import io
import uuid
import logging
from flask import Blueprint, request, jsonify, render_template, send_file, session

from src.backend.config.settings import AppSettings
from src.backend.parsers.hybrid_engine import HybridDocumentEngine, DocumentResult
from src.backend.exporters.docx_exporter import DocxExporter
from src.backend.exporters.pdf_exporter import PdfExporter
from src.backend.llm.translator import DocumentTranslator
from src.backend.database.db import (
    create_document,
    get_document_by_id,
    get_documents_by_user,
    update_document_translation
)
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
    gemini_model = "gemini-flash-lite-latest"
    kaggle_url = ""
    active_key_id = None

    if model_choice == "kaggle":
        mode = "HYBRID_KAGGLE"
        picked = KeyTourManager.get_next_key("kaggle")
        if picked:
            kaggle_url = picked["key_value"]
            active_key_id = picked["id"]
        if not kaggle_url:
            kaggle_url = os.getenv("KAGGLE_ENDPOINT", "")
        # Luôn cung cấp thêm Gemini Key làm dự phòng chuyển đổi tức thì (Failover) nếu Kaggle quá tải/timeout
        gemini_fallback = KeyTourManager.get_next_key("gemini")
        if gemini_fallback:
            gemini_key = gemini_fallback["key_value"]
            gemini_model = gemini_fallback.get("model_name") or "gemini-flash-lite-latest"
    elif model_choice in ["gemini-flash", "gemini-pro", "gemini-3.6-flash", "gemini-flash-lite-latest"]:
        mode = "STANDALONE"
        picked = KeyTourManager.get_next_key("gemini")
        if picked:
            gemini_key = picked["key_value"]
            gemini_model = picked.get("model_name") or "gemini-flash-lite-latest"
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
            gemini_model = picked.get("model_name") or "gemini-flash-lite-latest"
            active_key_id = picked["id"]

    settings = AppSettings(
        ocr_mode=mode,
        fast_path_enabled=fast_path,
        kaggle_endpoint=kaggle_url,
        gemini_api_key=gemini_key,
        gemini_model=gemini_model,
        timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "120"))
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
        created_doc = None
        try:
            created_doc = create_document(
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
            if created_doc and "id" in created_doc:
                session["active_document_id"] = created_doc["id"]
        except Exception as db_err:
            logger.warning(f"Khong the luu tai lieu vao CSDL: {db_err}")

        final_doc_id = (created_doc and created_doc.get("id")) or result.document_id

        # Đồng bộ lưu trữ lên AWS Cloud (S3 và DynamoDB) nếu có kết nối
        try:
            from src.backend.cloud.aws_storage import AWSStorageService
            aws_svc = AWSStorageService()
            if aws_svc.is_connected:
                s3_in_key = f"uploads/{final_doc_id}/{result.filename}"
                s3_in_uri = aws_svc.upload_file(
                    file_bytes,
                    s3_in_key,
                    content_type="application/pdf" if result.filename.lower().endswith(".pdf") else "image/png"
                )
                s3_out_key = f"outputs/{final_doc_id}/{result.filename}.md"
                s3_out_uri = aws_svc.upload_file(
                    result.full_markdown.encode("utf-8"),
                    s3_out_key,
                    content_type="text/markdown"
                )
                aws_svc.record_job(
                    job_id=final_doc_id,
                    filename=result.filename,
                    user_id=user["id"],
                    username=user.get("username", "anonymous"),
                    status="COMPLETED",
                    total_pages=result.total_pages,
                    digital_pages=result.digital_pages_count,
                    scanned_pages=result.scanned_pages_count,
                    processing_time_seconds=result.processing_time_seconds,
                    s3_input_uri=s3_in_uri or "",
                    s3_output_md_uri=s3_out_uri or "",
                    model_used=model_choice if model_choice != "auto" else ("Fast-Path + " + mode)
                )
        except Exception as aws_sync_err:
            logger.info(f"Lưu trữ AWS Cloud được bỏ qua hoặc ghi nhận nhẹ: {aws_sync_err}")

        return jsonify({
            "document_id": final_doc_id,
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

@studio_bp.route("/api/download/pdf", methods=["POST"])
@login_required
def api_download_pdf():
    """Xuat tep ket qua boc tach ra dinh dang PDF (.pdf) chuan A4 in an."""
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

        pdf_bytes = PdfExporter.export_to_bytes(doc_res)
        clean_filename = doc_res.filename
        if clean_filename.lower().endswith(".pdf"):
            download_name = clean_filename[:-4] + "_extracted.pdf"
        else:
            download_name = f"{clean_filename}.pdf"

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=download_name
        )
    except Exception as e:
        logger.error(f"Loi xuat file PDF: {e}")
        return jsonify({"error": str(e)}), 500

@studio_bp.route("/api/translate", methods=["POST"])
@login_required
def api_translate():
    """Dich thuat noi dung tai lieu Markdown sang ngon ngu dich chi dinh bang AI Gemini."""
    user = get_current_user()
    data = request.get_json() or {}
    markdown_text = data.get("markdown", "")
    target_lang = data.get("target_lang", "vi")
    model_name = data.get("model", "")

    if not markdown_text.strip():
        return jsonify({"error": "Noi dung can dich khong duoc de trong"}), 400

    try:
        translated_md = DocumentTranslator.translate_markdown(
            markdown_text=markdown_text,
            target_lang=target_lang,
            model_name=model_name or "gemini-flash-lite-latest"
        )

        active_doc_id = session.get("active_document_id")
        if active_doc_id and user:
            try:
                update_document_translation(active_doc_id, user["id"], translated_md)
            except Exception as up_err:
                logger.warning(f"Khong the cap nhat ban dich vao CSDL: {up_err}")

        return jsonify({
            "translated_markdown": translated_md,
            "target_lang": target_lang
        })
    except Exception as e:
        logger.error(f"Loi dich thuat: {e}")
        return jsonify({"error": str(e)}), 500

@studio_bp.route("/api/studio/active-document", methods=["GET", "POST", "DELETE"])
@login_required
def api_active_document():
    """Quan ly tai lieu dang duoc thao tac trong Studio de bao toan trang thai khi reload hoac chuyen tab."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Vui long dang nhap"}), 401

    if request.method == "POST":
        data = request.get_json() or {}
        doc_id = data.get("document_id")
        if doc_id:
            session["active_document_id"] = doc_id
            return jsonify({"success": True, "active_document_id": doc_id})
        return jsonify({"error": "Thieu document_id"}), 400

    elif request.method == "DELETE":
        session.pop("active_document_id", None)
        return jsonify({"success": True})

    # GET: Lay tai lieu dang active
    active_id = session.get("active_document_id")
    if active_id:
        doc = get_document_by_id(active_id, user_id=user["id"])
        if doc:
            return jsonify({"document": doc})

    # Neu session chua co hoac tai lieu khong con, lay tai lieu moi nhat cua user
    docs = get_documents_by_user(user["id"])
    if docs:
        latest = get_document_by_id(docs[0]["id"], user_id=user["id"])
        if latest:
            session["active_document_id"] = latest["id"]
            return jsonify({"document": latest})

    return jsonify({"document": None})

