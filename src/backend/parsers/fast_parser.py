import logging
import io
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ParsedPage(BaseModel):
    page_number: int
    is_scanned: bool
    markdown_content: str
    character_count: int
    tables_count: int = 0
    image_bytes: Optional[bytes] = None

class FastNativeParser:
    """Tầng 1: Trích xuất nhanh luồng văn bản số và cấu trúc bảng của tài liệu PDF."""
    def __init__(self, scan_threshold_chars: int = 50):
        self.scan_threshold_chars = scan_threshold_chars

    def parse_pdf(self, pdf_bytes: bytes) -> List[ParsedPage]:
        """Duyệt qua các trang PDF và bóc tách cấu trúc bằng PyMuPDF hoặc pypdf."""
        try:
            import fitz  # PyMuPDF
            return self._parse_with_pymupdf(pdf_bytes)
        except ImportError:
            logger.warning("Không tìm thấy thư viện PyMuPDF (fitz), chuyển sang dùng pypdf làm dự phòng.")
            return self._parse_with_pypdf(pdf_bytes)

    def _parse_with_pymupdf(self, pdf_bytes: bytes) -> List[ParsedPage]:
        import fitz
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        parsed_pages = []

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            page_num = page_idx + 1
            
            # Trích xuất văn bản thuần
            raw_text = page.get_text("text").strip()
            char_count = len(raw_text)

            # Đánh giá xem có phải trang scan hay không
            is_scanned = char_count < self.scan_threshold_chars

            # Trích xuất ảnh trang nếu là trang scan để phục vụ Tầng 2
            page_image_bytes = None
            if is_scanned:
                pix = page.get_pixmap(dpi=150)
                page_image_bytes = pix.tobytes("jpeg")

            # Xử lý cấu trúc văn bản và bảng biểu
            tables_count = 0
            markdown_lines = []

            # Thử tìm bảng biểu qua PyMuPDF (find_tables) nếu có
            table_bboxes = []
            try:
                tables = page.find_tables()
                if tables and tables.tables:
                    for tab in tables.tables:
                        tables_count += 1
                        table_bboxes.append(tab.bbox)
                        md_table = self._convert_table_to_markdown(tab.extract())
                        if md_table:
                            markdown_lines.append(md_table)
            except Exception as e:
                logger.debug(f"Không thể trích xuất bảng tự động trên trang {page_num}: {e}")

            # Nếu không tìm thấy bảng tự động nhưng có văn bản
            if not table_bboxes and raw_text:
                blocks = page.get_text("blocks")
                # Sắp xếp các khối văn bản theo thứ tự đọc (y0 tăng dần, x0 tăng dần)
                blocks.sort(key=lambda b: (b[1], b[0]))
                
                for b in blocks:
                    block_text = b[4].strip()
                    if not block_text:
                        continue
                    
                    # Phát hiện tiêu đề dựa trên độ dài hoặc viết hoa
                    if len(block_text) < 80 and ("\n" not in block_text) and (block_text.isupper() or block_text.endswith(":")):
                        markdown_lines.append(f"\n## {block_text}\n")
                    else:
                        markdown_lines.append(block_text)
            elif not markdown_lines and raw_text:
                markdown_lines.append(raw_text)

            content = "\n\n".join(markdown_lines).strip()

            parsed_pages.append(ParsedPage(
                page_number=page_num,
                is_scanned=is_scanned,
                markdown_content=content,
                character_count=char_count,
                tables_count=tables_count,
                image_bytes=page_image_bytes
            ))

        doc.close()
        return parsed_pages

    def _parse_with_pypdf(self, pdf_bytes: bytes) -> List[ParsedPage]:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        parsed_pages = []

        for page_idx, page in enumerate(reader.pages):
            page_num = page_idx + 1
            raw_text = page.extract_text() or ""
            raw_text = raw_text.strip()
            char_count = len(raw_text)
            is_scanned = char_count < self.scan_threshold_chars

            parsed_pages.append(ParsedPage(
                page_number=page_num,
                is_scanned=is_scanned,
                markdown_content=raw_text,
                character_count=char_count,
                tables_count=0,
                image_bytes=None
            ))

        return parsed_pages

    @staticmethod
    def _convert_table_to_markdown(matrix: List[List[Any]]) -> str:
        """Chuyển đổi ma trận hàng/cột thành bảng Markdown chuẩn."""
        if not matrix or len(matrix) < 1:
            return ""

        cleaned_rows = []
        for row in matrix:
            cleaned_rows.append([str(cell).replace("\n", " ").strip() if cell is not None else "" for cell in row])

        # Loại bỏ các hàng hoàn toàn rỗng
        cleaned_rows = [r for r in cleaned_rows if any(cell for cell in r)]
        if not cleaned_rows:
            return ""

        headers = cleaned_rows[0]
        header_line = "| " + " | ".join(headers) + " |"
        separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"

        body_lines = []
        for row in cleaned_rows[1:]:
            # Đảm bảo số cột khớp nhau
            padded_row = row + [""] * (len(headers) - len(row))
            body_lines.append("| " + " | ".join(padded_row[:len(headers)]) + " |")

        return "\n" + "\n".join([header_line, separator_line] + body_lines) + "\n"
