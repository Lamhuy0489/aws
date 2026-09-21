import os
import sys
import io
import uuid
import logging
from flask import Flask, request, jsonify, render_template, send_file, session
from werkzeug.security import check_password_hash

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.backend.config.settings import AppSettings
from src.backend.parsers.hybrid_engine import HybridDocumentEngine, DocumentResult
from src.backend.exporters.docx_exporter import DocxExporter
from src.backend.database.db import (
    init_db, get_user_by_username, get_user_by_id, create_user,
    create_document, get_documents_by_user, get_document_by_id, delete_document,
    get_all_api_keys, create_api_key, toggle_api_key_status, delete_api_key
)
from src.backend.auth.security import get_current_user, login_required, admin_required
from src.backend.llm.key_tour_manager import KeyTourManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY", "hybrid-ocr-enterprise-secret-key-2026")

SAMPLE_DIR = os.path.join(PROJECT_ROOT, "data", "sample_documents")
os.makedirs(SAMPLE_DIR, exist_ok=True)

# Khởi tạo CSDL khi khởi động ứng dụng
init_db()

def _get_system_font_path():
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/SFNS.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def generate_sample_pdfs():
    """Tạo tệp PDF mẫu nếu chưa có."""
    import fitz
    font_path = _get_system_font_path()
    invoice_path = os.path.join(SAMPLE_DIR, "sample_invoice.pdf")

    doc = fitz.open()
    page1 = doc.new_page(width=595, height=842)
    font_alias = "helv"
    if font_path:
        page1.insert_font(fontname="f_vn", fontfile=font_path)
        font_alias = "f_vn"

    page1.insert_text((50, 45), "CÔNG TY CỔ PHẦN CÔNG NGHỆ ĐÁM MÂY CLOUD JOURNEY", fontname=font_alias, fontsize=12)
    page1.insert_text((50, 65), "Địa chỉ: Tầng 10, Tòa nhà Công nghệ, Hà Nội | MST: 0109988776", fontname=font_alias, fontsize=9)
    page1.insert_text((50, 95), "HÓA ĐƠN DỊCH VỤ ĐIỆN TOÁN ĐÁM MÂY (AWS BILLING INVOICE)", fontname=font_alias, fontsize=14)
    page1.insert_text((50, 115), "Số hóa đơn: INV-2026-09-001 | Ngày lập: 21/09/2026", fontname=font_alias, fontsize=10)
    page1.insert_text((50, 130), "Khách hàng: Công ty Cổ phần Giải pháp Doanh nghiệp Việt Nam", fontname=font_alias, fontsize=10)

    # Kẻ lưới bảng chi phí
    shape = page1.new_shape()
    shape.draw_rect(fitz.Rect(50, 150, 545, 280))
    shape.draw_line((50, 175), (545, 175))
    shape.draw_line((50, 205), (545, 205))
    shape.draw_line((50, 235), (545, 235))
    shape.draw_line((50, 260), (545, 260))
    shape.draw_line((80, 150), (80, 280))
    shape.draw_line((260, 150), (260, 280))
    shape.draw_line((360, 150), (360, 280))
    shape.draw_line((440, 150), (440, 280))
    shape.finish(color=(0.2, 0.2, 0.2), width=1)
    shape.commit()

    page1.insert_text((55, 168), "STT", fontname=font_alias, fontsize=9)
    page1.insert_text((85, 168), "Tên Dịch Vụ AWS", fontname=font_alias, fontsize=9)
    page1.insert_text((265, 168), "Số Lượng", fontname=font_alias, fontsize=9)
    page1.insert_text((365, 168), "Đơn Giá (VNĐ)", fontname=font_alias, fontsize=9)
    page1.insert_text((445, 168), "Thành Tiền (VNĐ)", fontname=font_alias, fontsize=9)

    page1.insert_text((60, 195), "1", fontname=font_alias, fontsize=9)
    page1.insert_text((85, 195), "Amazon EC2 t3.medium", fontname=font_alias, fontsize=9)
    page1.insert_text((265, 195), "2 instances", fontname=font_alias, fontsize=9)
    page1.insert_text((365, 195), "750,000", fontname=font_alias, fontsize=9)
    page1.insert_text((445, 195), "1,500,000", fontname=font_alias, fontsize=9)

    page1.insert_text((60, 225), "2", fontname=font_alias, fontsize=9)
    page1.insert_text((85, 225), "Amazon S3 Standard Storage", fontname=font_alias, fontsize=9)
    page1.insert_text((265, 225), "250 GB", fontname=font_alias, fontsize=9)
    page1.insert_text((365, 225), "1,200", fontname=font_alias, fontsize=9)
    page1.insert_text((445, 225), "300,000", fontname=font_alias, fontsize=9)

    page1.insert_text((60, 250), "3", fontname=font_alias, fontsize=9)
    page1.insert_text((85, 250), "Amazon DynamoDB On-Demand", fontname=font_alias, fontsize=9)
    page1.insert_text((265, 250), "5,000,000 calls", fontname=font_alias, fontsize=9)
    page1.insert_text((365, 250), "0.05", fontname=font_alias, fontsize=9)
    page1.insert_text((445, 250), "250,000", fontname=font_alias, fontsize=9)

    page1.insert_text((60, 273), "4", fontname=font_alias, fontsize=9)
    page1.insert_text((85, 273), "Amazon API Gateway", fontname=font_alias, fontsize=9)
    page1.insert_text((265, 273), "1,500,000 reqs", fontname=font_alias, fontsize=9)
    page1.insert_text((365, 273), "1.00", fontname=font_alias, fontsize=9)
    page1.insert_text((445, 273), "1,500,000", fontname=font_alias, fontsize=9)

    page1.insert_text((50, 310), "Tổng thanh toán trước thuế: 3,550,000 VNĐ", fontname=font_alias, fontsize=10)
    page1.insert_text((50, 330), "Thuế giá trị gia tăng (VAT 10%): 355,000 VNĐ", fontname=font_alias, fontsize=10)
    page1.insert_text((50, 350), "Tổng cộng tiền thanh toán: 3,905,000 VNĐ", fontname=font_alias, fontsize=11)
    page1.insert_text((50, 380), "Ghi chú: Dịch vụ tuân thủ các chuẩn Well-Architected về độ tin cậy và bảo mật.", fontname=font_alias, fontsize=9)
    page1.insert_text((50, 420), "Người lập biểu: Nguyễn Văn A | Kế toán trưởng: Trần Thị B", fontname=font_alias, fontsize=10)

    # Trang 2: Giả lập scan
    page2 = doc.new_page(width=595, height=842)
    s2 = page2.new_shape()
    s2.draw_rect(fitz.Rect(40, 40, 555, 800))
    s2.finish(color=(0.3, 0.3, 0.3), fill=(0.95, 0.95, 0.93))
    s2.commit()

    doc.save(invoice_path)
    doc.close()

    # Tệp mẫu 2: Hợp đồng
    contract_path = os.path.join(SAMPLE_DIR, "sample_contract.pdf")
    doc2 = fitz.open()
    c_page = doc2.new_page(width=595, height=842)
    c_alias = "helv"
    if font_path:
        c_page.insert_font(fontname="f_vn", fontfile=font_path)
        c_alias = "f_vn"

    c_page.insert_text((150, 50), "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", fontname=c_alias, fontsize=11)
    c_page.insert_text((190, 70), "Độc lập - Tự do - Hạnh phúc", fontname=c_alias, fontsize=10)
    c_page.insert_text((100, 110), "HỢP ĐỒNG KINH TẾ DỊCH VỤ CÔNG NGHỆ THÔNG TIN", fontname=c_alias, fontsize=13)
    c_page.insert_text((220, 130), "Số: 88/2026/HĐKT-CLOUD", fontname=c_alias, fontsize=10)

    c_text = (
        "Căn cứ Bộ luật Dân sự nước CHXHCN Việt Nam năm 2015;\n\n"
        "BÊN A (BÊN SỬ DỤNG DỊCH VỤ):\n"
        "- Tên doanh nghiệp: Công ty Cổ phần Giải pháp Doanh nghiệp\n"
        "- Đại diện bởi: Ông Lâm Quang Huy - Chức vụ: Giám đốc Kỹ thuật\n\n"
        "BÊN B (BÊN CUNG CẤP DỊCH VỤ):\n"
        "- Tên doanh nghiệp: Trung tâm Đào tạo First Cloud Journey (FCJ)\n"
        "- Đại diện bởi: Ban điều hành Cộng đồng AWS Study Group\n\n"
        "ĐIỀU 1: PHẠM VI DỊCH VỤ\n"
        "Bên B cung cấp nền tảng xử lý và bóc tách tài liệu số thông minh trên nền tảng AWS cho Bên A.\n\n"
        "ĐIỀU 2: TIÊU CHUẨN KỸ THUẬT VÀ BẢO MẬT\n"
        "- 100% dữ liệu tài liệu được bảo vệ an toàn bằng AWS KMS.\n"
        "- Tỷ lệ bóc tách giữ nguyên bố cục bảng biểu đạt tối thiểu 95%."
    )
    c_page.insert_text((50, 170), c_text, fontname=c_alias, fontsize=10)

    c_shape = c_page.new_shape()
    c_shape.draw_rect(fitz.Rect(50, 550, 545, 670))
    c_shape.draw_line((297, 550), (297, 670))
    c_shape.draw_line((50, 580), (545, 580))
    c_shape.finish(color=(0.2, 0.2, 0.2), width=1)
    c_shape.commit()

    c_page.insert_text((100, 570), "ĐẠI DIỆN BÊN A", fontname=c_alias, fontsize=10)
    c_page.insert_text((350, 570), "ĐẠI DIỆN BÊN B", fontname=c_alias, fontsize=10)
    c_page.insert_text((85, 600), "(Ký, ghi rõ họ tên và đóng dấu)", fontname=c_alias, fontsize=9)
    c_page.insert_text((335, 600), "(Ký, ghi rõ họ tên và đóng dấu)", fontname=c_alias, fontsize=9)

    doc2.save(contract_path)
    doc2.close()

