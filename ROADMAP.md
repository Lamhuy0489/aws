# Lộ Trình Triển Khai Dự Án & Bản Đồ Tri Thức (Project Roadmap & Status)

Tài liệu này là nguồn sự thật duy nhất (Single Source of Truth) định hình ngữ cảnh, tiến độ và kế hoạch hành động cho toàn bộ dự án. Bất kỳ phiên làm việc hoặc Agent mới nào khi mở không gian làm việc này đều phải đọc và bám sát tài liệu này.

---

## 1. Thông Tin Tổng Quan Dự Án

* **Tên đề tài**: **Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS**
* **Mục tiêu cốt lõi**:
  1. Bóc tách tài liệu số siêu tốc Tầng 1 (Fast-Path bằng PyMuPDF trong 0.1s - 0.3s/trang, chi phí 0đ).
  2. Nhận diện thị giác Tầng 2 (Selective Vision OCR) cho trang scan/ảnh biểu mẫu (Kaggle GPU/TPU Qwen2.5-VL qua Cloudflare Tunnel kết hợp cơ chế tự phục hồi Failover sang Google Gemini 3.6 Flash).
  3. Dịch thuật tài liệu kỹ thuật đa ngôn ngữ (Technical Translation Engine) bảo toàn nguyên vẹn 100% cấu trúc Markdown và bảng biểu số liệu.
  4. Xuất bản tài liệu đa định dạng: Markdown (`.md`), Microsoft Word (`.docx`), PDF in ấn chuẩn A4 (`.pdf`).
  5. Giao diện Web Studio đơn trang (SPA) mượt mà không nhấp nháy, lưu trạng thái 2 lớp, quản trị tour xoay vòng API Key.
  6. **Tùy chọn mở rộng AWS Native AI khép kín (Secondary Optional)**: Hỗ trợ tích hợp Amazon Bedrock (Nova / Claude 3.5 Haiku) hoặc Amazon Textract / Amazon Translate phục vụ yêu cầu dữ liệu 100% nội bộ AWS. Chế độ này ở dạng tùy chọn phụ, mặc định tắt để đảm bảo FinOps 0 USD.
  * **Lưu ý đặc biệt**: Dự án tập trung thuần túy vào **Bóc tách OCR + Dịch thuật kỹ thuật + Xuất bản đa định dạng**, TUYỆT ĐỐI KHÔNG tích hợp chatbot hay RAG ngoài lề.

* **Thông tin định danh học viên & Môi trường AWS**:
  * **Họ và tên**: Lâm Quang Huy
  * **MSSV**: `0212267` | **Lớp**: 67CS - Khoa Công nghệ Thông tin, Trường Đại học Xây dựng Hà Nội (HUCE)
  * **AWS Account ID**: `677994024390`
  * **Tên tài khoản (Account Name)**: `huylam`
  * **Khu vực thực thi (AWS Region)**: `ap-southeast-1` (Asia Pacific - Singapore)
  * **IAM Principal**: `dev_admin` (`arn:aws:iam::677994024390:user/dev_admin`)
  * **Kho lưu trữ Amazon S3**: `huylam-ocr-documents-ap-southeast-1` (thư mục `uploads/` và `outputs/`)
  * **Bảng Amazon DynamoDB**: `document_processing_jobs` (Partition Key: `job_id`, Sort Key: `created_at`, On-Demand mode)
  * **Tham số AWS SSM Parameter Store**: `/huylam-ocr/config` (Loại `SecureString`, mã hóa KMS `alias/aws/ssm`)

---

## 2. Bảng Theo Dõi Tiến Độ Toàn Diện (Checklist)

### Giai đoạn 1: Đào tạo Nền tảng Hạ tầng AWS (Tuần 1 - Tuần 8) [HOÀN THÀNH 100%]
- [x] **Tuần 1**: Quản trị định danh và bảo mật (AWS IAM), giám sát cơ bản với Amazon CloudWatch Metrics.
- [x] **Tuần 2**: Thiết kế kiến trúc mạng Amazon VPC, Public/Private Subnets, Internet Gateway, NAT Gateway, Route Tables.
- [x] **Tuần 3**: Máy chủ ảo Amazon EC2 Linux & Windows, quản lý khối lưu trữ Amazon EBS Volumes và Snapshot.
- [x] **Tuần 4**: Lưu trữ đối tượng Amazon S3 (Static Website Hosting, Lifecycle Rules, Cross-Region Replication), AWS Systems Manager.
- [x] **Tuần 5**: Giám sát hệ thống tự động: Amazon CloudWatch Alarms, Metric Alarms và thông báo Amazon SNS.
- [x] **Tuần 6**: Kiến trúc sẵn sàng cao và co giãn tự động: Application Load Balancer (ALB), Auto Scaling Groups (ASG).
- [x] **Tuần 7**: Hạ tầng dưới dạng mã nguồn (IaC): AWS CloudFormation Stack tự động hóa, kiểm tra trôi dạt cấu hình (Drift Detection).
- [x] **Tuần 8**: Đóng gói và điều phối container: Docker, Amazon ECR (`huylam-web-app`), Amazon ECS Fargate (`huylam-ecs-cluster`, `huylam-web-service`), đo kiểm HTTP 200 OK, thực hiện FinOps Teardown giải phóng 100% tài nguyên về 0 USD.

