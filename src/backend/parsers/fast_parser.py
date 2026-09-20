import logging
import io
import re
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
    preview_png_b64: Optional[str] = None

class FastNativeParser:
    """Tầng 1: Trích xuất nhanh luồng văn bản số và cấu trúc bảng của tài liệu PDF bảo toàn bố cục."""
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
        import base64

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        parsed_pages = []

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            page_num = page_idx + 1
            
            # Trích xuất văn bản thô
            raw_text = page.get_text("text").strip()
            char_count = len(raw_text)

            # Tạo ảnh xem trước độ nét cao cho giao diện (DPI 130)
            pix = page.get_pixmap(dpi=130)
            preview_png_b64 = "data:image/png;base64," + base64.b64encode(pix.tobytes("png")).decode("utf-8")

            # Đánh giá xem có phải trang scan hay không
            is_scanned = char_count < self.scan_threshold_chars
            page_image_bytes = pix.tobytes("jpeg") if is_scanned else None

            tables_count = 0
            markdown_elements = []

            # 1. Tìm các bảng biểu có đường kẻ hoặc cấu trúc cột
            table_rects = []
            table_map = {}
            try:
                # Thử tìm bảng bằng đường kẻ trước
                tabs = page.find_tables()
                if not tabs or not tabs.tables:
                    # Nếu không có đường kẻ, thử tìm bảng theo căn lề cột văn bản
                    tabs = page.find_tables(vertical_strategy="text", horizontal_strategy="text")

                if tabs and tabs.tables:
                    for tab in tabs.tables:
                        extracted = tab.extract()
                        if extracted and len(extracted) >= 2 and len(extracted[0]) >= 2:
                            tables_count += 1
                            t_rect = fitz.Rect(tab.bbox)
                            table_rects.append(t_rect)
                            table_map[tab.bbox] = extracted
            except Exception as e:
                logger.debug(f"Lỗi phân tích bảng trên trang {page_num}: {e}")

            # 2. Bóc tách các khối văn bản ngoài bảng
            blocks = page.get_text("blocks")
            # Sắp xếp các khối văn bản theo thứ tự đọc tự nhiên (y0 tăng dần)
            blocks.sort(key=lambda b: (b[1], b[0]))

            spatial_elements = []

            for b in blocks:
                b_rect = fitz.Rect(b[:4])
                # Kiểm tra xem khối chữ này có nằm trong bảng nào không
                in_table = False
                for tr in table_rects:
                    intersect = tr & b_rect
                    if intersect.get_area() > 0.4 * b_rect.get_area():
                        in_table = True
                        break
                
                if not in_table:
                    block_text = b[4].strip()
                    if block_text:
                        # Tinh chỉnh định dạng khối chữ
                        formatted_text = self._format_text_block(block_text, b)
                        spatial_elements.append((b[1], "text", formatted_text))

            # 3. Thêm các bảng vào danh sách không gian
            for bbox, matrix in table_map.items():
                md_table = self._convert_table_to_markdown(matrix)
                if md_table:
                    spatial_elements.append((bbox[1], "table", md_table))

            # 4. Sắp xếp toàn bộ các phần tử (Tiêu đề, Text, Bảng biểu) theo tọa độ y0 dọc
            spatial_elements.sort(key=lambda item: item[0])

            content_lines = [item[2] for item in spatial_elements]
            content = "\n\n".join(content_lines).strip()

            if not content and raw_text:
                content = raw_text

            parsed_pages.append(ParsedPage(
                page_number=page_num,
                is_scanned=is_scanned,
                markdown_content=content,
                character_count=char_count,
                tables_count=tables_count,
                image_bytes=page_image_bytes,
                preview_png_b64=preview_png_b64
            ))

        doc.close()
        return parsed_pages

    def _format_text_block(self, text: str, block_tuple: tuple) -> str:
        """Tự động phân loại tiêu đề, nhãn giá trị và danh sách để giữ bố cục Markdown chuẩn."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            return ""

        first_line = lines[0]
        # Tiêu đề lớn của tài liệu: Tự động căn giữa
        title_keywords = ["HÓA ĐƠN", "HỢP ĐỒNG", "CỘNG HÒA", "ĐỘC LẬP", "BÁO CÁO", "BIÊN BẢN", "THÔNG BÁO", "CHỨNG NHẬN"]
        if len(lines) == 1:
            if any(kw in first_line.upper() for kw in title_keywords):
                return f"# {first_line}"
            elif first_line.isupper() and len(first_line) < 100:
                return f"## {first_line}"
            elif first_line.endswith(":") and len(first_line) < 80:
                return f"### {first_line}"

        # Xử lý các cặp nhãn Key: Value (ví dụ: Số hóa đơn: INV-001 | Ngày: 21/09/2026)
        formatted_lines = []
        for line in lines:
            if any(kw in line.upper() for kw in title_keywords):
                formatted_lines.append(f"# {line}")
                continue

            match = re.match(r"^([A-ZÀ-Ỹa-zà-ỹ0-9\s/_-]{2,30}):\s*(.+)$", line)
            if match and not line.startswith("-"):
                key, val = match.groups()
                formatted_lines.append(f"**{key.strip()}:** {val.strip()}")
            elif line.startswith("-") or line.startswith("*"):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)

        return "\n".join(formatted_lines)

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
                image_bytes=None,
                preview_png_b64=None
            ))

        return parsed_pages

    @staticmethod
    def _convert_table_to_markdown(matrix: List[List[Any]]) -> str:
        """Chuyển đổi ma trận hàng/cột thành bảng Markdown chuẩn có căn lề cột thông minh."""
        if not matrix or len(matrix) < 1:
            return ""

        cleaned_rows = []
        for row in matrix:
            cleaned_rows.append([str(cell).replace("\n", " ").strip() if cell is not None else "" for cell in row])

        cleaned_rows = [r for r in cleaned_rows if any(cell for cell in r)]
        if not cleaned_rows:
            return ""

        headers = cleaned_rows[0]
        if not any(headers):
            headers = [f"Cột {i+1}" for i in range(len(headers))]

        # Tự động căn lề thông minh theo loại dữ liệu cột
        separators = []
        for h in headers:
            h_lower = str(h).lower()
            if any(k in h_lower for k in ["stt", "no", "id", "thứ tự", "index"]):
                separators.append(":---:")  # Căn giữa cho cột STT / Mã
            elif any(k in h_lower for k in ["giá", "tiền", "phí", "tổng", "vat", "thuế", "price", "amount", "total"]):
                separators.append("---:")   # Căn phải cho số tiền / giá cả
            elif any(k in h_lower for k in ["số lượng", "qty", "quantity", "đơn vị", "đvt"]):
                separators.append(":---:")  # Căn giữa cho số lượng
            else:
                separators.append(":---")   # Căn trái cho tên hàng hóa, diễn giải

        header_line = "| " + " | ".join(headers) + " |"
        separator_line = "| " + " | ".join(separators) + " |"

        body_lines = []
        for row in cleaned_rows[1:]:
            padded_row = row + [""] * (len(headers) - len(row))
            body_lines.append("| " + " | ".join(padded_row[:len(headers)]) + " |")

        return "\n" + "\n".join([header_line, separator_line] + body_lines) + "\n"
