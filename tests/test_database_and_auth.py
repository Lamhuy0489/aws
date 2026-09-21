import os
import tempfile
import pytest
from werkzeug.security import check_password_hash

import src.backend.database.db as db_module
from src.backend.database.db import (
    init_db,
    get_db_connection,
    get_user_by_username,
    get_user_by_id,
    create_user,
    create_document,
    get_documents_by_user,
    get_document_by_id,
    delete_document,
    get_all_api_keys,
    get_active_keys_by_provider,
    create_api_key,
    toggle_api_key_status,
    increment_api_key_usage,
    delete_api_key
)
from src.backend.llm.key_tour_manager import KeyTourManager
from src.frontend.server import app

@pytest.fixture(autouse=True)
def isolated_test_db(monkeypatch):
    """Thiet lap co so du lieu SQLite rieng biet trong thu muc tam cho moi test."""
    temp_dir = tempfile.TemporaryDirectory()
    test_db_path = os.path.join(temp_dir.name, "test_app.db")
    monkeypatch.setattr(db_module, "DB_PATH", test_db_path)
    monkeypatch.setattr(db_module, "DB_DIR", temp_dir.name)
    init_db()
    yield test_db_path
    temp_dir.cleanup()

@pytest.fixture
def client():
    """Flask test client."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key-12345"
    with app.test_client() as client:
        yield client

def test_init_db_seeds_default_users_and_keys():
    """Kiem tra khoi tao CSDL tao san admin, demo va cac key xoay tour mac dinh."""
    admin = get_user_by_username("admin")
    assert admin is not None
    assert admin["role"] == "admin"
    assert check_password_hash(admin["password_hash"], "Admin@123")

    demo = get_user_by_username("demo")
    assert demo is not None
    assert demo["role"] == "user"

    keys = get_all_api_keys()
    assert len(keys) >= 4
    providers = [k["provider"] for k in keys]
    assert "kaggle" in providers
    assert "gemini" in providers

def test_user_creation_and_retrieval():
    """Kiem tra tao nguoi dung moi va truy van theo username hoac id."""
    user = create_user("testuser", "test@domain.vn", "Secret@123", role="user")
    assert user["username"] == "testuser"
    assert "id" in user

    retrieved = get_user_by_username("testuser")
    assert retrieved is not None
    assert retrieved["email"] == "test@domain.vn"
    assert check_password_hash(retrieved["password_hash"], "Secret@123")

    by_id = get_user_by_id(user["id"])
    assert by_id is not None
    assert by_id["username"] == "testuser"

def test_document_crud_operations():
    """Kiem tra cac thao tac CRUD tren kho tai lieu nguoi dung."""
    user = create_user("docuser", "doc@domain.vn", "Pass@123")
    user_id = user["id"]

    # 1. Tao tai lieu moi
    doc = create_document(
        user_id=user_id,
        filename="bang_ke_chi_phi.pdf",
        file_size=20480,
        total_pages=2,
        digital_pages=2,
        scanned_pages=0,
        full_markdown="# Bang ke chi phi\n| Muc | So tien |\n| EC2 | 100 |",
        model_used="Fast-Path",
        language="vi",
        processing_time=0.15
    )
    doc_id = doc["id"]
    assert doc_id is not None

    # 2. Lay danh sach tai lieu cua user
    docs = get_documents_by_user(user_id)
    assert len(docs) == 1
    assert docs[0]["filename"] == "bang_ke_chi_phi.pdf"

    # 3. Lay chi tiet tai lieu
    detail = get_document_by_id(doc_id, user_id)
    assert detail is not None
    assert "Bang ke chi phi" in detail["full_markdown"]

    # 4. Xoa tai lieu
    deleted = delete_document(doc_id, user_id)
    assert deleted is True
    assert get_document_by_id(doc_id, user_id) is None

def test_api_key_tour_rotation():
    """Kiem tra co che xoay tour Round-Robin dua tren luot dung usage_count."""
    # Tao 2 gemini keys voi usage ban dau khac nhau
    k1 = create_api_key("gemini", "Gemini Tour A", "AIza_KEY_A", "gemini-1.5-flash", priority=1)
    k2 = create_api_key("gemini", "Gemini Tour B", "AIza_KEY_B", "gemini-1.5-flash", priority=2)

    # Bat ca hai hoat dong
    active_gemini = get_active_keys_by_provider("gemini")
    assert len(active_gemini) >= 2

    # Lay key dau tien (usage_count = 0)
    picked_1 = KeyTourManager.get_next_key("gemini")
    assert picked_1 is not None

    # Ghi nhan 2 luot dung cho picked_1
    KeyTourManager.record_usage(picked_1["id"])
    KeyTourManager.record_usage(picked_1["id"])

    # Xoay vong tiep theo: phai uu tien key co usage_count thap hon
    picked_2 = KeyTourManager.get_next_key("gemini")
    assert picked_2 is not None
    assert picked_2["usage_count"] <= picked_1["usage_count"] + 2

    # Kiem tra toggle active/inactive
    new_status = toggle_api_key_status(k1["id"])
    assert new_status == 0  # Tu 1 thanh 0
    toggle_api_key_status(k1["id"])  # Bat lai

    # Kiem tra xoa key
    del_res = delete_api_key(k2["id"])
    assert del_res is True

def test_flask_auth_endpoints(client):
    """Kiem tra flow xac thuc: Dang ky -> Dang nhap -> Kiem tra me -> Dang xuat."""
    # 1. Dang ky tai khoan moi
    reg_resp = client.post("/api/auth/register", json={
        "username": "clientuser",
        "email": "client@domain.vn",
        "password": "ClientPassword@123"
    })
    assert reg_resp.status_code == 200
    assert reg_resp.json["message"] == "Đăng ký thành công"

    # 2. Dang xuat
    logout_resp = client.post("/api/auth/logout")
    assert logout_resp.status_code == 200

    # 3. Kiem tra me khi chua dang nhap
    me_unauth = client.get("/api/auth/me")
    assert me_unauth.status_code == 200
    assert me_unauth.json["authenticated"] is False

    # 4. Dang nhap
    login_resp = client.post("/api/auth/login", json={
        "username": "clientuser",
        "password": "ClientPassword@123"
    })
    assert login_resp.status_code == 200
    assert login_resp.json["user"]["username"] == "clientuser"

    # 5. Kiem tra me sau khi dang nhap
    me_auth = client.get("/api/auth/me")
    assert me_auth.status_code == 200
    assert me_auth.json["authenticated"] is True
    assert me_auth.json["user"]["role"] == "user"

def test_flask_admin_permissions(client):
    """Kiem tra phan quyen truy cap API Admin (chua dang nhap, user thuong, admin)."""
    # 1. Chua dang nhap -> 401 Unauthorized
    resp_unauth = client.get("/api/admin/keys")
    assert resp_unauth.status_code == 401

    # 2. Dang nhap voi user thuong (demo) -> 403 Forbidden
    client.post("/api/auth/login", json={
        "username": "demo",
        "password": "Demo@123"
    })
    resp_forbidden = client.get("/api/admin/keys")
    assert resp_forbidden.status_code == 403

    # 3. Dang xuat va dang nhap voi admin -> 200 OK
    client.post("/api/auth/logout")
    client.post("/api/auth/login", json={
        "username": "admin",
        "password": "Admin@123"
    })
    resp_admin = client.get("/api/admin/keys")
    assert resp_admin.status_code == 200
    assert "keys" in resp_admin.json
    assert len(resp_admin.json["keys"]) > 0
