import pytest
from src.backend.parsers.hybrid_engine import DocumentResult, ParsedPage
from src.backend.exporters.markdown_exporter import MarkdownExporter
from src.backend.exporters.docx_exporter import DocxExporter

@pytest.fixture
def sample_document_result():
    pages = [
        ParsedPage(
            page_number=1,
            is_scanned=False,
            markdown_content="# HỢP ĐỒNG KINH TẾ\n\nĐiều 1: Nội dung hợp đồng.",
            character_count=100,
            tables_count=0
        ),
        ParsedPage(
            page_number=2,
            is_scanned=True,
            markdown_content="| Hàng mục | Chi phí |\n| --- | --- |\n| Phí dịch vụ | 1,000,000 |",
            character_count=80,
            tables_count=1
        )
    ]
    return DocumentResult(
        document_id="doc-1234",
        filename="test_contract.pdf",
        total_pages=2,
        digital_pages_count=1,
        scanned_pages_count=1,
        full_markdown="# HỢP ĐỒNG KINH TẾ\n\nĐiều 1: Nội dung hợp đồng.\n\n| Hàng mục | Chi phí |\n| --- | --- |\n| Phí dịch vụ | 1,000,000 |",
        processing_time_seconds=1.25,
        pages=pages
    )

def test_markdown_exporter(sample_document_result):
    md_str = MarkdownExporter.export_to_string(sample_document_result)
    assert "# Báo Cáo Bóc Tách Tài Liệu: test_contract.pdf" in md_str
    assert "doc-1234" in md_str
    assert "1.25 giây" in md_str
    assert "| Hàng mục | Chi phí |" in md_str

def test_docx_exporter(sample_document_result):
    docx_bytes = DocxExporter.export_to_bytes(sample_document_result)
    assert docx_bytes is not None
    assert len(docx_bytes) > 0
    # Chữ ký tệp DOCX (định dạng tệp zip bắt đầu bằng PK\x03\x04)
    assert docx_bytes[:2] == b"PK"
