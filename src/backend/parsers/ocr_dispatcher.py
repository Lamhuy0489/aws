import base64
import json
import logging
import requests
from typing import Optional
from src.backend.config.settings import AppSettings

logger = logging.getLogger(__name__)

SYSTEM_OCR_PROMPT = (
    "Bạn là một hệ thống nhận diện và bóc tách tài liệu (OCR) chính xác tuyệt đối. "
    "Nhiệm vụ của bạn là đọc và trích xuất TOÀN BỘ nội dung văn bản có trong tài liệu/hình ảnh này sang định dạng Markdown chuẩn.\n"
    "Yêu cầu:\n"
    "1. CHỈ in ra duy nhất nội dung văn bản thực tế có trong tài liệu (tiêu đề, các đoạn văn bản, bảng biểu dữ liệu, danh sách, công thức).\n"
    "2. Giữ nguyên 100% cấu trúc bảng biểu Markdown (| Cột 1 | Cột 2 |) và chính tả tiếng Việt có dấu chuẩn xác.\n"
    "3. Tuyệt đối KHÔNG in ra lời chào, lời dẫn, ghi chú, giải thích, thông số kỹ thuật, metadata hoặc bảng đối soát hệ thống. Chỉ in duy nhất nội dung tài liệu."
)

class OCRDispatcher:
    """Tầng 2: Điều phối gọi mô hình Vision OCR ngoại vi (AWS Bedrock, Kaggle GPU/TPU hoặc Gemini Failover)."""
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.last_engine_used = ""

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

        # Xu ly che do AWS Native Foundation Models (Amazon Bedrock)
        if self.settings.ocr_mode == "AWS_NATIVE":
            try:
                logger.info(f"Đang gửi yêu cầu Vision OCR tới AWS Bedrock ({self.settings.aws_bedrock_model})...")
                bedrock_md = self._call_aws_bedrock_vision(image_bytes)
                if bedrock_md:
                    self.last_engine_used = "aws_bedrock"
                    return bedrock_md
            except Exception as e:
                logger.warning(f"AWS Bedrock chưa khả dụng ({e}). Kích hoạt chuyển đổi dự phòng sang Gemini Vision để bóc tách nội dung thật...")
            
            # Tự động nạp Gemini Key từ Tour nếu chưa có
            if not self.settings.gemini_api_key:
                try:
                    from src.backend.llm.key_tour_manager import KeyTourManager
                    picked_g = KeyTourManager.get_next_key("gemini")
                    if picked_g:
                        self.settings.gemini_api_key = picked_g["key_value"]
                        self.settings.gemini_model = picked_g.get("model_name") or "gemini-flash-lite-latest"
                except Exception as tour_err:
                    logger.warning(f"Không thể nạp Gemini Key dự phòng: {tour_err}")

            if self.settings.gemini_api_key:
                self.last_engine_used = "gemini_failover"
                return self._call_gemini_vision_with_failover(image_bytes)

            raise RuntimeError("AWS Bedrock không phản hồi và không tìm thấy khóa Gemini dự phòng hợp lệ.")

        kaggle_err = None
        # Thử gọi Kaggle Endpoint nếu ở chế độ HYBRID_KAGGLE
        if self.settings.ocr_mode == "HYBRID_KAGGLE" and self.settings.kaggle_endpoint:
            try:
                logger.info(f"Đang gửi ảnh sang Kaggle OCR Endpoint: {self.settings.kaggle_endpoint} (Timeout: {self.settings.timeout_seconds}s)")
                markdown_result = self._call_kaggle_endpoint(image_bytes)
                if markdown_result:
                    return markdown_result
            except Exception as e:
                kaggle_err = str(e)
                logger.warning(f"Lỗi khi gọi Kaggle OCR Endpoint ({kaggle_err}). Đang kích hoạt chuyển đổi dự phòng sang Gemini...")

        # Tự động nạp Gemini API Key từ Tour Xoay nếu chưa có
        if not self.settings.gemini_api_key:
            try:
                from src.backend.llm.key_tour_manager import KeyTourManager
                picked_g = KeyTourManager.get_next_key("gemini")
                if picked_g:
                    self.settings.gemini_api_key = picked_g["key_value"]
                    self.settings.gemini_model = picked_g.get("model_name") or "gemini-flash-lite-latest"
                    logger.info(f"Đã tự động nạp Gemini Key '{picked_g['key_alias']}' cho cơ chế dự phòng Tầng 2 OCR.")
            except Exception as tour_err:
                logger.warning(f"Không thể nạp Gemini Key dự phòng: {tour_err}")

        # Kích hoạt Standalone Fallback qua Gemini Flash API nếu có cấu hình
        if self.settings.gemini_api_key:
            return self._call_gemini_vision_with_failover(image_bytes)

        if kaggle_err:
            raise RuntimeError(f"Máy chủ Kaggle OCR phản hồi quá thời gian cho phép hoặc gặp lỗi mạng: {kaggle_err}")

        raise RuntimeError("Không có endpoint Kaggle hoặc API Key Gemini hợp lệ nào được cấu hình cho Tầng 2 OCR.")

    def _call_kaggle_endpoint(self, image_bytes: bytes) -> str:
        """Gửi ảnh đến máy chủ FastAPI đang chạy trên Kaggle qua Cloudflare Tunnel."""
        # Tự động chuẩn hóa kích thước ảnh về tối đa 1280px để tối ưu token thị giác và tăng tốc GPU
        try:
            import io
            from PIL import Image
            pil_img = Image.open(io.BytesIO(image_bytes))
            w, h = pil_img.size
            max_dim = 1280
            if max(w, h) > max_dim:
                scale = max_dim / max(w, h)
                new_w, new_h = int(w * scale), int(h * scale)
                pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                pil_img.convert("RGB").save(buf, format="JPEG", quality=85)
                image_bytes = buf.getvalue()
                logger.info(f"Đã chuẩn hóa ảnh từ ({w}x{h}) về ({new_w}x{new_h}) để tối ưu VRAM GPU Kaggle.")
        except Exception as resize_err:
            logger.warning(f"Không thể chuẩn hóa kích thước ảnh: {resize_err}")

        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "image_base64": b64_image,
            "prompt": SYSTEM_OCR_PROMPT
        }
        
        endpoint = self.settings.kaggle_endpoint
        if not endpoint.endswith("/ocr"):
            endpoint = endpoint.rstrip("/") + "/ocr"

        # Giới hạn thời gian chờ tối đa 5 giây; nếu không phản hồi thì tự động Failover tức thì sang Gemini
        kaggle_timeout = min(self.settings.timeout_seconds, 5)
        response = requests.post(
            endpoint,
            json=payload,
            timeout=kaggle_timeout,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("markdown", data.get("text", "")).strip()

    def _call_gemini_vision_with_failover(self, image_bytes: bytes) -> str:
        """
        Gửi ảnh đến Gemini Vision REST API với cơ chế Tour Xoay Key đa tầng:
        - Xoay vòng qua tất cả các API Key Gemini đang hoạt động trong CSDL.
        - Với mỗi Key, tự động thử qua các phiên bản mô hình tối ưu.
        - Nếu 1 key bị lỗi (400 Invalid, 403, 429 Quota), tự động loại trừ và xoay sang Key kế tiếp.
        """
        from src.backend.database.db import get_active_keys_by_provider, toggle_api_key_status
        from src.backend.llm.key_tour_manager import KeyTourManager

        b64_image = base64.b64encode(image_bytes).decode("utf-8")

        # Thu thập danh sách API Keys có thể sử dụng cho tour xoay
        key_candidates = []
        if self.settings.gemini_api_key and not self.settings.gemini_api_key.startswith("AIzaSy_"):
            key_candidates.append({
                "id": None,
                "key_value": self.settings.gemini_api_key,
                "key_alias": "Configured Key",
                "model_name": self.settings.gemini_model or "gemini-flash-lite-latest"
            })

        # Nạp thêm tất cả các key active từ CSDL
        try:
            db_keys = get_active_keys_by_provider("gemini")
            for k in db_keys:
                if not any(c["key_value"] == k["key_value"] for c in key_candidates):
                    # Bỏ qua các key demo giả lập
                    if not k["key_value"].startswith("AIzaSy_DEMO") and not k["key_value"].startswith("AIzaSy_TEST"):
                        key_candidates.append(dict(k))
        except Exception as db_err:
            logger.warning(f"Không thể nạp danh sách key từ CSDL: {db_err}")

        if not key_candidates:
            raise RuntimeError("Không có API Key Gemini nào đang hoạt động trong hệ thống xoay tour.")

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

        last_err_msg = ""
        per_try_timeout = min(self.settings.timeout_seconds, 15)

        for key_info in key_candidates:
            api_key = key_info["key_value"]
            key_alias = key_info.get("key_alias", "Gemini Key")
            key_id = key_info.get("id")

            # Xác định các model candidate cho key này (dùng các model v1beta đang hoạt động)
            pref_model = key_info.get("model_name") or self.settings.gemini_model or "gemini-flash-lite-latest"
            if "1.5" in pref_model:
                pref_model = "gemini-flash-lite-latest"
            models_to_try = [pref_model]
            for m in ["gemini-flash-lite-latest", "gemini-2.5-flash", "gemini-2.0-flash"]:
                if m not in models_to_try:
                    models_to_try.append(m)

            for model in models_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                try:
                    logger.info(f"Tour Xoay: Đang gọi Gemini ({model}) bằng key '{key_alias}'...")
                    response = requests.post(
                        url,
                        json=payload,
                        timeout=per_try_timeout,
                        headers={"Content-Type": "application/json"}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts:
                                extracted_text = parts[0].get("text", "").strip()
                                if key_id:
                                    KeyTourManager.record_usage(key_id)
                                logger.info(f"Tour Xoay: Bóc tách OCR thành công bằng key '{key_alias}' ({model}).")
                                return extracted_text
                        return ""

                    status_code = response.status_code
                    last_err_msg = f"Key '{key_alias}' - Model {model} phản hồi HTTP {status_code}: {response.text[:100]}"
                    logger.warning(last_err_msg)

                    # Nếu lỗi 400 API_KEY_INVALID, tự động vô hiệu hóa key hỏng khỏi tour xoay
                    if status_code == 400 and ("API_KEY_INVALID" in response.text or "key not valid" in response.text.lower()):
                        if key_id:
                            toggle_api_key_status(key_id)
                            logger.warning(f"Đã tự động loại bỏ key không hợp lệ khỏi tour: '{key_alias}' ({key_id})")
                        break

                    # Nếu lỗi 429 hoặc 403, chuyển sang key tiếp theo trong tour
                    if status_code in [429, 403]:
                        logger.info(f"Key '{key_alias}' quá tải/hết quota (HTTP {status_code}). Đang xoay tour sang key tiếp theo...")
                        break

                except requests.exceptions.Timeout:
                    last_err_msg = f"Key '{key_alias}' - Timeout sau {per_try_timeout}s"
                    logger.warning(last_err_msg)
                except Exception as e:
                    last_err_msg = f"Key '{key_alias}' - Lỗi kết nối: {e}"
                    logger.warning(last_err_msg)

        raise RuntimeError(f"Tất cả các API Key trong Tour Xoay đều gặp sự cố. Chi tiết lỗi cuối: {last_err_msg}")

    def _call_aws_bedrock_vision(self, image_bytes: bytes) -> str:
        """Gửi ảnh đến AWS Bedrock sử dụng Converse API với mô hình đa phương thức."""
        from src.backend.cloud.aws_storage import AWSStorageService
        aws_svc = AWSStorageService(settings=self.settings)
        if not aws_svc.is_connected:
            raise RuntimeError("Chưa kết nối hoặc cấu hình AWS SDK Boto3 không hợp lệ.")

        target_model = self.settings.aws_bedrock_model
        if "nova-micro" in target_model.lower():
            target_model = "amazon.nova-lite-v1:0"

        # Chuẩn hóa ảnh sang JPEG nếu cần
        try:
            import io
            from PIL import Image
            pil_img = Image.open(io.BytesIO(image_bytes))
            w, h = pil_img.size
            max_dim = 1568
            if max(w, h) > max_dim:
                scale = max_dim / max(w, h)
                pil_img = pil_img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            pil_img.convert("RGB").save(buf, format="JPEG", quality=85)
            image_bytes = buf.getvalue()
        except Exception as resize_err:
            logger.warning(f"Không thể xử lý kích thước ảnh Bedrock: {resize_err}")

        res = aws_svc.invoke_bedrock_converse(
            prompt=SYSTEM_OCR_PROMPT,
            system_instruction="Bạn là chuyên gia OCR tài liệu chuẩn xác cao trên AWS.",
            model_id=target_model,
            image_bytes=image_bytes,
            image_format="jpeg"
        )
        if not res:
            raise RuntimeError(f"AWS Bedrock không trả về kết quả hoặc bị từ chối quyền truy cập ({target_model}).")
        return res.strip()