### Giai đoạn 2: Phát triển Ứng dụng Cốt lõi Cục bộ (Local Web Studio) [HOÀN THÀNH 100%]
- [x] Xây dựng động cơ bóc tách nhanh Tầng 1: `FastNativeParser` bằng PyMuPDF (`src/backend/parsers/fast_parser.py`).
- [x] Xây dựng động cơ OCR chọn lọc Tầng 2: `OCRDispatcher` (`src/backend/parsers/ocr_dispatcher.py`) tích hợp Kaggle Qwen2.5-VL và cơ chế tự phục hồi sang Gemini 3.6 Flash.
- [x] Xây dựng bộ điều phối hợp nhất `HybridDocumentEngine` (`src/backend/parsers/hybrid_engine.py`).
- [x] Xây dựng động cơ dịch thuật tài liệu kỹ thuật `DocumentTranslator` (`src/backend/llm/translator.py`) đa ngôn ngữ, phân trang tự động, giữ nguyên bảng biểu Markdown.
- [x] Xây dựng bộ xuất bản đa định dạng `docx_exporter.py`, `pdf_exporter.py`, `markdown_exporter.py` (`src/backend/exporters/`).
- [x] Thiết kế giao diện Web Studio SPA hiện đại (`src/frontend/`): Điều hướng không giật lag (`spa_router.js`), lưu trạng thái hai lớp (`studio.js`), giao diện xem trước tài liệu song song (Split-view).
- [x] Xây dựng bảng điều khiển quản trị `/admin` quản lý KPI và Tour xoay vòng API Key (Round-Robin Tour Manager) (`src/backend/llm/key_tour_manager.py`).
- [x] Xây dựng màn hình cài đặt `/settings` hỗ trợ chuyển đổi giao diện sáng/tối, chọn ngôn ngữ và đổi mật khẩu an toàn.
- [x] Viết bộ kiểm thử tự động toàn diện: 27/27 bài kiểm thử `pytest` vượt qua 100% (`tests/`).
- [x] Dọn dẹp sạch sẽ các tệp dư thừa, đưa tài liệu báo cáo sự cố vào `docs/reports/`, chuẩn hóa `requirements.txt` và `.env.example`.
- [x] Đồng bộ toàn bộ mã nguồn lên kho lưu trữ GitHub `aws` nhánh `main`.

### Giai đoạn 3: Thiết kế Kiến trúc Serverless Capstone (Tuần 9) [HOÀN THÀNH 100%]
- [x] Nghiên cứu kiến trúc Serverless Computing và mô hình thực thi hướng sự kiện (Event-Driven) của AWS Lambda.
- [x] So sánh chi tiết ưu nhược điểm giữa Container (ECS Fargate) và Serverless (AWS Lambda) trong bài toán xử lý tài liệu không đồng bộ.
- [x] Thiết kế sơ đồ kiến trúc Serverless Microservices phân tầng kết hợp Amazon CloudFront, S3, API Gateway, Lambda, DynamoDB, SSM.
- [x] Thiết kế lược đồ cơ sở dữ liệu NoSQL Amazon DynamoDB (`document_processing_jobs`) với Partition Key `job_id`, Sort Key `created_at` và chế độ cước On-Demand (`PAY_PER_REQUEST`).
- [x] Thiết kế giải pháp cấp phát S3 Presigned URL khắc phục triệt để giới hạn 10 MB payload của API Gateway.
- [x] Biên soạn tài liệu Worklog Tuần 9 song ngữ trên website Hugo (`workshop/content/1-Worklog/1.9-Week9/`) và đẩy lên GitHub.

### Giai đoạn 4: Triển khai Hạ tầng Đám mây AWS (Tuần 10) [ĐANG TRIỂN KHAI]
- [x] Soạn thảo hướng dẫn thiết lập bằng tay từng bước (Manual Step-by-Step Setup Guide) trên AWS Management Console.
- [x] Cập nhật Đề xuất dự án Proposal bám sát tính năng OCR, Dịch thuật và tùy chọn mở rộng AWS Native AI.
- [x] Biên soạn Worklog Tuần 10 song ngữ trên website Hugo và đồng bộ lên GitHub `workshop`.
- [ ] **Thao tác 1**: Tạo kho lưu trữ Amazon S3 Bucket `huylam-ocr-documents-ap-southeast-1` trên Region `ap-southeast-1`:
  - [ ] Bật Block all public access.
  - [ ] Tạo thư mục `uploads/` (nhận tệp gốc).
  - [ ] Tạo thư mục `outputs/` (lưu kết quả MD, DOCX, PDF).
  - [ ] Cấu hình chính sách CORS cho phép các phương thức `GET`, `PUT`, `POST`, `HEAD`.
