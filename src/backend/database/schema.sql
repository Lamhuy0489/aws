-- Bảng thông tin người dùng và phân quyền
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user', -- 'user' hoặc 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng lưu trữ lịch sử tài liệu bóc tách của người dùng
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_size INTEGER DEFAULT 0,
    total_pages INTEGER DEFAULT 1,
    digital_pages INTEGER DEFAULT 0,
    scanned_pages INTEGER DEFAULT 0,
    model_used TEXT DEFAULT 'Fast-Path',
    language TEXT DEFAULT 'vi',
    status TEXT DEFAULT 'COMPLETED',
    full_markdown TEXT NOT NULL,
    processing_time REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Bảng quản lý API Keys và cấu hình xoay vòng (Key Tour)
CREATE TABLE IF NOT EXISTS api_keys (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,          -- 'kaggle', 'gemini', 'groq', 'openai'
    key_alias TEXT NOT NULL,         -- Tên định danh (vd: 'Gemini Primary', 'Kaggle TPU 1')
    key_value TEXT NOT NULL,         -- API Key hoặc Tunnel URL
    model_name TEXT NOT NULL,        -- 'Qwen2.5-VL-7B', 'gemini-1.5-flash', etc.
    base_url TEXT DEFAULT '',        -- URL phụ trợ nếu có
    is_active INTEGER DEFAULT 1,     -- 1: Hoạt động, 0: Tạm dừng
    priority INTEGER DEFAULT 1,      -- Mức ưu tiên (1: cao nhất)
    usage_count INTEGER DEFAULT 0,   -- Số lượt đã gọi để xoay tour
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
