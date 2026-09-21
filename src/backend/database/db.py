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
