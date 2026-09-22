import os
import sys
import logging
from flask import Flask, redirect, render_template, send_file, jsonify

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.backend.database.db import init_db
from src.backend.auth.security import get_current_user
from src.frontend.blueprints.auth import auth_bp
from src.frontend.blueprints.studio import studio_bp
from src.frontend.blueprints.library import library_bp
from src.frontend.blueprints.admin import admin_bp
from src.frontend.blueprints.settings import settings_bp

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)
app.secret_key = os.getenv("SECRET_KEY", "hybrid-ocr-enterprise-secret-key-2026")

SAMPLE_DIR = os.path.join(PROJECT_ROOT, "data", "sample_documents")
os.makedirs(SAMPLE_DIR, exist_ok=True)

# Khoi tao CSDL khi khoi dong ung dung
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
    """Tao tep PDF mau neu chua co."""
    import fitz
    font_path = _get_system_font_path()
    invoice_path = os.path.join(SAMPLE_DIR, "sample_invoice.pdf")

    if not os.path.exists(invoice_path):
        doc = fitz.open()
        page1 = doc.new_page(width=595, height=842)
        font_alias = "helv"
        if font_path:
            page1.insert_font(fontname="f_vn", fontfile=font_path)
            font_alias = "f_vn"

        page1.insert_text((50, 45), "CONG TY CO PHAN CONG NGHE DAM MAY CLOUD JOURNEY", fontname=font_alias, fontsize=12)
        page1.insert_text((50, 65), "Dia chi: Tang 10, Toa nha Cong nghe, Ha Noi | MST: 0109988776", fontname=font_alias, fontsize=9)
        page1.insert_text((50, 95), "HOA DON DICH VU DIEN TOAN DAM MAY (AWS BILLING INVOICE)", fontname=font_alias, fontsize=14)
        page1.insert_text((50, 115), "So hoa don: INV-2026-09-001 | Ngay lap: 21/09/2026", fontname=font_alias, fontsize=10)
        page1.insert_text((50, 130), "Khach hang: Cong ty Co phan Giai phap Doanh nghiep Viet Nam", fontname=font_alias, fontsize=10)

        # Ke luoi bang chi phi
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
        page1.insert_text((85, 168), "Ten Dich Vu AWS", fontname=font_alias, fontsize=9)
        page1.insert_text((265, 168), "So Luong", fontname=font_alias, fontsize=9)
        page1.insert_text((365, 168), "Don Gia (VND)", fontname=font_alias, fontsize=9)
        page1.insert_text((445, 168), "Thanh Tien (VND)", fontname=font_alias, fontsize=9)

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
        page1.insert_text((265, 250), "5,000,000 ops", fontname=font_alias, fontsize=9)
        page1.insert_text((365, 250), "0.5", fontname=font_alias, fontsize=9)
        page1.insert_text((445, 250), "2,500,000", fontname=font_alias, fontsize=9)

        page1.insert_text((55, 273), "Tong Cong:", fontname=font_alias, fontsize=10)
        page1.insert_text((445, 273), "4,300,000 VND", fontname=font_alias, fontsize=10)

        page1.insert_text((50, 310), "Ghi chu: Gia tren chua bao gom 10% Thue Gia tri gia tang (VAT).", fontname=font_alias, fontsize=9)
        page1.insert_text((50, 325), "Vui long thanh toan vao Tai khoan Cong ty trong vong 15 ngay ke tu ngay lap hoa don.", fontname=font_alias, fontsize=9)
        page1.insert_text((50, 340), "Ngan hang: Techcombank - Chi nhanh Ha Noi | STK: 19038899221100", fontname=font_alias, fontsize=9)
        page1.insert_text((50, 370), "Nguoi lap bieu: Nguyen Van A", fontname=font_alias, fontsize=9)
        page1.insert_text((380, 370), "Ke toan truong: Tran Thi B", fontname=font_alias, fontsize=9)

        doc.save(invoice_path)
        doc.close()

# Khoi tao tep mau
generate_sample_pdfs()

# Dang ky cac Blueprints theo kien truc da trang
app.register_blueprint(auth_bp)
app.register_blueprint(studio_bp)
app.register_blueprint(library_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(settings_bp)

@app.route("/")
def index_redirect():
    """Tuyen duong goc: Tu dong chuyen huong thong minh theo trang thai dang nhap va vai tro."""
    user = get_current_user()
    if not user:
        return redirect("/login")
    if user.get("role") == "admin":
        return redirect("/admin")
    return redirect("/studio")

@app.route("/data/sample_documents/<filename>")
def serve_sample_documents(filename):
    """Cung cap tep tai lieu mau cho giao dien."""
    filepath = os.path.join(SAMPLE_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Tep mau khong ton tai"}), 404
    return send_file(filepath, mimetype="application/pdf")

@app.errorhandler(403)
def page_forbidden(e):
    """Trang chan quyen truy cap 403 Forbidden."""
    user = get_current_user()
    return render_template("403.html", user=user), 403

@app.errorhandler(404)
def page_not_found(e):
    """Trang bao loi 404 Not Found."""
    return jsonify({"error": "Duong dan khong ton tai tren he thong", "code": "NOT_FOUND"}), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("=" * 60)
    print("GIAO DIEN WEB HYBRID DOCUMENT OCR ENTERPRISE DANG CHAY TAI:")
    print(f"http://localhost:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False)
