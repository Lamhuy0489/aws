# Đặc Tả Kỹ Thuật: Hệ Thống Bóc Tách & OCR Tài Liệu Lai Phi Máy Chủ Trên AWS
## (Serverless Hybrid Document OCR & Parsing Platform)

Tài liệu này mô tả chi tiết thiết kế kiến trúc, nguyên lý hoạt động, và quy trình triển khai của hệ thống **Serverless Hybrid Document OCR & Parsing Platform** trên nền tảng đám mây AWS kết hợp môi trường điện toán ngoài (Kaggle TPU/GPU).

---

## 1. Tổng quan bài toán và Mục tiêu

Trong các quy trình nghiệp vụ doanh nghiệp (kế toán, tài chính, bảo hiểm, pháp lý), việc số hóa khối lượng lớn tài liệu (hợp đồng, hóa đơn, báo cáo tài chính dạng PDF hoặc ảnh chụp) gặp hai thách thức lớn:
1. **Hạn chế của OCR truyền thống**: Chỉ bóc tách văn bản thô dạng phẳng (flat text), làm vỡ bảng biểu, mất thứ tự đọc của văn bản nhiều cột, và đánh mất hoàn toàn các định dạng ngữ nghĩa (tiêu đề, danh sách).
2. **Chi phí và hiệu năng khi lạm dụng mô hình Vision AI nặng**: Nếu gửi toàn bộ tài liệu 50-100 trang vào các mô hình thị giác máy tính nặng (như Qwen2.5-VL hoặc OCR thương mại), hệ thống sẽ rất chậm và tốn kém chi phí tính toán không cần thiết, trong khi thực tế 80-90% các trang tài liệu văn phòng đã có sẵn luồng văn bản số (digital text stream).

**Mục tiêu của giải pháp**:
- **Tối ưu tốc độ và chi phí bằng cơ chế xử lý hai tầng (Two-Stage Hybrid Parsing)**:
  - *Tầng 1 (Fast-Path)*: Bóc tách trực tiếp luồng văn bản số, font chữ và tái lập bảng biểu trong 0.1 - 0.3 giây/trang ngay trên AWS Lambda với chi phí 0 USD.
  - *Tầng 2 (Slow-Path / Selective OCR)*: Chỉ kích hoạt mô hình thị giác AI nặng cho các trang là ảnh scan hoặc chứa bảng biểu phức tạp.
- **Hỗ trợ hai chế độ linh hoạt (Dual-Mode)**:
  - *Chế độ Kaggle Accelerated*: Chuyển tiếp các trang scan sang Kaggle TPU/GPU qua Cloudflare Tunnel để chạy mô hình AI mã nguồn mở miễn phí.
  - *Chế độ Standalone Fallback*: Tự động chuyển tiếp sang Google Gemini 1.5 Flash Vision API khi Kaggle offline, đảm bảo hệ thống trên AWS hoạt động liên tục 24/7.
- **Đầu ra đa định dạng**: Giữ nguyên bố cục bảng biểu và cấu trúc phân cấp, xuất ra định dạng Markdown (`.md`), Microsoft Word (`.docx`), và PDF tìm kiếm được.

---

## 2. Sơ đồ kiến trúc tổng thể trên AWS (Solution Architecture)

```text
[ Người Dùng / Trình Duyệt ]
            │
            ▼ HTTPS (SSL/TLS)
[ Amazon CloudFront + Amazon S3 ] (Hosting Dashboard Quản Lý & Xem Kết Quả)
            │
            ▼ REST API Request (Xin Presigned URL hoặc Tải Kết Quả)
[ Amazon API Gateway ]
            │
            ├──> 1. Trả về S3 Presigned URL cho Client
            │
[ Amazon S3 Bucket ]
      │
      ├── /uploads/ (File PDF / Ảnh gốc tải lên trực tiếp)
      │      │
      │      ▼ (Sự kiện s3:ObjectCreated tự động kích hoạt)
      ▼
[ AWS Lambda: Hybrid Document Engine ]
      │
      ├── 2. Đọc cấu hình chế độ & Keys ──> [ AWS SSM Parameter Store ]
      │                                       (Lưu URL Kaggle, API Keys mã hóa)
      │
      ├── 3. Thực thi Tầng 1 (Fast-Path):
      │      - Bóc tách văn bản số & bảng bằng PyMuPDF
      │      - Đánh giá mật độ text để phân loại trang scan
      │
      ├── 4. Thực thi Tầng 2 (Selective OCR cho trang scan):
      │      ├── [Nhánh chính: Kaggle GPU/TPU qua Cloudflare Tunnel] (Qwen2.5-VL / GOT-OCR)
      │      └── [Nhánh dự phòng: Gemini 1.5 Flash Vision API] (Tự động kích hoạt khi lỗi)
      │
      ├── 5. Ghép nối và xuất đa định dạng ─> [ Amazon S3: /outputs/ ]
      │                                       (.md, .docx, .pdf)
      │
      └── 6. Ghi nhận nhật ký & siêu dữ liệu ─> [ Amazon DynamoDB (document_jobs) ]
                                                [ Amazon CloudWatch (Logs & Metrics) ]
```

