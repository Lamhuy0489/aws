import os
import tempfile
import pytest
from werkzeug.security import check_password_hash

import src.backend.database.db as db_module
from src.backend.database.db import (
    init_db,
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
    delete_api_key,
    get_all_users,
    get_admin_system_stats
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

def test_document_isolation_between_accounts():
    """Kiem tra ranh gioi tai lieu chat che giua hai tai khoan khac nhau."""
    user_a = create_user("usera", "a@domain.vn", "Pass@123")
    user_b = create_user("userb", "b@domain.vn", "Pass@123")

    # User A tao 1 tai lieu
    doc_a = create_document(
        user_id=user_a["id"],
        filename="bang_ke_user_a.pdf",
        file_size=1024,
        total_pages=1,
        digital_pages=1,
        scanned_pages=0,
        full_markdown="# Document of User A",
        model_used="Fast-Path",
        language="vi"
    )

    # User A nhin thay tai lieu cua minh
    docs_a = get_documents_by_user(user_a["id"])
    assert len(docs_a) == 1
    assert docs_a[0]["id"] == doc_a["id"]

    # User B KHONG nhin thay tai lieu cua User A
    docs_b = get_documents_by_user(user_b["id"])
    assert len(docs_b) == 0

    # User B khong the lay chi tiet tai lieu cua User A
    doc_detail_for_b = get_document_by_id(doc_a["id"], user_id=user_b["id"])
    assert doc_detail_for_b is None

    # User B khong the xoa tai lieu cua User A
    delete_result = delete_document(doc_a["id"], user_id=user_b["id"])
    assert delete_result is False

    # Tai lieu cua User A van con nguyen ven
    assert get_document_by_id(doc_a["id"], user_id=user_a["id"]) is not None

def test_api_key_tour_and_admin_stats():
    """Kiem tra co che xoay tour va thong ke he thong admin."""
    # 1. Thong ke ban dau
    stats = get_admin_system_stats()
    assert stats["total_users"] >= 2
    assert stats["total_keys"] >= 4
    assert stats["active_keys"] >= 4

    # 2. Xoay tour key
    picked = KeyTourManager.get_next_key("gemini")
    assert picked is not None
    KeyTourManager.record_usage(picked["id"])

    updated_stats = get_admin_system_stats()
    assert updated_stats["total_key_usage"] >= 1

    # 3. Lay danh sach user admin
    users = get_all_users()
    assert len(users) >= 2
    for u in users:
        assert "password_hash" not in u

def test_role_based_login_redirection(client):
    """Kiem tra form dang nhap tu dong chuyen huong: admin -> /admin, user -> /studio."""
    # 1. Dang nhap tai khoan Admin -> redirect sang /admin
    resp_admin = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "Admin@123"
    })
    assert resp_admin.status_code == 200
    assert resp_admin.json["redirect_url"] == "/admin"

    # 2. Dang xuat
    client.post("/api/auth/logout")

    # 3. Dang nhap tai khoan User (demo) -> redirect sang /studio
    resp_user = client.post("/api/auth/login", json={
        "username": "demo",
        "password": "Demo@123"
    })
    assert resp_user.status_code == 200
    assert resp_user.json["redirect_url"] == "/studio"

def test_multi_page_view_routes_and_protection(client):
    """Kiem tra dieu huong da trang va bao ve ranh gioi giua cac route HTML."""
    # 1. Chua dang nhap:
    # GET / -> 302 ve /login
    resp_root = client.get("/")
    assert resp_root.status_code == 302
    assert "/login" in resp_root.headers["Location"]

    # GET /studio -> 302 ve /login
    resp_studio_unauth = client.get("/studio")
    assert resp_studio_unauth.status_code == 302
    assert "/login" in resp_studio_unauth.headers["Location"]

    # GET /admin -> 302 ve /login
    resp_admin_unauth = client.get("/admin")
    assert resp_admin_unauth.status_code == 302
    assert "/login" in resp_admin_unauth.headers["Location"]

    # 2. Dang nhap tai khoan user thuong (demo)
    client.post("/api/auth/login", json={"username": "demo", "password": "Demo@123"})

    # GET /studio -> 200 OK
    resp_studio_auth = client.get("/studio")
    assert resp_studio_auth.status_code == 200
    assert b"Studio" in resp_studio_auth.data

    # GET /library -> 200 OK
    resp_lib_auth = client.get("/library")
    assert resp_lib_auth.status_code == 200
    assert b"Kho" in resp_lib_auth.data

    # GET /admin -> 403 Forbidden
    resp_admin_forbidden = client.get("/admin")
    assert resp_admin_forbidden.status_code == 403
    assert b"403" in resp_admin_forbidden.data

    # 3. Dang xuat va dang nhap voi admin
    client.post("/api/auth/logout")
    client.post("/api/auth/login", json={"username": "admin", "password": "Admin@123"})

    # GET /admin -> 200 OK
    resp_admin_ok = client.get("/admin")
    assert resp_admin_ok.status_code == 200
    assert b"Quan" in resp_admin_ok.data

    # GET /api/admin/stats -> 200 OK
    resp_stats = client.get("/api/admin/stats")
    assert resp_stats.status_code == 200
    assert "stats" in resp_stats.json

def test_studio_active_document_persistence(client):
    """Kiem tra luu tru va khôi phuc state tai lieu dang thao tac giua Studio va CSDL."""
    # Dang nhap
    client.post("/api/auth/login", json={"username": "demo", "password": "Demo@123"})
    demo = get_user_by_username("demo")

    # Khi chua co tai lieu nao, active-document tra ve None
    resp_init = client.get("/api/studio/active-document")
    assert resp_init.status_code == 200
    assert resp_init.json["document"] is None

    # Tao tai lieu moi cho user
    doc = create_document(
        user_id=demo["id"],
        filename="bao_cao_tai_chinh.pdf",
        file_size=5000,
        total_pages=2,
        digital_pages=2,
        scanned_pages=0,
        full_markdown="# Bao Cao Tai Chinh",
        model_used="Fast-Path",
        language="vi"
    )

    # GET active-document tra ve tai lieu vua tao
    resp_active = client.get("/api/studio/active-document")
    assert resp_active.status_code == 200
    assert resp_active.json["document"] is not None
    assert resp_active.json["document"]["filename"] == "bao_cao_tai_chinh.pdf"

    # POST active-document de set id
    resp_set = client.post("/api/studio/active-document", json={"document_id": doc["id"]})
    assert resp_set.status_code == 200
    assert resp_set.json["active_document_id"] == doc["id"]

    # DELETE active-document
    resp_del = client.delete("/api/studio/active-document")
    assert resp_del.status_code == 200
    assert resp_del.json["success"] is True

def test_document_translation_db_update():
    """Kiem tra cap nhat ban dich Markdown vao CSDL."""
    from src.backend.database.db import update_document_translation
    demo = get_user_by_username("demo")
    doc = create_document(
        user_id=demo["id"],
        filename="hop_dong.pdf",
        file_size=2048,
        total_pages=1,
        digital_pages=1,
        scanned_pages=0,
        full_markdown="# Hop Dong Kinh Te",
        model_used="Fast-Path",
        language="vi"
    )

    # Cap nhat ban dich
    ok = update_document_translation(doc["id"], demo["id"], "# Economic Contract (English Translation)")
    assert ok is True

    # Truy van lai de kiem tra
    retrieved = get_document_by_id(doc["id"], demo["id"])
    assert retrieved["translated_markdown"] == "# Economic Contract (English Translation)"
