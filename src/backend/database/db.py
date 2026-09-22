import sqlite3
import os
import uuid
import logging
from typing import Optional, List, Dict, Any
from werkzeug.security import generate_password_hash

logger = logging.getLogger(__name__)

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
DB_PATH = os.path.join(DB_DIR, "app.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_db_connection() -> sqlite3.Connection:
    """Tạo kết nối tới SQLite CSDL và bật chế độ trả về Dictionary Row."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Khởi tạo cấu trúc bảng và nạp dữ liệu mẫu ban đầu."""
    conn = get_db_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    # Khởi tạo tài khoản quản trị viên và người dùng mẫu nếu chưa tồn tại
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()["count"]

    if user_count == 0:
        logger.info("Khởi tạo tài khoản mẫu ban đầu: admin và demo...")
        admin_id = str(uuid.uuid4())[:8]
        demo_id = str(uuid.uuid4())[:8]

        cursor.execute(
            "INSERT INTO users (id, username, email, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            (admin_id, "admin", "admin@cloudjourney.vn", generate_password_hash("Admin@123"), "admin")
        )
        cursor.execute(
            "INSERT INTO users (id, username, email, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            (demo_id, "demo", "demo@cloudjourney.vn", generate_password_hash("Demo@123"), "user")
        )

    # Khởi tạo danh sách API Keys mẫu cho cơ chế xoay tour nếu chưa có
    cursor.execute("SELECT COUNT(*) as count FROM api_keys")
    key_count = cursor.fetchone()["count"]

    if key_count == 0:
        logger.info("Khởi tạo danh sách API Keys mẫu cho cơ chế xoay tour...")
        keys_data = [
            (str(uuid.uuid4())[:8], "kaggle", "Kaggle TPU Qwen2.5-VL", "https://hybrid-ocr.trycloudflare.com", "Qwen2.5-VL-7B", "", 1, 1, 0),
            (str(uuid.uuid4())[:8], "gemini", "Gemini 1.5 Flash - Slot 1", "AIzaSy_DEMO_KEY_SLOT_1", "gemini-1.5-flash", "", 1, 2, 0),
            (str(uuid.uuid4())[:8], "gemini", "Gemini 1.5 Flash - Slot 2", "AIzaSy_DEMO_KEY_SLOT_2", "gemini-1.5-flash", "", 1, 3, 0),
            (str(uuid.uuid4())[:8], "groq", "Groq LLaMA Vision Backup", "gsk_DEMO_KEY_GROQ_1", "llama-3.2-11b-vision", "https://api.groq.com/openai/v1", 1, 4, 0)
        ]
        cursor.executemany(
            """INSERT INTO api_keys 
               (id, provider, key_alias, key_value, model_name, base_url, is_active, priority, usage_count) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            keys_data
        )

    # Đảm bảo bảng documents có cột translated_markdown
    try:
        cursor.execute("SELECT translated_markdown FROM documents LIMIT 1")
    except sqlite3.OperationalError:
        try:
            cursor.execute("ALTER TABLE documents ADD COLUMN translated_markdown TEXT")
            logger.info("Đã bổ sung cột translated_markdown vào bảng documents.")
        except Exception as e:
            logger.warning(f"Không thể thêm cột translated_markdown: {e}")

    conn.commit()
    conn.close()
    logger.info(f"Khởi tạo CSDL SQLite hoàn tất tại: {DB_PATH}")

# --- Các hàm thao tác User ---

def get_user_by_username(username: str) -> Optional[dict]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id: str) -> Optional[dict]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_user(username: str, email: str, password: str, role: str = "user") -> dict:
    conn = get_db_connection()
    user_id = str(uuid.uuid4())[:8]
    hashed_pw = generate_password_hash(password)
    conn.execute(
        "INSERT INTO users (id, username, email, password_hash, role) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, email, hashed_pw, role)
    )
    conn.commit()
    conn.close()
    return {"id": user_id, "username": username, "email": email, "role": role}

# --- Các hàm thao tác Document (Kho lưu trữ tài liệu) ---

def create_document(
    user_id: str,
    filename: str,
    file_size: int,
    total_pages: int,
    digital_pages: int,
    scanned_pages: int,
    full_markdown: str,
    model_used: str = "Fast-Path",
    language: str = "vi",
    processing_time: float = 0.0
) -> dict:
    conn = get_db_connection()
    doc_id = str(uuid.uuid4())[:8]
    conn.execute(
        """INSERT INTO documents 
           (id, user_id, filename, file_size, total_pages, digital_pages, scanned_pages, 
            full_markdown, model_used, language, processing_time) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (doc_id, user_id, filename, file_size, total_pages, digital_pages, scanned_pages,
         full_markdown, model_used, language, processing_time)
    )
    conn.commit()
    conn.close()
    return {
        "id": doc_id,
        "filename": filename,
        "total_pages": total_pages,
        "digital_pages": digital_pages,
        "scanned_pages": scanned_pages,
        "processing_time": processing_time
    }

def get_documents_by_user(user_id: str) -> List[dict]:
    conn = get_db_connection()
    rows = conn.execute(
        """SELECT id, filename, file_size, total_pages, digital_pages, scanned_pages, 
                  model_used, language, status, processing_time, created_at 
           FROM documents WHERE user_id = ? ORDER BY created_at DESC""",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_document_by_id(doc_id: str, user_id: Optional[str] = None) -> Optional[dict]:
    conn = get_db_connection()
    query = "SELECT * FROM documents WHERE id = ?"
    params = [doc_id]
    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_document(doc_id: str, user_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM documents WHERE id = ? AND user_id = ?", (doc_id, user_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def update_document_translation(doc_id: str, user_id: str, translated_markdown: str) -> bool:
    """Cập nhật nội dung bản dịch Markdown của tài liệu vào CSDL."""
    conn = get_db_connection()
    cursor = conn.execute(
        "UPDATE documents SET translated_markdown = ? WHERE id = ? AND user_id = ?",
        (translated_markdown, doc_id, user_id)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

# --- Các hàm thao tác API Key & Xoay Tour ---

def get_all_api_keys() -> List[dict]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM api_keys ORDER BY priority ASC, created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_active_keys_by_provider(provider: str) -> List[dict]:
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM api_keys WHERE provider = ? AND is_active = 1 ORDER BY usage_count ASC, priority ASC",
        (provider,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_api_key(provider: str, key_alias: str, key_value: str, model_name: str, base_url: str = "", priority: int = 1) -> dict:
    conn = get_db_connection()
    key_id = str(uuid.uuid4())[:8]
    conn.execute(
        """INSERT INTO api_keys 
           (id, provider, key_alias, key_value, model_name, base_url, priority) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (key_id, provider, key_alias, key_value, model_name, base_url, priority)
    )
    conn.commit()
    conn.close()
    return {"id": key_id, "provider": provider, "key_alias": key_alias, "model_name": model_name}

def toggle_api_key_status(key_id: str) -> Optional[int]:
    conn = get_db_connection()
    row = conn.execute("SELECT is_active FROM api_keys WHERE id = ?", (key_id,)).fetchone()
    if not row:
        conn.close()
        return None
    new_status = 0 if row["is_active"] == 1 else 1
    conn.execute("UPDATE api_keys SET is_active = ? WHERE id = ?", (new_status, key_id))
    conn.commit()
    conn.close()
    return new_status

def increment_api_key_usage(key_id: str):
    conn = get_db_connection()
    conn.execute(
        "UPDATE api_keys SET usage_count = usage_count + 1, last_used_at = CURRENT_TIMESTAMP WHERE id = ?",
        (key_id,)
    )
    conn.commit()
    conn.close()

def delete_api_key(key_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM api_keys WHERE id = ?", (key_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

# --- Cac ham thong ke va quan ly danh cho Admin ---

def get_all_users() -> List[dict]:
    """Lay danh sach tat ca nguoi dung trong he thong (khong tra ve password_hash)."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_admin_system_stats() -> dict:
    """Tong hop chi so hoat dong toan he thong danh cho Bang Quan Tri Admin."""
    conn = get_db_connection()
    total_users = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()["count"]
    total_docs = conn.execute("SELECT COUNT(*) as count FROM documents").fetchone()["count"]
    total_keys = conn.execute("SELECT COUNT(*) as count FROM api_keys").fetchone()["count"]
    active_keys = conn.execute("SELECT COUNT(*) as count FROM api_keys WHERE is_active = 1").fetchone()["count"]
    total_usage = conn.execute("SELECT COALESCE(SUM(usage_count), 0) as total FROM api_keys").fetchone()["total"]
    
    # Lay 5 tai lieu gan nhat toan he thong lam nhat ky xu ly
    recent_docs = conn.execute(
        """SELECT d.id, d.filename, d.total_pages, d.model_used, d.processing_time, d.created_at, u.username
           FROM documents d
           LEFT JOIN users u ON d.user_id = u.id
           ORDER BY d.created_at DESC LIMIT 5"""
    ).fetchall()
    
    conn.close()
    return {
        "total_users": total_users,
        "total_documents": total_docs,
        "total_keys": total_keys,
        "active_keys": active_keys,
        "total_key_usage": total_usage,
        "recent_activity": [dict(r) for r in recent_docs]
    }

# --- Cac ham quan ly cau hinh ca nhan hoa nguoi dung (User Settings) ---

def get_user_settings(user_id: str) -> dict:
    """Lay cau hinh ca nhan cua nguoi dung, neu chua co se tu dong tao mac dinh."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,)).fetchone()
    if not row:
        conn.execute(
            """INSERT OR IGNORE INTO user_settings 
               (user_id, theme, language, default_model, default_target_lang, fast_path_default)
               VALUES (?, 'light', 'vi', 'auto', 'vi', 1)""",
            (user_id,)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else {
        "user_id": user_id,
        "theme": "light",
        "language": "vi",
        "default_model": "auto",
        "default_target_lang": "vi",
        "fast_path_default": 1
    }

def update_user_settings(user_id: str, settings: dict) -> dict:
    """Cap nhat cau hinh ca nhan cua nguoi dung."""
    conn = get_db_connection()
    # Dam bao da co ban ghi
    get_user_settings(user_id)

    theme = settings.get("theme", "light")
    language = settings.get("language", "vi")
    default_model = settings.get("default_model", "auto")
    default_target_lang = settings.get("default_target_lang", "vi")
    fast_path_default = 1 if settings.get("fast_path_default", True) else 0

    conn.execute(
        """UPDATE user_settings 
           SET theme = ?, language = ?, default_model = ?, default_target_lang = ?, 
               fast_path_default = ?, updated_at = CURRENT_TIMESTAMP
           WHERE user_id = ?""",
        (theme, language, default_model, default_target_lang, fast_path_default, user_id)
    )
    conn.commit()
    conn.close()
    return get_user_settings(user_id)

def update_user_password(user_id: str, new_password_hash: str) -> bool:
    """Cap nhat mat khau moi da ma hoa cho nguoi dung."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_password_hash, user_id))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

