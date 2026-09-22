import os
import tempfile
import pytest
from werkzeug.security import check_password_hash

import src.backend.database.db as db_module
from src.backend.database.db import (
    init_db,
    get_user_by_username,
    get_user_settings,
    get_all_api_keys
)
from src.frontend.server import app

@pytest.fixture(autouse=True)
def isolated_test_db(monkeypatch):
    """Thiết lập CSDL SQLite tạm thời riêng biệt cho từng bài kiểm thử."""
    temp_dir = tempfile.TemporaryDirectory()
    test_db_path = os.path.join(temp_dir.name, "test_app.db")
    monkeypatch.setattr(db_module, "DB_PATH", test_db_path)
    monkeypatch.setattr(db_module, "DB_DIR", temp_dir.name)
    init_db()
    yield test_db_path
    temp_dir.cleanup()

@pytest.fixture
def client():
    """Khởi tạo Flask test client."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key-admin-settings"
    with app.test_client() as client:
        yield client

def login_user(client, username, password):
    """Tiện ích đăng nhập vào hệ thống."""
    return client.post("/api/auth/login", json={"username": username, "password": password})

# ==============================================================================
# 1. KIỂM THỬ ĐIỂM CUỐI CÀI ĐẶT CÁ NHÂN HÓA (/api/settings)
# ==============================================================================

def test_settings_unauthorized_access(client):
    """Kiểm tra chặn người dùng chưa đăng nhập truy cập API cài đặt."""
    res_get = client.get("/api/settings")
    assert res_get.status_code == 401

    res_post = client.post("/api/settings", json={"theme": "dark"})
    assert res_post.status_code == 401

def test_settings_get_and_update(client):
    """Kiểm tra đọc và cập nhật tùy chọn cá nhân thành công."""
    login_user(client, "demo", "Demo@123")

    # Đọc cấu hình mặc định
    res_get = client.get("/api/settings")
    assert res_get.status_code == 200
    assert "settings" in res_get.json
    assert res_get.json["settings"]["theme"] == "light"

    # Cập nhật cài đặt
    payload = {
        "theme": "dark",
        "language": "en",
        "default_model": "gemini-3.6-flash",
        "default_target_lang": "vi",
        "fast_path_default": False
    }
    res_post = client.post("/api/settings", json=payload)
    assert res_post.status_code == 200
    assert res_post.json["settings"]["theme"] == "dark"
    assert res_post.json["settings"]["language"] == "en"

def test_settings_change_password_flow(client):
    """Kiểm tra toàn diện quy trình đổi mật khẩu tài khoản."""
    login_user(client, "demo", "Demo@123")

    # Mật khẩu mới và xác nhận không khớp
    res_mismatch = client.post("/api/settings/password", json={
        "old_password": "Demo@123",
        "new_password": "NewPassword@123",
        "confirm_password": "DifferentPassword@123"
    })
    assert res_mismatch.status_code == 400
    assert "không khớp" in res_mismatch.json["error"]

    # Mật khẩu mới quá ngắn (< 6 ký tự)
    res_short = client.post("/api/settings/password", json={
        "old_password": "Demo@123",
        "new_password": "123",
        "confirm_password": "123"
    })
    assert res_short.status_code == 400

    # Nhập sai mật khẩu cũ
    res_wrong_old = client.post("/api/settings/password", json={
        "old_password": "WrongPassword@123",
        "new_password": "NewPassword@123",
        "confirm_password": "NewPassword@123"
    })
    assert res_wrong_old.status_code == 400
    assert "không chính xác" in res_wrong_old.json["error"]

    # Đổi mật khẩu thành công
    res_success = client.post("/api/settings/password", json={
        "old_password": "Demo@123",
        "new_password": "NewPassword@456",
        "confirm_password": "NewPassword@456"
    })
    assert res_success.status_code == 200
    assert "thành công" in res_success.json["message"]

    # Đăng xuất và thử đăng nhập bằng mật khẩu mới
    client.post("/api/auth/logout")
    res_login_new = client.post("/api/auth/login", json={"username": "demo", "password": "NewPassword@456"})
    assert res_login_new.status_code == 200

# ==============================================================================
# 2. KIỂM THỬ PHÂN QUYỀN VÀ API QUẢN TRỊ VIÊN (/api/admin/*)
# ==============================================================================

def test_admin_access_control(client):
    """Kiểm tra phân quyền nghiêm ngặt: User thường không được vào trang/API Admin."""
    # 1. Chưa đăng nhập
    res_unauth = client.get("/api/admin/stats")
    assert res_unauth.status_code == 401

    # 2. Đăng nhập bằng tài khoản User thường ('demo')
    login_user(client, "demo", "Demo@123")
    res_forbidden_stats = client.get("/api/admin/stats")
    assert res_forbidden_stats.status_code == 403

    res_forbidden_keys = client.get("/api/admin/keys")
    assert res_forbidden_keys.status_code == 403

    res_forbidden_users = client.get("/api/admin/users")
    assert res_forbidden_users.status_code == 403

def test_admin_crud_api_keys(client):
    """Kiểm tra luồng CRUD trọn vẹn của Quản trị viên đối với tour xoay API Key."""
    login_user(client, "admin", "Admin@123")

    # 1. Lấy danh sách khóa ban đầu
    res_keys = client.get("/api/admin/keys")
    assert res_keys.status_code == 200
    initial_count = len(res_keys.json["keys"])
    assert initial_count >= 4

    # 2. Thêm khóa mới vào tour xoay
    res_add = client.post("/api/admin/keys", json={
        "provider": "gemini",
        "key_alias": "Gemini Backup Automated Test",
        "key_value": "AIzaSy_AUTOMATED_TEST_SLOT_99",
        "model_name": "gemini-3.6-flash",
        "base_url": "",
        "priority": 2
    })
    assert res_add.status_code == 200
    new_key_id = res_add.json["key"]["id"]
    assert new_key_id is not None

    # 3. Tạm dừng khóa vừa tạo (Toggle)
    res_toggle_off = client.post(f"/api/admin/keys/{new_key_id}/toggle")
    assert res_toggle_off.status_code == 200
    assert res_toggle_off.json["is_active"] == 0

    # 4. Kích hoạt lại khóa (Toggle)
    res_toggle_on = client.post(f"/api/admin/keys/{new_key_id}/toggle")
    assert res_toggle_on.status_code == 200
    assert res_toggle_on.json["is_active"] == 1

    # 5. Xóa khóa khỏi tour xoay
    res_del = client.delete(f"/api/admin/keys/{new_key_id}")
    assert res_del.status_code == 200

    # 6. Xác nhận khóa đã không còn
    res_keys_after = client.get("/api/admin/keys")
    ids_after = [k["id"] for k in res_keys_after.json["keys"]]
    assert new_key_id not in ids_after

def test_admin_get_users_and_stats(client):
    """Kiểm tra lấy số liệu thống kê toàn hệ thống và danh sách người dùng."""
    login_user(client, "admin", "Admin@123")

    # Thống kê KPI
    res_stats = client.get("/api/admin/stats")
    assert res_stats.status_code == 200
    stats = res_stats.json["stats"]
    assert stats["total_users"] >= 2
    assert "active_keys" in stats

    # Danh sách người dùng
    res_users = client.get("/api/admin/users")
    assert res_users.status_code == 200
    users = res_users.json["users"]
    usernames = [u["username"] for u in users]
    assert "admin" in usernames
    assert "demo" in usernames
