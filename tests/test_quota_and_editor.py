import os
import sys
import unittest

# Đặt đường dẫn gốc của project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.database.db import (
    init_db,
    get_user_aws_quota,
    increment_user_aws_usage,
    refund_user_aws_usage,
    update_document_markdown,
    create_user,
    get_user_by_username
)
from src.frontend.server import app

class TestQuotaAndEditor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.test_user = get_user_by_username("demo")
        if not cls.test_user:
            cls.test_user = create_user("demo", "demo@cloudjourney.vn", "Demo@123", "user")

    def test_aws_quota_lifecycle(self):
        user_id = self.test_user["id"]
        
        # 1. Quota ban đầu
        initial = get_user_aws_quota(user_id, limit=20)
        self.assertIn("remaining", initial)
        self.assertIn("used", initial)
        self.assertEqual(initial["limit"], 20)

        # 2. Increment quota
        after_inc = increment_user_aws_usage(user_id, limit=20)
        self.assertEqual(after_inc["used"], initial["used"] + 1)
        self.assertEqual(after_inc["remaining"], initial["remaining"] - 1)

        # 3. Refund quota
        after_refund = refund_user_aws_usage(user_id, limit=20)
        self.assertEqual(after_refund["used"], initial["used"])
        self.assertEqual(after_refund["remaining"], initial["remaining"])

    def test_markdown_update(self):
        user_id = self.test_user["id"]
        # Thử cập nhật document id giả lập (kết quả trả về False vì id không tồn tại nhưng không lỗi cú pháp)
        res = update_document_markdown("non-existent-doc", user_id, "# New Markdown Content")
        self.assertFalse(res)

    def test_quota_endpoint(self):
        client = app.test_client()
        with client.session_transaction() as sess:
            sess["user_id"] = self.test_user["id"]

        resp = client.get("/api/studio/quota")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("aws_quota", data)
        self.assertEqual(data["aws_quota"]["limit"], 20)

    def test_update_markdown_endpoint(self):
        from src.backend.database.db import create_document
        user_id = self.test_user["id"]
        doc = create_document(
            user_id=user_id,
            filename="sample_test.pdf",
            file_size=1024,
            total_pages=1,
            digital_pages=1,
            scanned_pages=0,
            full_markdown="# Original Text",
            model_used="aws-bedrock",
            language="vi",
            processing_time=1.0
        )
        doc_id = doc["id"]

        client = app.test_client()
        with client.session_transaction() as sess:
            sess["user_id"] = user_id

        # Update original markdown
        resp = client.post(f"/api/studio/document/{doc_id}/markdown", json={
            "markdown": "# Modified Content by User",
            "tab_type": "original"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json().get("success"))

        from src.backend.database.db import get_document_by_id
        updated = get_document_by_id(doc_id, user_id=user_id)
        self.assertEqual(updated["full_markdown"], "# Modified Content by User")

if __name__ == "__main__":
    unittest.main()
