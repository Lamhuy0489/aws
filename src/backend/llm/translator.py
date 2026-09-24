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
        """Dịch nội dung văn bản Markdown sang ngôn ngữ đích với cơ chế xoay vòng Key và dự phòng mô hình."""
        if not markdown_text or not markdown_text.strip():
            return ""

        # Nếu người dùng chọn mô hình AWS Native Bedrock
        if model_name and (model_name.startswith("amazon.") or model_name.startswith("anthropic.") or model_name in ["bedrock-nova", "bedrock-claude"]):
            actual_model = "amazon.nova-micro-v1:0" if "nova" in model_name else "anthropic.claude-3-5-haiku-20241022-v1:0"
            return cls.translate_with_bedrock(markdown_text, target_lang, model_id=actual_model)

        # Thu thập danh sách API Keys có thể sử dụng (từ tham số, settings cấu hình, hoặc Tour Xoay CSDL)
        key_candidates = []
        if api_key and not api_key.startswith("AIzaSy_DEMO") and not api_key.startswith("AIzaSy_TEST"):
            key_candidates.append({
                "id": None,
                "key_value": api_key,
                "key_alias": "Explicit Key",
                "model_name": model_name
            })

        # Lấy từ settings hệ thống nếu có
        try:
            from src.backend.config.settings import get_settings
            settings = get_settings()
            if settings.gemini_api_key and not settings.gemini_api_key.startswith("AIzaSy_DEMO") and not settings.gemini_api_key.startswith("AIzaSy_TEST"):
                if not any(k["key_value"] == settings.gemini_api_key for k in key_candidates):
                    key_candidates.append({
                        "id": None,
                        "key_value": settings.gemini_api_key,
                        "key_alias": "Settings Key",
                        "model_name": settings.gemini_model or "gemini-flash-lite-latest"
                    })
        except Exception:
            pass

        # Lấy tất cả key active thực tế từ CSDL (đã tự động lọc bỏ các key demo)
        try:
            from src.backend.database.db import get_active_keys_by_provider
            db_keys = get_active_keys_by_provider("gemini")
            for k in db_keys:
                if not any(c["key_value"] == k["key_value"] for c in key_candidates):
                    if not k["key_value"].startswith("AIzaSy_DEMO") and not k["key_value"].startswith("AIzaSy_TEST"):
                        key_candidates.append(dict(k))
        except Exception as db_err:
            logger.warning(f"Không thể nạp danh sách key từ CSDL cho dịch thuật: {db_err}")

        if not key_candidates:
            raise RuntimeError("Không tìm thấy Google Gemini API Key hợp lệ nào để thực hiện dịch thuật.")

        pages = [p for p in markdown_text.split("\n\n---\n\n") if p.strip()]
        last_error = None

        # Vòng lặp xoay tour qua từng API Key cho đến khi thành công
        for key_info in key_candidates:
            current_key = key_info["key_value"]
            key_id = key_info.get("id")
            current_model = key_info.get("model_name") or model_name or "gemini-flash-lite-latest"
            if current_model in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]:
                current_model = "gemini-flash-lite-latest"

            try:
                if len(pages) > 1:
                    logger.info(f"Dịch tài liệu {len(pages)} trang qua key '{key_info.get('key_alias', 'N/A')}'...")
                    translated_pages = []
                    for idx, page_content in enumerate(pages):
                        trans_page = cls._translate_single_chunk(page_content, target_lang, current_key, current_model)
                        translated_pages.append(trans_page)
                    
                    if key_id:
                        KeyTourManager.record_usage(key_id)
                    return "\n\n---\n\n".join(translated_pages)
                else:
                    trans_res = cls._translate_single_chunk(markdown_text, target_lang, current_key, current_model)
                    if key_id:
                        KeyTourManager.record_usage(key_id)
                    return trans_res
            except Exception as err:
                err_msg = str(err)
                logger.warning(f"Lỗi khi dịch thuật với key '{key_info.get('key_alias')}': {err_msg}. Đang tự động xoay sang key kế tiếp...")
                last_error = err
                # Nếu lỗi xác thực API Key không hợp lệ (400, 403), tự động tắt key đó trong CSDL
                if key_id and ("400" in err_msg or "403" in err_msg or "API_KEY_INVALID" in err_msg):
                    try:
                        from src.backend.database.db import toggle_api_key_status
                        toggle_api_key_status(key_id)
                        logger.info(f"Đã tự động vô hiệu hóa key lỗi ID {key_id}")
                    except Exception:
                        pass
                continue

        raise RuntimeError(f"Tất cả các API Key dịch thuật đều không phản hồi: {last_error}")

    @classmethod
    def _translate_single_chunk(cls, chunk_text: str, target_lang: str, api_key: str, model_name: str) -> str:
        """Dịch một đoạn văn bản đơn lẻ với danh sách mô hình dự phòng Gemini."""
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

        candidate_models = [
            "gemini-flash-lite-latest",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash-lite",
            "gemini-3.6-flash"
        ]
        if model_name and model_name not in candidate_models and "gemini" in model_name:
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
                response = requests.post(url, json=payload, timeout=30, headers={"Content-Type": "application/json"})
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        translated_text = "".join(p.get("text", "") for p in parts).strip()
                        return translated_text
                elif response.status_code in (400, 403):
                    # Key bị lỗi hoặc hết hạn, ngắt vòng lặp model để chuyển sang key tiếp theo ngay lập tức
                    err_msg = f"HTTP {response.status_code}: {response.text[:150]}"
                    logger.warning(f"Key không hợp lệ hoặc bị từ chối: {err_msg}")
                    raise RuntimeError(err_msg)

                logger.warning(f"Dịch thuật với model {m} trả về status {response.status_code}. Thử model kế tiếp...")
                last_err = RuntimeError(f"HTTP {response.status_code}: {response.text[:100]}")
            except RuntimeError:
                raise
            except Exception as e:
                logger.warning(f"Lỗi khi dịch thuật qua model {m}: {e}. Thử model kế tiếp...")
                last_err = e

        raise RuntimeError(f"Lỗi dịch thuật AI: {str(last_err)}")
