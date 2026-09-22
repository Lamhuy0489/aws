import io
import pytest
from src.backend.parsers.fast_parser import FastNativeParser, ParsedPage

def test_convert_table_to_markdown():
    matrix = [
        ["Hạng mục", "Số lượng", "Đơn giá"],
        ["Máy chủ EC2", "2", "500,000"],
        ["Lưu trữ S3", "50 GB", "1,000"]
    ]
    md = FastNativeParser._convert_table_to_markdown(matrix)
    
    assert "| Hạng mục | Số lượng | Đơn giá |" in md
    assert "| :--- | :---: | ---: |" in md
    assert "| Máy chủ EC2 | 2 | 500,000 |" in md
    assert "| Lưu trữ S3 | 50 GB | 1,000 |" in md

def test_convert_empty_table():
    assert FastNativeParser._convert_table_to_markdown([]) == ""
    assert FastNativeParser._convert_table_to_markdown([[]]) == ""

def test_fast_parser_scan_threshold():
    parser = FastNativeParser(scan_threshold_chars=50)
    assert parser.scan_threshold_chars == 50

def test_no_false_positive_tables_on_scientific_paper():
    """Kiem tra tai lieu bai bao khoa hoc khong bi bien thanh bang gia 65 dong x 6 cot."""
    import os
    paper_path = "/Users/huylam/Downloads/28_Bai_Bao_Hoi nghi KH_Khoa_CNTT_2026.pdf"
    if not os.path.exists(paper_path):
        pytest.skip("Khong tim thay tep bai bao khoa hoc de kiem tra")

    with open(paper_path, "rb") as f:
        pdf_bytes = f.read()

    parser = FastNativeParser()
    pages = parser.parse_pdf(pdf_bytes)

    assert len(pages) == 11
    # Trang 1 cua bai bao khoa hoc khong duoc chua bat ky bang gia nao
    assert pages[0].tables_count == 0
    # Noi dung trang 1 phai chua day du Abstract va tieu de, khong bi bam nat boi dau gach dung |
    assert "## Abstract" in pages[0].markdown_content
    assert "Survey of Attributes for Anomaly Detection" in pages[0].markdown_content
    assert "## 1. Introduction" in pages[0].markdown_content
    assert pages[0].preview_png_b64 is not None
    # Base64 thuan khong duoc chua tien to data:image
    assert not pages[0].preview_png_b64.startswith("data:")
    assert pages[0].image_bytes is not None

def test_sample_invoice_real_table_extraction():
    """Kiem tra hoa don mau van trich xuat dung cau truc bang that."""
    import os
    from src.frontend.server import SAMPLE_DIR
    invoice_path = os.path.join(SAMPLE_DIR, "sample_invoice.pdf")
    if not os.path.exists(invoice_path):
        pytest.skip("Khong tim thay tep hoa don mau")

    with open(invoice_path, "rb") as f:
        pdf_bytes = f.read()

    parser = FastNativeParser()
    pages = parser.parse_pdf(pdf_bytes)

    assert len(pages) >= 1
    # Hoa don phai nhan dien duoc bang dich vu
    assert pages[0].tables_count >= 1
    assert "Amazon EC2" in pages[0].markdown_content
    assert "| STT |" in pages[0].markdown_content