generate_sample_pdfs()

# --- Định tuyến Giao diện & Tệp mẫu ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sample/<filename>")
def get_sample(filename):
    file_path = os.path.join(SAMPLE_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="application/pdf")
    return jsonify({"error": "Không tìm thấy tệp mẫu"}), 404

# --- API Xác Thực Người Dùng (Auth Endpoints) ---

@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"error": "Vui lòng nhập đầy đủ thông tin"}), 400

    if get_user_by_username(username):
        return jsonify({"error": "Tên đăng nhập đã tồn tại"}), 409

    try:
        user = create_user(username, email, password, role="user")
        session["user_id"] = user["id"]
        return jsonify({"message": "Đăng ký thành công", "user": user})
    except Exception as e:
        return jsonify({"error": f"Lỗi tạo tài khoản: {str(e)}"}), 500

@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    user = get_user_by_username(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Tên đăng nhập hoặc mật khẩu không chính xác"}), 401

    session["user_id"] = user["id"]
    return jsonify({
        "message": "Đăng nhập thành công",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    })

@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    session.clear()
    return jsonify({"message": "Đã đăng xuất thành công"})

@app.route("/api/auth/me", methods=["GET"])
def auth_me():
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

# --- API Kho Lưu Trữ Tài Liệu (Document Library Endpoints) ---

@app.route("/api/documents", methods=["GET"])
def list_user_documents():
    user = get_current_user()
    user_id = user["id"] if user else "demo"
    docs = get_documents_by_user(user_id)
    return jsonify({"documents": docs})

@app.route("/api/documents/<doc_id>", methods=["GET"])
def get_document_details(doc_id):
    user = get_current_user()
    user_id = user["id"] if user else None
    doc = get_document_by_id(doc_id, user_id)
    if not doc:
        return jsonify({"error": "Không tìm thấy tài liệu"}), 404
    return jsonify({"document": doc})

@app.route("/api/documents/<doc_id>", methods=["DELETE"])
def remove_document(doc_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Vui lòng đăng nhập"}), 401
    success = delete_document(doc_id, user["id"])
    if not success:
        return jsonify({"error": "Không thể xóa tài liệu"}), 404
    return jsonify({"message": "Đã xóa tài liệu thành công"})

# --- API Quản Trị Viên (Admin Key Tour Endpoints) ---

@app.route("/api/admin/keys", methods=["GET"])
@admin_required
def admin_list_keys():
    keys = get_all_api_keys()
    # Ẩn bớt ký tự nhạy cảm khi hiển thị
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

@app.route("/api/admin/keys", methods=["POST"])
@admin_required
def admin_add_key():
    data = request.get_json() or {}
    provider = data.get("provider", "gemini").lower()
    key_alias = data.get("key_alias", "").strip()
    key_value = data.get("key_value", "").strip()
    model_name = data.get("model_name", "gemini-1.5-flash").strip()
    base_url = data.get("base_url", "").strip()
    priority = int(data.get("priority", 1))

    if not key_alias or not key_value:
        return jsonify({"error": "Vui lòng nhập tên gợi nhớ và giá trị Key"}), 400

    new_key = create_api_key(provider, key_alias, key_value, model_name, base_url, priority)
    return jsonify({"message": "Thêm API Key thành công", "key": new_key})

@app.route("/api/admin/keys/<key_id>/toggle", methods=["POST"])
@admin_required
def admin_toggle_key(key_id):
    new_status = toggle_api_key_status(key_id)
    if new_status is None:
        return jsonify({"error": "Không tìm thấy key"}), 404
    return jsonify({"message": "Đã thay đổi trạng thái key", "is_active": new_status})

@app.route("/api/admin/keys/<key_id>", methods=["DELETE"])
@admin_required
def admin_delete_key(key_id):
    success = delete_api_key(key_id)
    if not success:
        return jsonify({"error": "Không tìm thấy key để xóa"}), 404
    return jsonify({"message": "Đã xóa API Key thành công"})

# --- API Bóc Tách Tài Liệu (Processing Endpoint) ---

@app.route("/api/process", methods=["POST"])
def process_file():
    if "file" not in request.files:
        return jsonify({"error": "Không tìm thấy tệp tải lên"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "Tên tệp không hợp lệ"}), 400

    mode = request.form.get("mode", "LOCAL_MOCK")
    model_choice = request.form.get("model_choice", "auto")
    fast_path = request.form.get("fast_path", "true").lower() == "true"
    kaggle_url = request.form.get("kaggle_url", "").strip()
    gemini_key = request.form.get("gemini_key", "").strip()
    doc_lang = request.form.get("language", "vi")

    # Cơ chế xoay tour API Key từ cơ sở dữ liệu nếu người dùng không truyền thủ công
    active_key_id = None
    if mode == "STANDALONE" and not gemini_key:
        picked = KeyTourManager.get_next_key("gemini")
        if picked:
            gemini_key = picked["key_value"]
            active_key_id = picked["id"]

    if mode == "HYBRID_KAGGLE" and not kaggle_url:
        picked = KeyTourManager.get_next_key("kaggle")
        if picked:
            kaggle_url = picked["key_value"]
            active_key_id = picked["id"]

    settings = AppSettings(
        ocr_mode=mode,
        fast_path_enabled=fast_path,
        kaggle_endpoint=kaggle_url,
        gemini_api_key=gemini_key
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

        # Cập nhật số lượt gọi xoay tour cho Key
        if active_key_id:
            KeyTourManager.record_usage(active_key_id)

        # Lưu tài liệu vào Kho CSDL cho người dùng hiện tại (hoặc demo)
        user = get_current_user()
        owner_id = user["id"] if user else "demo"
        try:
            create_document(
                user_id=owner_id,
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
            logger.warning(f"Không thể lưu tài liệu vào CSDL: {db_err}")

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
        logger.error(f"Lỗi trong quá trình xử lý: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/download/docx", methods=["POST"])
def download_docx():
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
        logger.error(f"Lỗi xuất file Word: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("=" * 60)
    print(f"GIAO DIỆN WEB HYBRID DOCUMENT OCR ĐANG CHẠY TẠI:")
    print(f"http://localhost:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False)
