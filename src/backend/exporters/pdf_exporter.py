import io
import os
import re
import logging
import fitz
import markdown
from src.backend.parsers.hybrid_engine import DocumentResult

logger = logging.getLogger(__name__)

class PdfExporter:
    """Chuyển đổi kết quả bóc tách Markdown sang tài liệu PDF chuẩn A4 in ấn bằng PyMuPDF Story."""

    @staticmethod
    def export_to_bytes(result: DocumentResult) -> bytes:
        """Kết xuất kết quả tài liệu thành mảng byte của tệp PDF chuẩn in ấn A4."""
        # 1. Làm sạch ghi chú phân trang Markdown dạng HTML comment
        cleaned_md = re.sub(r"<!--\s*Trang\s*\d+.*?-->", "", result.full_markdown)

        # 2. Chuyển đổi Markdown sang HTML có bảng biểu
        html_body = markdown.markdown(
            cleaned_md,
            extensions=["tables", "fenced_code", "nl2br"]
        )

        # 3. CSS định dạng văn bản A4 chuẩn trang in
        css = """
        @page {
            size: A4;
            margin: 20mm;
        }
        body {
            font-family: sans-serif;
            font-size: 11pt;
            line-height: 1.45;
            color: #1e293b;
        }
        h1 {
            font-size: 16pt;
            font-weight: bold;
            color: #0f172a;
            margin-top: 16pt;
            margin-bottom: 10pt;
            border-bottom: 1.5px solid #2563eb;
            padding-bottom: 4pt;
        }
        h2 {
            font-size: 13.5pt;
            font-weight: bold;
            color: #1e293b;
            margin-top: 14pt;
            margin-bottom: 8pt;
        }
        h3 {
            font-size: 12pt;
            font-weight: 600;
            color: #334155;
            margin-top: 10pt;
            margin-bottom: 6pt;
        }
        h4 {
            font-size: 11pt;
            font-weight: 600;
            color: #475569;
            margin-top: 8pt;
            margin-bottom: 4pt;
        }
        p {
            margin-top: 0;
            margin-bottom: 8pt;
            text-align: justify;
        }
        ul, ol {
            margin-top: 4pt;
            margin-bottom: 8pt;
            padding-left: 20pt;
        }
        li {
            margin-bottom: 3pt;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10pt;
            margin-bottom: 12pt;
            font-size: 9.5pt;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 5pt 7pt;
            vertical-align: top;
        }
        th {
            background-color: #f1f5f9;
            font-weight: bold;
            color: #0f172a;
            text-align: left;
        }
        tr:nth-child(even) td {
            background-color: #f8fafc;
        }
        blockquote {
            border-left: 3px solid #94a3b8;
            padding-left: 10pt;
            margin-left: 0;
            margin-right: 0;
            color: #475569;
            font-style: italic;
        }
        code {
            font-family: monospace;
            background-color: #f1f5f9;
            padding: 1pt 3pt;
            font-size: 9.5pt;
            border-radius: 2pt;
        }
        pre {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 8pt;
            font-size: 9pt;
            line-height: 1.3;
        }
        """

        full_html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <style>{css}</style>
        </head>
        <body>
            {html_body}
        </body>
        </html>"""

        story = fitz.Story(html=full_html)

        # Kích thước trang A4: 595 x 842 points. Lề trang 54 points (khoảng 19mm)
        page_width, page_height = 595.0, 842.0
        margin_x, margin_y = 54.0, 54.0
        content_rect = fitz.Rect(margin_x, margin_y, page_width - margin_x, page_height - margin_y)
        mediabox = fitz.Rect(0, 0, page_width, page_height)

        out_buffer = io.BytesIO()
        writer = fitz.DocumentWriter(out_buffer)
        story.write(writer, lambda rect_num, filled: (mediabox, content_rect, None))
        writer.close()

        pdf_bytes = out_buffer.getvalue()
        logger.info(f"Kết xuất PDF thành công cho tài liệu {result.filename}: {len(pdf_bytes)} bytes")
        return pdf_bytes

    @staticmethod
    def export_to_file(result: DocumentResult, output_path: str) -> str:
        """Xuất tài liệu kết quả ra đường dẫn tệp PDF cụ thể."""
        pdf_bytes = PdfExporter.export_to_bytes(result)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
        return output_path
