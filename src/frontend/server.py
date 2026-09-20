import os
import sys
import io
import uuid
import logging

# Đảm bảo thư mục gốc dự án luôn nằm trong PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify, render_template, send_file
from src.backend.config.settings import AppSettings
from src.backend.parsers.hybrid_engine import HybridDocumentEngine, DocumentResult
from src.backend.exporters.docx_exporter import DocxExporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates")

# Thư mục chứa tài liệu mẫu
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_documents")
os.makedirs(SAMPLE_DIR, exist_ok=True)

def generate_sample_pdfs():
    """Tạo tệp PDF mẫu để phục vụ kiểm thử giao diện nếu chưa có."""
    import fitz

    invoice_path = os.path.join(SAMPLE_DIR, "sample_invoice.pdf")
    if not os.path.exists(invoice_path):
        doc = fitz.open()
        
        # Trang 1: PDF văn bản số có bảng biểu (Fast-Path)
        page1 = doc.new_page(width=595, height=842)
        p1_text = (
            "CÔNG TY CỔ PHẦN CÔNG NGHỆ ĐÁM MÂY CLOUD JOURNEY\n"
            "Địa chỉ: Tầng 10, Tòa nhà Công nghệ, Hà Nội | Mã số thuế: 0109988776\n\n"
            "HÓA ĐƠN DỊCH VỤ ĐIỆN TOÁN ĐÁM MÂY (AWS BILLING INVOICE)\n"
            "Số hóa đơn: INV-2026-09-001 | Ngày lập: 21/09/2026\n"
            "Khách hàng: Công ty Cổ phần Giải pháp Doanh nghiệp Việt Nam\n\n"
            "CHI TIẾT DỊCH VỤ SỬ DỤNG:\n"
            "- Máy chủ ảo Amazon EC2 t3.medium: 2 phiên bản (720 giờ)\n"
            "- Lưu trữ đám mây Amazon S3 Standard: 250 GB\n"
            "- Cơ sở dữ liệu phi quan hệ Amazon DynamoDB On-Demand: 5 triệu lượt đọc/ghi\n"
            "- Cổng kết nối bảo mật Amazon API Gateway: 1,500,000 requests\n\n"
            "Tổng thanh toán trước thuế: 3,500,000 VNĐ\n"
            "Thuế giá trị gia tăng (10%): 350,000 VNĐ\n"
            "Tổng cộng tiền thanh toán: 3,850,000 VNĐ\n\n"
            "Người lập biểu: Nguyễn Văn A | Kế toán trưởng: Trần Thị B"
        )
        page1.insert_text((50, 60), p1_text, fontsize=11, fontname="helv")

        # Trang 2: Giả lập trang ảnh scan (Chỉ có hình ảnh vẽ sẵn, không có text layer)
        page2 = doc.new_page(width=595, height=842)
        # Vẽ một số hình khối và khung chữ như một bản vẽ scan
        shape = page2.new_shape()
        shape.draw_rect(fitz.Rect(50, 50, 545, 750))
        shape.finish(color=(0.2, 0.2, 0.2), fill=(0.96, 0.96, 0.96))
        shape.commit()
        # Không chèn text layer để mật độ ký tự < 50, kích hoạt Tầng 2 OCR!
        
        doc.save(invoice_path)
        doc.close()
        logger.info(f"Đã tạo tệp mẫu: {invoice_path}")

    contract_path = os.path.join(SAMPLE_DIR, "sample_contract.pdf")
    if not os.path.exists(contract_path):
        doc = fitz.open()
        p = doc.new_page(width=595, height=842)
        c_text = (
            "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n"
            "Độc lập - Tự do - Hạnh phúc\n\n"
            "HỢP ĐỒNG KINH TẾ DỊCH VỤ CÔNG NGHỆ THÔNG TIN\n"
            "Số: 88/2026/HĐKT-CLOUD\n\n"
            "Căn cứ Bộ luật Dân sự nước CHXHCN Việt Nam năm 2015;\n"
            "Hôm nay, ngày 21 tháng 09 năm 2026, chúng tôi gồm các bên:\n\n"
            "BÊN A (BÊN SỬ DỤNG DỊCH VỤ):\n"
            "- Tên doanh nghiệp: Công ty Cổ phần Dịch vụ Số Một\n"
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
        p.insert_text((50, 60), c_text, fontsize=11, fontname="helv")
        doc.save(contract_path)
        doc.close()
        logger.info(f"Đã tạo tệp mẫu: {contract_path}")

# Khởi tạo tệp mẫu khi nạp server
generate_sample_pdfs()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sample/<filename>")
def get_sample(filename):
    file_path = os.path.join(SAMPLE_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="application/pdf")
    return jsonify({"error": "Không tìm thấy tệp mẫu"}), 404

@app.route("/api/process", methods=["POST"])
def process_file():
    if "file" not in request.files:
        return jsonify({"error": "Không tìm thấy tệp tải lên"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "Tên tệp không hợp lệ"}), 400

    mode = request.form.get("mode", "LOCAL_MOCK")
    fast_path = request.form.get("fast_path", "true").lower() == "true"
    kaggle_url = request.form.get("kaggle_url", "").strip()
    gemini_key = request.form.get("gemini_key", "").strip()

    # Khởi tạo cấu hình xử lý
    settings = AppSettings(
        ocr_mode=mode,
        fast_path_enabled=fast_path,
        kaggle_endpoint=kaggle_url,
        gemini_api_key=gemini_key
    )

    engine = HybridDocumentEngine(settings=settings)
    file_bytes = uploaded_file.read()
    doc_id = str(uuid.uuid4())[:8]

    try:
        result = engine.process_document(
            file_bytes=file_bytes,
            filename=uploaded_file.filename,
            document_id=doc_id
        )

        return jsonify({
            "document_id": result.document_id,
            "filename": result.filename,
            "total_pages": result.total_pages,
            "digital_pages_count": result.digital_pages_count,
            "scanned_pages_count": result.scanned_pages_count,
            "full_markdown": result.full_markdown,
            "processing_time_seconds": result.processing_time_seconds
        })
    except Exception as e:
        logger.error(f"Lỗi trong quá trình xử lý: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/download/docx", methods=["POST"])
def download_docx():
    data = request.get_json() or {}
    try:
        # Tái tạo DocumentResult từ dữ liệu client gửi lên
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
