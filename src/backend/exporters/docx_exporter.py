import io
import os
import re
import logging
from typing import List
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from src.backend.parsers.hybrid_engine import DocumentResult

logger = logging.getLogger(__name__)

class DocxExporter:
    """Chuyển đổi nội dung Markdown và bảng biểu thành tài liệu Microsoft Word (.docx)."""
    @staticmethod
    def export_to_bytes(result: DocumentResult) -> bytes:
        doc = Document()

        # Tiêu đề tài liệu
        title = doc.add_heading(f"Tài Liệu Đã Bóc Tách: {result.filename}", level=0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Thông tin tóm tắt
        meta_p = doc.add_paragraph()
        meta_p.add_run(f"Mã tài liệu: {result.document_id} | Tổng số trang: {result.total_pages} | "
                       f"Trang số: {result.digital_pages_count} | Trang scan: {result.scanned_pages_count}\n").italic = True

        doc.add_paragraph("―" * 40)

        # Xử lý từng dòng Markdown
        lines = result.full_markdown.split("\n")
        table_buffer: List[str] = []
        in_table = False

        for line in lines:
            trimmed = line.strip()

            # Phát hiện khối bảng Markdown
            if trimmed.startswith("|") and trimmed.endswith("|"):
                in_table = True
                table_buffer.append(trimmed)
                continue
            else:
                if in_table and table_buffer:
                    DocxExporter._render_markdown_table_to_docx(doc, table_buffer)
                    table_buffer = []
                    in_table = False

            if not trimmed:
                continue

            # Tiêu đề phân cấp
            if trimmed.startswith("# "):
                doc.add_heading(trimmed[2:].strip(), level=1)
            elif trimmed.startswith("## "):
                doc.add_heading(trimmed[3:].strip(), level=2)
            elif trimmed.startswith("### "):
                doc.add_heading(trimmed[4:].strip(), level=3)
            elif trimmed.startswith("- ") or trimmed.startswith("* "):
                p = doc.add_paragraph(trimmed[2:].strip(), style="List Bullet")
            elif trimmed.startswith("<!--") and trimmed.endswith("-->"):
                # Ghi chú chuyển trang
                p = doc.add_paragraph(trimmed)
                p.runs[0].font.color.rgb = RGBColor(128, 128, 128)
                p.runs[0].font.size = Pt(9)
            else:
                doc.add_paragraph(trimmed)

        # Nếu tệp kết thúc bằng một bảng
        if in_table and table_buffer:
            DocxExporter._render_markdown_table_to_docx(doc, table_buffer)

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def export_to_file(result: DocumentResult, output_path: str) -> str:
        docx_bytes = DocxExporter.export_to_bytes(result)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(docx_bytes)
        logger.info(f"Đã xuất tệp Word (.docx) tại: {output_path}")
        return output_path

    @staticmethod
    def _render_markdown_table_to_docx(doc: Document, table_lines: List[str]):
        """Dựng bảng biểu Microsoft Word từ các dòng Markdown table."""
        rows = []
        for line in table_lines:
            cells = [c.strip() for c in line.strip("|").split("|")]
            # Bỏ qua dòng phân cách |---|---|
            if all(set(c).issubset({"-", ":", " "}) for c in cells):
                continue
            rows.append(cells)

        if not rows:
            return

        num_cols = max(len(r) for r in rows)
        table = doc.add_table(rows=len(rows), cols=num_cols)
        table.style = "Table Grid"

        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_value in enumerate(row_data):
                if col_idx < num_cols:
                    cell = table.cell(row_idx, col_idx)
                    cell.text = cell_value
                    # In đậm dòng tiêu đề đầu tiên
                    if row_idx == 0:
                        for p in cell.paragraphs:
                            for run in p.runs:
                                run.bold = True

        doc.add_paragraph()  # Thêm khoảng trống sau bảng