---

## 3. Chi tiết các thành phần kỹ thuật

### a. Tầng 1: Phân tích cấu trúc gốc (Fast-Path Native Parsing)
- **Công nghệ thực thi**: `PyMuPDF` kết hợp bộ phân tích bố cục (Layout Analyzer).
- **Nguyên lý hoạt động**:
  - Đọc trực tiếp bảng cây phân cấp của tệp PDF (DOM-like tree).
  - Trích xuất các khối văn bản (blocks), dòng (lines), tọa độ chữ (spans), kích thước phông chữ để suy diễn tiêu đề (h1, h2, h3) và đoạn văn.
  - Nhận diện các đường kẻ ngang/dọc để tái lập bảng biểu thành định dạng Markdown Table (`| Cột 1 | Cột 2 |`).
  - **Tiêu chí phân loại trang scan**: Nếu số lượng ký tự số trích xuất được dưới ngưỡng (threshold < 50 ký tự) hoặc diện tích ảnh chiếm trên 85% diện tích trang, trang đó được đánh dấu là `IS_SCANNED = True` và chuyển sang Tầng 2.

### b. Tầng 2: OCR thị giác chọn lọc (Selective Vision OCR)
- **Trình điều phối (OCR Dispatcher)**:
  - Chỉ gửi các trang được đánh dấu là ảnh scan sang mô hình thị giác máy tính.
  - Chuẩn hóa ảnh trang thành định dạng JPEG nén Base64.
- **Kết nối ngoại vi**:
  - Gửi request kèm prompt chuyên dụng trích xuất Markdown tới Kaggle Cloudflare Tunnel API.
  - Nếu kết nối thất bại hoặc vượt quá thời gian chờ (timeout > 15s), hệ thống tự động chuyển tiếp sang Gemini 1.5 Flash Vision.

### c. Tầng Bảo mật & Quản lý cấu hình (Security & SSM)
- Tham số cấu hình đặt tại `/hybrid_ocr/config` trong **AWS Systems Manager Parameter Store**:
  ```json
  {
    "mode": "HYBRID_KAGGLE",
    "fast_path_enabled": true,
    "scan_threshold_chars": 50,
    "kaggle_endpoint": "https://xyz.trycloudflare.com/v1/ocr",
    "gemini_api_key": "AIzaSy...",
    "supported_exports": ["md", "docx"]
  }
  ```
- Toàn bộ quyền truy cập tuân thủ nguyên tắc quyền tối thiểu (IAM Least Privilege).

### d. Tầng Lưu trữ & Dữ liệu (Storage & Database)
- **Amazon S3**:
  - `uploads/{job_id}/{filename}`: Tệp gốc được tải lên trực tiếp qua Presigned URL.
  - `outputs/{job_id}/{filename}.md`: Tệp Markdown kết quả.
  - `outputs/{job_id}/{filename}.docx`: Tệp Microsoft Word kết quả.
- **Amazon DynamoDB** (Bảng `document_processing_jobs`):
  - Khóa chính: `job_id` (String).
  - Thuộc tính: `filename`, `total_pages`, `digital_pages`, `scanned_pages`, `status`, `processing_time_seconds`, `created_at`.

---

## 4. Phân tích chi phí (FinOps)

Toàn bộ hệ thống được thiết kế để chi phí vận hành bằng **0 USD**:
- **AWS Lambda**: Nằm trong hạn mức 1,000,000 request/tháng và 3,200,000 giây tính toán miễn phí.
- **Amazon S3**: Hạn mức 5 GB lưu trữ tiêu chuẩn miễn phí trong 12 tháng đầu.
- **Amazon DynamoDB**: Hạn mức 25 GB lưu trữ miễn phí vĩnh viễn.
- **Amazon API Gateway**: 1,000,000 lượt gọi API miễn phí trong 12 tháng đầu.
- **Kaggle GPU/TPU**: 30 giờ GPU T4/P100 và 20 giờ TPU v5e miễn phí mỗi tuần.
- **Gemini 1.5 Flash API**: Gói Free Tier hỗ trợ 15 request/phút.

---

## 5. Kế hoạch xác minh và tiêu chuẩn chất lượng

1. **Kiểm thử đơn vị (Unit Testing)**:
   - Kiểm tra khả năng nhận diện trang PDF số so với trang ảnh scan.
   - Kiểm tra tính chính xác của bảng biểu Markdown được tạo ra.
   - Kiểm tra khả năng xuất tệp sang định dạng `.docx` không bị lỗi font tiếng Việt.
2. **Kiểm thử tích hợp (Integration Testing)**:
   - Kiểm thử chuyển đổi dự phòng tự động khi Kaggle endpoint bị ngắt kết nối.
