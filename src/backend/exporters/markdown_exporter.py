import os
import logging
from src.backend.parsers.hybrid_engine import DocumentResult

logger = logging.getLogger(__name__)

class MarkdownExporter:
    """Xuất kết quả bóc tách ra tệp Markdown (.md) chuẩn."""
    @staticmethod
    def export_to_string(result: DocumentResult) -> str:
        """Trả về nội dung Markdown kèm theo thông tin tổng quan ở đầu trang."""
        header = (
            f"# Báo Cáo Bóc Tách Tài Liệu: {result.filename}\n\n"
            f"- **Mã tài liệu**: `{result.document_id}`\n"
            f"- **Tổng số trang**: {result.total_pages} (Văn bản số: {result.digital_pages_count}, Ảnh scan: {result.scanned_pages_count})\n"
            f"- **Thời gian xử lý**: {result.processing_time_seconds} giây\n\n"
            f"---\n\n"
        )
        return header + result.full_markdown

    @staticmethod
    def export_to_file(result: DocumentResult, output_path: str) -> str:
        content = MarkdownExporter.export_to_string(result)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Đã xuất tệp Markdown tại: {output_path}")
        return output_path
