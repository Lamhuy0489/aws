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
            # Lưu trữ base64 thuần túy (không kèm tiền tố trùng lặp)
            preview_png_b64 = base64.b64encode(pix.tobytes("png")).decode("utf-8")

            # Đánh giá xem có phải trang scan hay không
            is_scanned = char_count < self.scan_threshold_chars
            # Luôn lưu trữ byte ảnh để sẵn sàng cho Tầng 2 OCR hoặc tải về
            page_image_bytes = pix.tobytes("jpeg")

            tables_count = 0

            # 1. Tìm các bảng biểu thực sự có đường kẻ vector graphics
            # Tuyệt đối không dùng vertical_strategy='text' vì sẽ biến văn bản canh đều thành bảng giả
            table_rects = []
            try:
                tabs = page.find_tables()
                if tabs and tabs.tables:
                    page_rect = page.rect
                    for tab in tabs.tables:
                        extracted = tab.extract()
                        if extracted and len(extracted) >= 2 and len(extracted[0]) >= 2:
                            t_rect = fitz.Rect(tab.bbox)
                            # Bảng hợp lệ không được chiếm trọn toàn bộ trang
                            if t_rect.get_area() < 0.88 * page_rect.get_area():
                                tables_count += 1
                                table_rects.append((t_rect, tab.bbox, extracted))
            except Exception as e:
                logger.debug(f"Lỗi phân tích bảng trên trang {page_num}: {e}")

            # 2. Bóc tách các khối văn bản ngoài bảng theo thứ tự đọc chuẩn (sort=True)
            blocks = page.get_text("blocks", sort=True)
            elements = []
            pending_tables = list(table_rects)

            for b in blocks:
                b_rect = fitz.Rect(b[:4])
                # Kiểm tra xem khối chữ này có nằm trong bảng nào không
                in_table = False
                for tr, bbox, matrix in table_rects:
                    if (tr & b_rect).get_area() > 0.4 * b_rect.get_area():
                        in_table = True
                        break

                if in_table:
                    continue

                # Chèn các bảng xuất hiện trước khối chữ này theo trục dọc y
                to_remove = []
                for item in pending_tables:
                    tr, bbox, matrix = item
                    if tr.y1 <= b_rect.y0 + 5:
                        md_table = self._convert_table_to_markdown(matrix)
                        if md_table:
                            elements.append(md_table)
                        to_remove.append(item)
                for item in to_remove:
                    pending_tables.remove(item)

                block_text = b[4].strip()
                if block_text:
                    formatted_text = self._format_text_block(block_text, b, page_idx)
                    if formatted_text:
                        elements.append(formatted_text)

            # Chèn các bảng còn lại
            for item in pending_tables:
                tr, bbox, matrix = item
                md_table = self._convert_table_to_markdown(matrix)
                if md_table:
                    elements.append(md_table)

            content = "\n\n".join(elements).strip()
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

    def _format_text_block(self, text: str, block_tuple: tuple, page_idx: int = 0) -> str:
        """Tự động phân loại tiêu đề, nhãn giá trị và danh sách để giữ bố cục Markdown chuẩn."""
        cleaned_text = text.strip()
        if not cleaned_text:
            return ""

        # Chuẩn hóa các ký tự bullet điểm từ Word/PDF sang định dạng Markdown
        cleaned_text = re.sub(r"^[\u2022\u25cf\u25aa\u25ab]\s*", "- ", cleaned_text, flags=re.MULTILINE)

        lines = [line.strip() for line in cleaned_text.split("\n") if line.strip()]
        if not lines:
            return ""

        first_line = lines[0]
        y0 = block_tuple[1]

        # 1. Nhận diện Header đầu trang (running header)
        if y0 < 50 and len(lines) <= 2:
            if any(k in first_line.lower() for k in ["conference", "hội nghị", "tạp chí", "journal", "proceedings", "fit_cma", "khoa cntt"]):
                return f"> *{' '.join(lines)}*"

        # 2. Tiêu đề lớn tài liệu hoặc bài báo khoa học (Document Title)
        title_keywords = ["HÓA ĐƠN", "HỢP ĐỒNG", "CỘNG HÒA", "ĐỘC LẬP", "BÁO CÁO", "BIÊN BẢN", "THÔNG BÁO", "CHỨNG NHẬN", "INVOICE", "REPORT"]
        if any(kw in first_line.upper() for kw in title_keywords):
            return f"# {' '.join(lines)}"

        if page_idx == 0 and 60 <= y0 < 110 and len(lines) <= 3:
            if not any(lines[-1].endswith(end) for end in [".", ";", ":"]):
                if len(" ".join(lines)) < 160:
                    return f"# {' '.join(lines)}"

        # 3. Tác giả (Author) trên trang đầu
        if page_idx == 0 and 110 <= y0 <= 160 and len(lines) <= 2:
            if not any(kw in first_line.lower() for kw in ["abstract", "tóm tắt", "keywords", "từ khóa"]):
                if not any(first_line.startswith(p) for p in ["#", "-", "*", "1."]):
                    return f"**Tác giả:** {' '.join(lines)}"

        # 4. Nhận diện các mục đề mục (Section Headings)
        if len(lines) <= 2 and len(first_line) < 100:
            first_lower = first_line.lower()
            if first_lower in ["abstract", "tóm tắt", "references", "tài liệu tham khảo", "acknowledgment", "acknowledgments", "lời cảm ơn", "phụ lục", "appendix"]:
                return f"## {first_line}"
            if first_line.isupper() and len(first_line) < 80 and not first_line.endswith("."):
                return f"## {first_line}"

            # Cấp 2: 1. Introduction, 2. Background
            m_h2 = re.match(r"^([0-9]+)\.\s+([A-ZÀ-Ỹ].+)$", first_line)
            if m_h2:
                return f"## {first_line}"

            # Cấp 3: 2.1. The Role of Attributes
            m_h3 = re.match(r"^([0-9]+\.[0-9]+)\.\s+([A-ZÀ-Ỹ].+)$", first_line)
            if m_h3:
                return f"### {first_line}"

            # Cấp 4: 2.1.1. Sub-section
            m_h4 = re.match(r"^([0-9]+\.[0-9]+\.[0-9]+)\.\s+([A-ZÀ-Ỹ].+)$", first_line)
            if m_h4:
                return f"#### {first_line}"

        # 5. Xử lý chú thích bảng, hình ảnh hoặc Keywords (Keywords: ..., Table 1: ..., Figure 1: ...)
        caption_match = re.match(r"^(Keywords|Từ khóa|Table \d+|Bảng \d+|Figure \d+|Hình \d+)[:.]\s*(.*)$", first_line, re.IGNORECASE)
        if caption_match:
            full_caption = " ".join(lines)
            return f"**{full_caption}**"

        # 6. Xử lý các cặp nhãn Key: Value (ví dụ: Số hóa đơn: INV-001 | Ngày lập: 21/09/2026)
        formatted_lines = []
        is_key_value_block = True
        for line in lines:
            kv_match = re.match(r"^([A-ZÀ-Ỹa-zà-ỹ0-9\s/_-]{2,30}):\s*(.+)$", line)
            if kv_match and not line.startswith("-") and not line.startswith("*"):
                key, val = kv_match.groups()
                formatted_lines.append(f"**{key.strip()}:** {val.strip()}")
            else:
                is_key_value_block = False
                break

        if is_key_value_block and formatted_lines:
            return "\n".join(formatted_lines)

        # 7. Nối dòng mềm cho các đoạn văn bản (Soft-wrap unwrap) và danh sách
        unwrapped = []
        current_para = []

        for line in lines:
            if line.startswith("- ") or line.startswith("* ") or re.match(r"^\d+\.\s+", line):
                if current_para:
                    unwrapped.append(" ".join(current_para))
                    current_para = []
                unwrapped.append(line)
            else:
                if current_para and current_para[-1].endswith("-"):
                    # Nối từ bị ngắt dấu gạch nối cuối dòng (vd: signature-\nspecific -> signature-specific)
                    current_para[-1] = current_para[-1][:-1] + line
                else:
                    current_para.append(line)

        if current_para:
            unwrapped.append(" ".join(current_para))

        return "\n\n".join(unwrapped)

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
