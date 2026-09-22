# Quy Tắc Vận Hành Dự Án & Bộ Não Tri Thức (Project Agent Rules)

Tài liệu này định hình vai trò, ngữ cảnh và các quy tắc vận hành bất biến cho mọi AI Agent làm việc trong kho lưu trữ này.

---

## 1. Vai Trò & Ngữ Cảnh Dự Án

* **Tên đề tài**: **Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS**
* **Mục tiêu chuyên môn**: Xây dựng nền tảng đám mây xử lý, bóc tách tài liệu số/scan (Fast-Path PyMuPDF + Kaggle/Gemini Vision OCR), dịch thuật tài liệu kỹ thuật bảo toàn 100% cấu trúc Markdown và bảng biểu số liệu, xuất bản đa định dạng (.md, .docx, .pdf chuẩn in ấn A4).
* **Định hướng mở rộng**: Hỗ trợ tùy chọn **AWS Native AI khép kín (Amazon Bedrock / Amazon Textract / Amazon Translate)** ở dạng tùy chọn phụ (Secondary Optional, mặc định tắt để bảo vệ ngân sách FinOps 0 USD).
* **Phạm vi tuyệt đối**: Tập trung duy nhất vào chu trình **Bóc Tách OCR -> Dịch Thuật Kỹ Thuật -> Xuất Bản Đa Định Dạng**. Tuyệt đối **KHÔNG** đưa vào chatbot hay RAG ngoài lề.

* **Thông tin định danh học viên & Tài khoản AWS**:
  * **Học viên**: Lâm Quang Huy
  * **MSSV**: `0212267` | **Lớp**: 67CS - Khoa Công nghệ Thông tin, Trường Đại học Xây dựng Hà Nội (HUCE)
  * **AWS Account ID**: `677994024390` | **Account Name**: `huylam`
  * **AWS Region**: `ap-southeast-1` (Singapore) | **IAM Principal**: `dev_admin`
  * **S3 Bucket**: `huylam-ocr-documents-ap-southeast-1` (`uploads/`, `outputs/`)
  * **DynamoDB Table**: `document_processing_jobs` (Partition Key `job_id`, Sort Key `created_at`, On-Demand mode)
  * **SSM Parameter**: `/huylam-ocr/config` (SecureString, KMS `alias/aws/ssm`)

---

## 2. Các Ràng Buộc Bất Biến (Strict Behavioral Rules)

1. **Quy tắc tuyệt đối không dùng Emoji / Icon**:
   * Tuyệt đối không sử dụng bất kỳ emoji, icon, hay ký tự trang trí Unicode nào trong lời thoại, mã nguồn, tài liệu markdown, commit message hay tên tệp.
   * Chỉ sử dụng văn bản thuần chuẩn mực (plain text) và định dạng GitHub Flavored Markdown.
2. **Quy tắc ngôn ngữ**:
   * Luôn phản hồi bằng tiếng Việt chuẩn, có dấu đầy đủ, ngữ pháp chính xác và văn phong kỹ thuật chuyên nghiệp.
3. **Quy tắc liên kết tệp**:
   * Luôn sử dụng cú pháp clickable link `file://` cho mọi đường dẫn tệp cục bộ (ví dụ: `[ROADMAP.md](file:///Users/huylam/Downloads/aws/ROADMAP.md)`).
4. **Kỷ luật tài chính đám mây (FinOps 0 USD)**:
   * Mọi tài nguyên AWS đề xuất hoặc khởi tạo phải nằm trong gói AWS Free Tier hoặc chế độ On-Demand không phát sinh chi phí khi nhàn rỗi.
   * Sau khi hoàn tất đo kiểm các dịch vụ tính cước theo giờ (như EC2, ECS Task), phải hướng dẫn người dùng thực hiện quy trình Teardown dọn sạch tài nguyên.

---

## 3. Cấu Trúc Hệ Thống & Nguồn Sự Thật

1. **[ROADMAP.md](file:///Users/huylam/Downloads/aws/ROADMAP.md)**: Nguồn sự thật duy nhất về tiến độ thực hiện (Checklist) của 12 tuần thực tập và các đầu việc cần làm.
2. **`raw/`**: Thư mục dữ liệu nguồn thô, chỉ đọc (các tài liệu đề bài, checklist FCJ). Tuyệt đối không sửa đổi hoặc xóa tệp trong thư mục này.
3. **`wiki/`**: Kho tri thức Obsidian được biên dịch theo phương pháp Karpathy, gồm `index.md`, `log.md`, `concepts/`, `sources/`, `syntheses/`, `outputs/`.
4. **`src/`**: Mã nguồn ứng dụng (gồm `backend/` và `frontend/`).
5. **`workshop/`**: Website báo cáo thực tập xây dựng bằng Hugo (gồm các Worklog từ Tuần 1 đến Tuần 12, Proposal, Workshop guide).

---

## 4. Bốn Chu Kỳ Vận Hành Tri Thức

- **Ingest**: Tiếp nhận tài liệu mới vào `raw/`, tạo bản tóm tắt trong `wiki/sources/`, trích xuất khái niệm vào `wiki/concepts/`, cập nhật `wiki/index.md` và ghi nhật ký vào `wiki/log.md`.
- **Compile**: Tổng hợp nhiều nguồn tri thức thành bài viết chuyên sâu trong `wiki/syntheses/`.
- **Query**: Tra cứu chéo giữa `wiki/`, `raw/` và `ROADMAP.md` để trả lời chính xác, trích dẫn liên kết dạng `[[ten-tep]]`.
- **Lint**: Rà soát các liên kết hỏng, phát hiện mâu thuẫn thông tin và đảm bảo tính nhất quán của hệ thống.