- [ ] **Thao tác 2**: Tạo bảng cơ sở dữ liệu Amazon DynamoDB `document_processing_jobs` trên Region `ap-southeast-1`:
  - [ ] Partition Key: `job_id` (String).
  - [ ] Sort Key: `created_at` (String).
  - [ ] Capacity Mode: On-Demand (`PAY_PER_REQUEST`).
- [ ] **Thao tác 3**: Tạo tham số bảo mật trên AWS Systems Manager Parameter Store:
  - [ ] Name: `/huylam-ocr/config`.
  - [ ] Type: `SecureString` (KMS Key: `alias/aws/ssm`).
  - [ ] Value: Cấu hình JSON chứa `ocr_mode`, `scan_threshold_chars`, `kaggle_endpoint`, `gemini_api_key`, `aws_native_mode_enabled: false`.
- [ ] **Thao tác 4 (Tùy chọn)**: Yêu cầu cấp quyền mô hình trên Amazon Bedrock (Nova Micro / Claude 3.5 Haiku) tại `us-east-1` hoặc `ap-southeast-1`.
- [ ] **Thao tác 5**: Cập nhật mã nguồn Python tích hợp AWS SDK Boto3 để đọc/ghi trực tiếp tới S3, DynamoDB và SSM Parameter Store.
- [ ] **Thao tác 6**: Thu thập ảnh minh chứng AWS Console có viền đỏ bao quanh Account Badge `huylam (677994024390)`.

### Giai đoạn 5: Tích hợp Đám mây Đầu - Cuối & Đo kiểm Hiệu năng (Tuần 11) [DỰ KIẾN]
- [ ] Cấu hình cơ chế tự động hóa: S3 Event Notification kích hoạt Lambda hoặc đóng gói triển khai Docker Web Studio lên ECS Fargate.
- [ ] Triển khai giao diện Web Studio lên Amazon S3 Static Hosting + Amazon CloudFront CDN có HTTPS.
- [ ] Thực hiện đo kiểm hiệu năng thực tế (Benchmark):
  - [ ] Tốc độ bóc tách Fast-Path (mục tiêu 0.1s - 0.3s/trang).
  - [ ] Thời gian nhận diện OCR trang scan qua Kaggle GPU và Gemini Failover.
  - [ ] Thời gian dịch thuật và độ chính xác giữ nguyên cấu trúc Markdown bảng biểu.
  - [ ] Tốc độ kết xuất và kích thước tệp xuất bản DOCX và PDF in ấn.
- [ ] Đo kiểm tùy chọn phụ AWS Native AI (Amazon Bedrock / Textract) khi người dùng chủ động bật trong Cài đặt.
- [ ] Biên soạn tài liệu Worklog Tuần 11 song ngữ và đồng bộ lên website Hugo.

### Giai đoạn 6: Nghiệm thu, Kiểm toán FinOps & Bảo vệ Tốt nghiệp (Tuần 12) [DỰ KIẾN]
- [ ] Kiểm toán tài chính đám mây FinOps qua AWS Budgets / Cost Explorer: Chứng minh toàn bộ hạ tầng vận hành ở mức 0.00 USD trong suốt kỳ thực tập.
- [ ] Thực hiện quy trình Teardown an toàn hoặc duy trì các tài nguyên ở chế độ On-Demand không phát sinh chi phí.
- [ ] Chuẩn hóa toàn bộ nội dung hướng dẫn thực hành trong thư mục `workshop/content/5-Workshop/`.
- [ ] Xây dựng kịch bản và quay video clip demo hoàn chỉnh (từ upload tệp -> bóc tách Fast-Path/OCR -> dịch thuật đa ngôn ngữ -> tải tệp kết quả -> kiểm tra dữ liệu trên AWS S3 và DynamoDB).
- [ ] Hoàn thành Báo cáo Thực tập Tốt nghiệp (Final Internship Report) và Slide thuyết trình bảo vệ đề tài.

---

## 3. Quy Tắc Bất Biến Khi Làm Việc Trong Thư Mục Này

1. **Tuyệt đối không dùng Emoji / Icon**: Không sử dụng bất kỳ biểu tượng cảm xúc, icon hay ký tự trang trí Unicode nào trong mã nguồn, văn bản, commit message, báo cáo hay lời thoại.
2. **Ngôn ngữ chuẩn mực**: Toàn bộ trao đổi và tài liệu tiếng Việt phải sử dụng tiếng Việt có dấu đầy đủ, chuẩn chính tả và văn phong kỹ thuật rõ ràng.
3. **Liên kết tệp**: Luôn sử dụng cú pháp clickable link `file://` cho mọi tệp cục bộ.
4. **Kỷ luật tài chính FinOps**: Mọi thiết kế và tài nguyên triển khai trên AWS phải tuân thủ nghiêm ngặt hạn mức AWS Free Tier, đảm bảo chi phí phát sinh là 0 USD.
5. **Không lan man ngoài phạm vi**: Tập trung 100% vào chu trình **Bóc tách OCR + Dịch thuật kỹ thuật + Xuất bản đa định dạng**. Không gợi ý hay bổ sung chatbot/RAG.
