import logging
from typing import Optional, Dict
from src.backend.database.db import get_active_keys_by_provider, increment_api_key_usage

logger = logging.getLogger(__name__)

class KeyTourManager:
    """Quản lý và điều phối danh sách API Keys theo cơ chế xoay vòng (Tour Rotation)."""
    
    @staticmethod
    def get_next_key(provider: str) -> Optional[Dict]:
        """
        Lấy API Key tiếp theo theo nguyên tắc xoay tour:
        Ưu tiên key đang hoạt động (is_active = 1) và có số lượt gọi (usage_count) thấp nhất.
        """
        active_keys = get_active_keys_by_provider(provider)
        if not active_keys:
            logger.warning(f"Không tìm thấy API Key nào đang hoạt động cho nhà cung cấp: {provider}")
            return None

        # Chọn key có lượt sử dụng ít nhất
        selected_key = active_keys[0]
        logger.info(f"Xoay tour: Chọn key '{selected_key['key_alias']}' (Lượt dùng hiện tại: {selected_key['usage_count']})")
        return selected_key

    @staticmethod
    def record_usage(key_id: str):
        """Ghi nhận lượt gọi thành công của key."""
        try:
            increment_api_key_usage(key_id)
        except Exception as e:
            logger.error(f"Lỗi khi cập nhật usage count cho key {key_id}: {e}")
