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

### Giai đoạn 4: Triển khai Hạ tầng Đám mây AWS (Tuần 10) [HOÀN THÀNH 100%]
- [x] Soạn thảo hướng dẫn thiết lập bằng tay từng bước (Manual Step-by-Step Setup Guide) trên AWS Management Console.
- [x] Cập nhật Đề xuất dự án Proposal bám sát tính năng OCR, Dịch thuật và tùy chọn mở rộng AWS Native AI.
- [x] Biên soạn Worklog Tuần 10 song ngữ trên website Hugo và đồng bộ lên GitHub `workshop`.
- [x] **Thao tác 1**: Thiết lập kho lưu trữ Amazon S3 Bucket `huylam-ocr-documents-ap-southeast-1` trên Region `ap-southeast-1`:
  - [x] Đã tạo S3 Bucket `huylam-ocr-documents-ap-southeast-1` (Block all public access = ON).
  - [x] Đã tạo thư mục `uploads/` (nhận tệp gốc).
  - [x] Đã tạo thư mục `outputs/` (lưu kết quả MD, DOCX, PDF).
  - [x] Đã cấu hình chính sách CORS cho phép các phương thức `GET`, `PUT`, `POST`, `HEAD`.
- [x] **Thao tác 2**: Tạo bảng cơ sở dữ liệu Amazon DynamoDB `document_processing_jobs` trên Region `ap-southeast-1`:
  - [x] Partition Key: `job_id` (String).
  - [x] Sort Key: `created_at` (String).
  - [x] Capacity Mode: On-Demand (`PAY_PER_REQUEST`).
  - [x] Bảng ở trạng thái Active (ARN: `arn:aws:dynamodb:ap-southeast-1:677994024390:table/document_processing_jobs`).
- [x] **Thao tác 3**: Tạo tham số bảo mật trên AWS Systems Manager Parameter Store:
  - [x] Name: `/huylam-ocr/config`.
  - [x] Type: `SecureString` (KMS Key: `alias/aws/ssm`).
  - [x] Value: Cấu hình JSON chứa `ocr_mode`, `scan_threshold_chars`, `kaggle_endpoint`, `gemini_api_key`, `aws_native_mode_enabled: false`.
  - [x] ARN: `arn:aws:ssm:ap-southeast-1:677994024390:parameter/huylam-ocr/config`.
- [x] **Thao tác 4 (Tùy chọn)**: Đo kiểm cơ chế Amazon Bedrock Model Access & Phân tích chính sách tài khoản:
  - [x] Kiểm tra danh mục mô hình nội bộ AWS (Amazon Nova Micro/Lite/Pro) trong Model Catalog.
  - [x] Đo kiểm thực tế trong Playground và ghi nhận chính sách hạn chế Runtime (`ValidationException: Operation not allowed`) của AWS đối với tài khoản mới/Free Tier.
  - [x] Thu thập ảnh chụp màn hình chi tiết Nova Micro và ảnh lỗi Playground làm minh chứng kỹ thuật cho báo cáo thực tập.
- [x] **Thao tác 5**: Cập nhật mã nguồn Python tích hợp AWS SDK Boto3 để đọc/ghi trực tiếp tới S3, DynamoDB và SSM Parameter Store:
  - [x] Đã đo kiểm xác thực danh tính `dev_admin` trên tài khoản `677994024390`.
  - [x] Đã tự tay chạy script Boto3 đọc và giải mã thành công cấu hình JSON từ SSM Parameter Store `/huylam-ocr/config`.
  - [x] Đã tự tay chạy script Boto3 ghi và đọc tệp thử nghiệm trên S3 Bucket `huylam-ocr-documents-ap-southeast-1`.
  - [x] Đã tự tay chạy script Boto3 ghi và đọc bản ghi tiến trình (`job-manual-test-01`) trên bảng DynamoDB `document_processing_jobs`.
- [x] **Thao tác 6**: Thu thập ảnh minh chứng AWS Console có viền đỏ bao quanh Account Badge `huylam (677994024390)`:
  - [x] Đã hoàn thành thu thập và đóng khung đỏ cho toàn bộ 9 ảnh minh chứng thực tế trên AWS Console.
  - [x] Nhúng toàn bộ 9 ảnh minh chứng vào Worklog Tuần 10 song ngữ và biên dịch Hugo 215 trang không lỗi.

### Giai đoạn 5: Tích hợp Đám mây Đầu - Cuối & Đo kiểm Hiệu năng (Tuần 11)
- [x] Đóng gói container hóa Web Studio: Xây dựng chuẩn mực Dockerfile (nền Python 3.11-slim) và .dockerignore tối ưu hóa cho Amazon ECR / ECS Fargate.
- [x] Cấu hình cơ chế tự động hóa Serverless hướng sự kiện: S3 Event Notification kích hoạt Lambda (`huylam-ocr-processor`) khi có tệp mới trong S3 `uploads/`, ghi nhận tiến trình vào DynamoDB `document_processing_jobs` (`RECEIVED_VIA_S3_EVENT`) và giám sát qua CloudWatch Logs (thời gian thực thi 214 ms, bộ nhớ 88 MB).
- [x] Thực hiện đo kiểm hiệu năng thực tế (Benchmark):
  - [x] Tốc độ bóc tách Fast-Path (đạt 0.31s trên `cv.pdf` và 3.07s trên bài báo 11 trang, ~0.28s/trang).
  - [x] Thời gian nhận diện OCR trang scan qua Kaggle GPU và Gemini Failover (đạt 2.54s - 6.99s).
  - [x] Thời gian dịch thuật và độ chính xác giữ nguyên cấu trúc Markdown bảng biểu (hoàn tất chuyển ngữ `cv.pdf` đạt 3.480 ký tự).
  - [x] Tốc độ kết xuất và kích thước tệp xuất bản DOCX và PDF in ấn (tệp `cv.pdf.docx` 38.2 KB mở chuẩn trên Microsoft Word macOS).
- [x] Tích hợp và đo kiểm tùy chọn độc lập AWS Native AI (Amazon Bedrock / Nova) trực tiếp trên Web Studio (không chạy song song).
- [x] Biên soạn tài liệu Worklog Tuần 11 song ngữ kèm bộ 15 ảnh minh chứng viền đỏ chuẩn xác và đồng bộ lên website Hugo (215 trang).

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
