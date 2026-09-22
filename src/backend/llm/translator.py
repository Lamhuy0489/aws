import logging
import requests
from typing import Optional, Dict, List
from src.backend.llm.key_tour_manager import KeyTourManager

logger = logging.getLogger(__name__)

LANG_MAP = {
    "vi": "Tiếng Việt",
    "en": "English",
    "ja": "Tiếng Nhật (Japanese)",
    "ko": "Tiếng Hàn (Korean)",
    "zh": "Tiếng Trung (Chinese)",
    "fr": "Tiếng Pháp (French)",
    "de": "Tiếng Đức (German)"
}

class DocumentTranslator:
    """Module dịch thuật tài liệu chuyên nghiệp đa ngữ sử dụng Gemini AI bảo toàn cấu trúc Markdown."""

    @classmethod
    def translate_with_bedrock(
        cls,
        markdown_text: str,
        target_lang: str = "en",
        model_id: Optional[str] = None
    ) -> str:
        """Dịch nội dung Markdown sử dụng mô hình khép kín Amazon Bedrock (Amazon Nova Micro/Lite hoặc Claude)."""
        if not markdown_text or not markdown_text.strip():
            return ""
        from src.backend.cloud.aws_storage import AWSStorageService
        aws_svc = AWSStorageService()
        target_lang_name = LANG_MAP.get(target_lang.lower(), target_lang)

        system_instruction = (
            f"Bạn là chuyên gia dịch thuật tài liệu kỹ thuật cao cấp trên nền tảng AWS.\n"
            f"Nhiệm vụ: Dịch toàn bộ văn bản sau sang {target_lang_name}.\n"
            f"NGUYÊN TẮC BẮT BUỘC:\n"
            f"1. Bảo toàn 100% cấu trúc Markdown (tiêu đề, danh sách, khối mã, chú thích <!-- Trang X -->, bảng biểu | ... |).\n"
            f"2. Không thay đổi số liệu, thông số kỹ thuật hay mã định danh.\n"
            f"3. Dịch văn phong tự nhiên, chuẩn xác kỹ thuật.\n"
            f"4. Tuyệt đối không thêm emoji, lời dẫn hay giải thích mở đầu/kết thúc. Chỉ trả về nội dung Markdown đã dịch."
        )

        pages = [p for p in markdown_text.split("\n\n---\n\n") if p.strip()]
        if len(pages) > 1:
            translated_pages = []
            for page in pages:
                res = aws_svc.invoke_bedrock_converse(
                    prompt=page,
                    system_instruction=system_instruction,
                    model_id=model_id
                )
                translated_pages.append(res or page)
            return "\n\n---\n\n".join(translated_pages)
        else:
            res = aws_svc.invoke_bedrock_converse(
                prompt=markdown_text,
                system_instruction=system_instruction,
                model_id=model_id
            )
            return res or markdown_text

    @classmethod
    def translate_markdown(cls, markdown_text: str, target_lang: str = "en", api_key: Optional[str] = None, model_name: str = "gemini-flash-lite-latest") -> str:
        """Dịch nội dung văn bản Markdown sang ngôn ngữ đích (tự động chia trang nếu tài liệu lớn để tránh quá tải)."""
        if not markdown_text or not markdown_text.strip():
            return ""

        # Nếu người dùng chọn mô hình AWS Native Bedrock
        if model_name.startswith("amazon.") or model_name.startswith("anthropic.") or model_name in ["bedrock-nova", "bedrock-claude"]:
            actual_model = "amazon.nova-micro-v1:0" if "nova" in model_name else "anthropic.claude-3-5-haiku-20241022-v1:0"
            return cls.translate_with_bedrock(markdown_text, target_lang, model_id=actual_model)

        # Lấy API Key từ Tour Xoay nếu không được truyền vào
        active_key_id = None
        if not api_key:
            picked = KeyTourManager.get_next_key("gemini")
            if picked:
                api_key = picked["key_value"]
                # Ưu tiên gemini-flash-lite-latest
                model_name = picked.get("model_name") or model_name
                if model_name in ["gemini-3.6-flash", "gemini-1.5-flash"]:
                    model_name = "gemini-flash-lite-latest"
                active_key_id = picked["id"]

        if not api_key:
            raise RuntimeError("Không tìm thấy Google Gemini API Key hợp lệ nào để thực hiện dịch thuật.")

        # Kiểm tra nếu tài liệu có nhiều trang phân tách bởi \n\n---\n\n
        pages = [p for p in markdown_text.split("\n\n---\n\n") if p.strip()]
        if len(pages) > 1:
            logger.info(f"Tài liệu gồm {len(pages)} trang, tiến hành dịch từng trang để đảm bảo tốc độ và bảo toàn bố cục...")
            translated_pages = []
            for idx, page_content in enumerate(pages):
                logger.info(f"Đang dịch trang {idx + 1}/{len(pages)} sang {target_lang}...")
                trans_page = cls._translate_single_chunk(page_content, target_lang, api_key, model_name)
                translated_pages.append(trans_page)

            if active_key_id:
                KeyTourManager.record_usage(active_key_id)
            return "\n\n---\n\n".join(translated_pages)
        else:
            # Tài liệu 1 trang
            trans_res = cls._translate_single_chunk(markdown_text, target_lang, api_key, model_name)
            if active_key_id:
                KeyTourManager.record_usage(active_key_id)
            return trans_res

    @classmethod
    def _translate_single_chunk(cls, chunk_text: str, target_lang: str, api_key: str, model_name: str) -> str:
        """Dịch một đoạn văn bản đơn lẻ với cơ chế tự động xoay mô hình dự phòng nếu gặp lỗi."""
        target_lang_name = LANG_MAP.get(target_lang.lower(), target_lang)

        system_instruction = (
            f"Bạn là chuyên gia dịch thuật tài liệu kỹ thuật, khoa học và hành chính cao cấp.\n"
            f"Nhiệm vụ: Dịch toàn bộ văn bản sau đây sang {target_lang_name}.\n\n"
            f"CÁC NGUYÊN TẮC BẮT BUỘC:\n"
            f"1. Bảo toàn 100% cấu trúc cú pháp Markdown: Giữ nguyên các cấp tiêu đề (#, ##, ###), "
            f"các danh sách (- , * ), trích dẫn (> ), các chú thích HTML (<!-- Trang ... -->), và đặc biệt là toàn bộ bảng biểu Markdown (| ... | ... |).\n"
            f"2. Đối với bảng biểu, dịch tiêu đề cột và nội dung văn bản trong từng ô sang {target_lang_name}, "
            f"nhưng tuyệt đối không làm thay đổi số liệu, đơn vị đo, đơn vị tiền tệ hoặc mã số.\n"
            f"3. Dịch thuật lưu loát, tự nhiên, văn phong chuẩn mực chuyên ngành kỹ thuật/khoa học/kinh tế.\n"
            f"4. Tuyệt đối không thêm bất kỳ lời dẫn, lời chào, lời giải thích hay ký tự emoji nào. Chỉ trả về duy nhất nội dung văn bản Markdown đã được dịch."
        )

        candidate_models = ["gemini-flash-lite-latest", "gemini-3.5-flash-lite"]
        if model_name and model_name not in candidate_models:
            candidate_models.insert(0, model_name)

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": system_instruction},
                        {"text": chunk_text}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.95,
                "maxOutputTokens": 4096
            }
        }

        last_err = None
        for m in candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
            try:
                response = requests.post(url, json=payload, timeout=25, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        translated_text = "".join(p.get("text", "") for p in parts).strip()
                        return translated_text
                logger.warning(f"Dịch thuật với model {m} trả về status {response.status_code}. Thử model kế tiếp...")
                last_err = RuntimeError(f"HTTP {response.status_code}: {response.text[:100]}")
            except Exception as e:
                logger.warning(f"Lỗi khi dịch thuật qua model {m}: {e}. Thử model kế tiếp...")
                last_err = e

        raise RuntimeError(f"Lỗi dịch thuật AI: {str(last_err)}")
