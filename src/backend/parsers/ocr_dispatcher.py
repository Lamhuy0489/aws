import base64
import json
import logging
import requests
from typing import Optional
from src.backend.config.settings import AppSettings

logger = logging.getLogger(__name__)

SYSTEM_OCR_PROMPT = (
    "Bạn là chuyên gia OCR tài liệu cao cấp. Hãy chuyển đổi hình ảnh tài liệu này "
    "thành định dạng Markdown chuẩn xác. Yêu cầu bắt buộc:\n"
    "1. Giữ nguyên 100% toàn bộ bảng biểu số liệu bằng định dạng Markdown Table (| Cột 1 | Cột 2 |).\n"
    "2. Giữ nguyên các cấp tiêu đề (#, ##, ###), danh sách liệt kê, và thứ tự đọc của văn bản nhiều cột.\n"
    "3. Bảo toàn chính xác toàn bộ chữ tiếng Việt có dấu và các ký tự đặc biệt.\n"
    "4. Tuyệt đối không thêm lời giải thích, lời chào hay bình luận; chỉ xuất duy nhất nội dung Markdown của tài liệu."
)

class OCRDispatcher:
    """Tầng 2: Điều phối gọi mô hình Vision OCR ngoại vi (Kaggle GPU/TPU hoặc Gemini Fallback)."""
    def __init__(self, settings: AppSettings):
        self.settings = settings

    def ocr_image(self, image_bytes: bytes) -> str:
        """Thực hiện OCR cho ảnh trang scan, tự động kích hoạt failover nếu gặp lỗi."""
        if not image_bytes:
            return ""

        # Kiểm thử cục bộ không cần mạng (LOCAL_MOCK)
        if self.settings.ocr_mode == "LOCAL_MOCK":
            logger.info("Đang xử lý ở chế độ LOCAL_MOCK: Trả về kết quả OCR mẫu...")
            return (
                "## THÔNG TIN HÓA ĐƠN DỊCH VỤ (MẪU OCR SCAN)\n\n"
                "| Mã Dịch Vụ | Tên Dịch Vụ / Hàng Hóa | Số Lượng | Đơn Giá (VNĐ) | Thành Tiền (VNĐ) |\n"
                "| :--- | :--- | :--- | :--- | :--- |\n"
                "| AWS-EC2-01 | Máy Chủ Ảo Amazon EC2 t3.medium | 2 | 750,000 | 1,500,000 |\n"
                "| AWS-S3-02 | Lưu Trữ Amazon S3 Standard (GB) | 100 | 1,200 | 120,000 |\n"
                "| AWS-DDB-03 | Cơ Sở Dữ Liệu DynamoDB On-Demand | 1 | 250,000 | 250,000 |\n\n"
                "**Tổng tiền trước thuế**: 1,870,000 VNĐ\n"
                "**Thuế GTGT (10%)**: 187,000 VNĐ\n"
                "**Tổng giá trị thanh toán**: 2,057,000 VNĐ"
            )

        # Thử gọi Kaggle Endpoint nếu ở chế độ HYBRID_KAGGLE
        if self.settings.ocr_mode == "HYBRID_KAGGLE" and self.settings.kaggle_endpoint:
            try:
                logger.info(f"Đang gửi ảnh sang Kaggle OCR Endpoint: {self.settings.kaggle_endpoint}")
                markdown_result = self._call_kaggle_endpoint(image_bytes)
                if markdown_result:
                    return markdown_result
            except Exception as e:
                logger.warning(f"Lỗi khi gọi Kaggle OCR Endpoint ({str(e)}). Đang kích hoạt chuyển đổi dự phòng sang Gemini...")

        # Kích hoạt Standalone Fallback qua Gemini Flash API
        if self.settings.gemini_api_key:
            try:
                logger.info("Đang gọi Google Gemini 1.5 Flash Vision API làm dự phòng...")
                return self._call_gemini_vision(image_bytes)
            except Exception as e:
                logger.error(f"Lỗi khi gọi Gemini Vision API: {str(e)}")
                raise RuntimeError(f"Tất cả các dịch vụ OCR ngoại vi đều thất bại: {str(e)}")

        raise RuntimeError("Không có endpoint Kaggle hoặc API Key Gemini hợp lệ nào được cấu hình cho Tầng 2 OCR.")

    def _call_kaggle_endpoint(self, image_bytes: bytes) -> str:
        """Gửi ảnh đến máy chủ FastAPI đang chạy trên Kaggle qua Cloudflare Tunnel."""
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "image_base64": b64_image,
            "prompt": SYSTEM_OCR_PROMPT
        }
        
        endpoint = self.settings.kaggle_endpoint
        if not endpoint.endswith("/ocr"):
            endpoint = endpoint.rstrip("/") + "/ocr"

        response = requests.post(
            endpoint,
            json=payload,
            timeout=self.settings.timeout_seconds,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("markdown", data.get("text", "")).strip()

    def _call_gemini_vision(self, image_bytes: bytes) -> str:
        """Gửi ảnh trực tiếp đến Gemini 1.5 Flash REST API mà không cần cài đặt thư viện nặng."""
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.settings.gemini_model}:generateContent?key={self.settings.gemini_api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": SYSTEM_OCR_PROMPT},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": b64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 4096
            }
        }

        response = requests.post(
            url,
            json=payload,
            timeout=self.settings.timeout_seconds,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        
        try:
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
        except Exception as e:
            logger.error(f"Lỗi khi bóc tách phản hồi JSON từ Gemini: {e}")

        return ""
