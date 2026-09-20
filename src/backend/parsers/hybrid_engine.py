import time
import logging
from typing import List, Optional
from pydantic import BaseModel
from src.backend.config.settings import AppSettings
from src.backend.parsers.fast_parser import FastNativeParser, ParsedPage
from src.backend.parsers.ocr_dispatcher import OCRDispatcher

logger = logging.getLogger(__name__)

class DocumentResult(BaseModel):
    document_id: str
    filename: str
    total_pages: int
    digital_pages_count: int
    scanned_pages_count: int
    full_markdown: str
    processing_time_seconds: float
    pages: List[ParsedPage]
    page_images: List[str] = []

class HybridDocumentEngine:
    """Bộ điều phối hợp nhất xử lý tài liệu đa tầng (Fast-Path kết hợp Selective Vision OCR)."""
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.fast_parser = FastNativeParser(scan_threshold_chars=settings.scan_threshold_chars)
        self.ocr_dispatcher = OCRDispatcher(settings=settings)

    def process_document(self, file_bytes: bytes, filename: str, document_id: str = "") -> DocumentResult:
        """Xử lý tệp tài liệu PDF hoặc tệp hình ảnh đơn lẻ."""
        start_time = time.time()
        is_pdf = filename.lower().endswith(".pdf")
        
        if is_pdf:
            result = self._process_pdf(file_bytes, filename, document_id)
        else:
            result = self._process_single_image(file_bytes, filename, document_id)

        result.processing_time_seconds = round(time.time() - start_time, 2)
        logger.info(
            f"Hoàn thành xử lý {filename}: {result.total_pages} trang "
            f"({result.digital_pages_count} số, {result.scanned_pages_count} scan) "
            f"trong {result.processing_time_seconds}s"
        )
        return result

    def _process_pdf(self, pdf_bytes: bytes, filename: str, document_id: str) -> DocumentResult:
        pages = self.fast_parser.parse_pdf(pdf_bytes)
        digital_count = 0
        scanned_count = 0
        assembled_markdown = []

        for page in pages:
            if not page.is_scanned:
                # Tầng 1: Sử dụng kết quả bóc tách trực tiếp (Fast-Path)
                digital_count += 1
                page_header = f"<!-- Trang {page.page_number} (Văn bản số) -->\n\n"
                assembled_markdown.append(page_header + page.markdown_content)
            else:
                # Tầng 2: Kích hoạt mô hình Vision OCR cho trang scan (Slow-Path)
                scanned_count += 1
                logger.info(f"Phát hiện trang {page.page_number} là trang scan. Kích hoạt Tầng 2...")
                
                ocr_text = ""
                if page.image_bytes:
                    try:
                        ocr_text = self.ocr_dispatcher.ocr_image(page.image_bytes)
                        page.markdown_content = ocr_text
                    except Exception as e:
                        logger.error(f"Lỗi khi OCR trang {page.page_number}: {e}")
                        ocr_text = f"[Lỗi OCR trên trang {page.page_number}: {str(e)}]"
                
                page_header = f"<!-- Trang {page.page_number} (Ảnh scan - OCR) -->\n\n"
                assembled_markdown.append(page_header + (ocr_text or page.markdown_content))

        full_md = "\n\n---\n\n".join(assembled_markdown)
        page_images = [p.preview_png_b64 for p in pages if p.preview_png_b64]

        return DocumentResult(
            document_id=document_id or filename,
            filename=filename,
            total_pages=len(pages),
            digital_pages_count=digital_count,
            scanned_pages_count=scanned_count,
            full_markdown=full_md,
            processing_time_seconds=0.0,
            pages=pages,
            page_images=page_images
        )

    def _process_single_image(self, image_bytes: bytes, filename: str, document_id: str) -> DocumentResult:
        import base64
        logger.info(f"Xử lý tệp hình ảnh đơn lẻ: {filename} thông qua Tầng 2 OCR...")
        ocr_text = self.ocr_dispatcher.ocr_image(image_bytes)
        
        b64_img = "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode("utf-8")
        page = ParsedPage(
            page_number=1,
            is_scanned=True,
            markdown_content=ocr_text,
            character_count=len(ocr_text),
            tables_count=1 if "|" in ocr_text else 0,
            image_bytes=image_bytes,
            preview_png_b64=b64_img
        )

        return DocumentResult(
            document_id=document_id or filename,
            filename=filename,
            total_pages=1,
            digital_pages_count=0,
            scanned_pages_count=1,
            full_markdown=ocr_text,
            processing_time_seconds=0.0,
            pages=[page],
            page_images=[b64_img]
        )
