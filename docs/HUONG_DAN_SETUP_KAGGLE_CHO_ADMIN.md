# Cẩm Nang Quản Trị Viên: Hướng Dẫn Thiết Lập & Sử Dụng Kaggle GPU OCR Server

Tài liệu này hướng dẫn chi tiết dành cho Quản trị viên (Admin) của nền tảng **Serverless Hybrid Document OCR, Parsing & Technical Translation Platform** nhằm thiết lập, vận hành máy chủ bóc tách thị giác AI (Vision OCR) trên nền tảng Kaggle GPU hoàn toàn miễn phí và kết nối trực tiếp với Web Studio thông qua Cloudflare Tunnel.

---

## 1. Tổng quan Kiến trúc Tích hợp Ngoại vi

Trong kiến trúc **Two-Stage Hybrid Parsing Engine** của dự án:
- **Tầng 1 (Fast-Path)**: Chạy trực tiếp trên máy chủ AWS EC2 bằng thư viện `PyMuPDF` (chi phí 0.00 USD, độ trễ 0.1s - 0.3s/trang).
- **Tầng 2 (Selective Vision OCR)**: Được kích hoạt khi gặp các trang là ảnh chụp, tài liệu scan hoặc biểu mẫu phức tạp. Hệ thống sử dụng mô hình thị giác đa phương thức lớn **Qwen2.5-VL-7B-Instruct** vận hành trên hạ tầng GPU miễn phí của Kaggle (NVIDIA Tesla T4 x 2 hoặc P100 với 16 GB VRAM) và kết nối an toàn với máy chủ AWS qua **Cloudflare Tunnel** (HTTPS).

```text
  [ Người Dùng Web Studio ]
              │
              ▼
  [ AWS Application Load Balancer / EC2 ]
              │
              ├── (Trang văn bản số) ──► [ Tầng 1: Fast-Path PyMuPDF (0.1s) ]
              │
              └── (Trang ảnh scan)   ──► [ Tầng 2: OCR Dispatcher ]
                                                  │
                                                  ▼ (Cloudflare Tunnel HTTPS)
                                       ┌────────────────────────────────────┐
                                       │   Kaggle GPU OCR Server (FastAPI)  │
                                       │   Model: Qwen2.5-VL-7B-Instruct    │
                                       │   GPU: NVIDIA T4 x 2 / P100        │
                                       └────────────────────────────────────┘
```

---

## 2. Quy Trình 5 Bước Thiết Lập và Vận Hành

### Bước 1: Mở Notebook trên Kaggle
1. Đăng nhập vào tài khoản Kaggle của bạn.
2. Mở trực tiếp Notebook chính thức của dự án:
   - **Đường link Kaggle Notebook**: [https://www.kaggle.com/code/lamhuy8904/qwen2-5-vl-ocr-server](https://www.kaggle.com/code/lamhuy8904/qwen2-5-vl-ocr-server)
   *(Hoặc tải tệp [qwen_ocr_server.ipynb](file:///Users/huylam/Downloads/aws/src/kaggle/qwen_ocr_server.ipynb) trong thư mục `src/kaggle/` và tải lên Kaggle dưới dạng New Notebook).*

---

### Bước 2: Cấu hình Môi trường GPU & Internet
Tại giao diện Kaggle Notebook, nhìn sang bảng điều khiển bên phải (**Session options**):
1. **Accelerator**: Chọn **GPU T4 x 2** (hoặc **GPU P100**).
2. **Language**: Python.
3. **Environment**: Always use latest environment.
4. **Internet**: Chuyển công tắc sang **Internet on** (Bắt buộc phải bật để Kaggle có thể tải thư viện và mở kết nối Cloudflare Tunnel ra Internet).

---

### Bước 3: Khởi chạy Máy chủ (Run All)
1. Nhấp vào nút **Run All** trên thanh công cụ phía trên (hoặc nhấn phím tắt `Ctrl + F9`).
2. Quá trình thực thi diễn ra tuần tự:
   - **Cell 1**: Cài đặt các gói thư viện phụ thuộc (`transformers>=4.49.0`, `accelerate`, `qwen-vl-utils`, `pycloudflared`, `fastapi`, `uvicorn`).
   - **Cell 2 & 3**: Kiểm tra thông số GPU và nạp trọng số mô hình `Qwen2.5-VL-7B-Instruct` vào VRAM GPU.
   - **Cell 4**: Khởi tạo ứng dụng FastAPI với endpoint `/ocr` và `/health`.
   - **Cell 5**: Khởi chạy binary `cloudflared` tạo đường hầm HTTPS ra ngoài Internet và khởi chạy Uvicorn server trên cổng nội bộ 8000.

---

### Bước 4: Tìm Log và Sao chép Link Tunnel
1. Cuộn màn hình xuống ô chạy cuối cùng (Cell 5).
2. Quan sát phần đầu ra (Output Log), tìm khối văn bản thông báo:
   ```text
   ======================================================================
   MAY CHU KAGGLE OCR DA SAN SANG HOAT DONG!
   URL Endpoint: https://random-subdomain.trycloudflare.com/ocr
   URL Health:   https://random-subdomain.trycloudflare.com/health
   ======================================================================
   Sao chep URL Endpoint tren va dan vao trang Admin / Settings!
   ```
3. Sao chép chuỗi URL:
   - Ví dụ: `https://random-subdomain.trycloudflare.com/ocr` (hoặc `https://random-subdomain.trycloudflare.com`).
   - *Lưu ý*: Bạn có thể kiểm tra nhanh trạng thái máy chủ bằng cách mở link `https://random-subdomain.trycloudflare.com/health` trên trình duyệt, kết quả hiển thị `{"status": "healthy", "device": "cuda"}` là hoàn tất.

---

### Bước 5: Dán Link vào Web Studio và Kích hoạt
1. Mở trình duyệt và truy cập Web Studio:
   ```text
   http://huylam-ocr-alb-1284818160.ap-southeast-1.elb.amazonaws.com
   ```
2. Đăng nhập bằng tài khoản Quản trị viên (**Admin**).
3. Nhấp vào thanh điều hướng: **Quản Trị Hệ Thống** (`/admin`).
4. Tại khu vực **Hướng Dẫn Kết Nối Kaggle GPU OCR Server**, nhấp nút **Nhập Endpoint Kaggle** (hoặc bấm **Thêm Khóa API Mới**):
   - **Nhà cung cấp (Provider)**: Chọn `Kaggle TPU/GPU (Qwen2.5-VL / Cloudflare Tunnel)`.
   - **Tên gợi nhớ (Alias)**: Nhập tên mô tả (ví dụ: `Kaggle GPU Qwen2.5-VL Slot 1`).
   - **Giá trị API Key / Endpoint URL**: Dán link URL vừa sao chép ở Bước 4 vào ô này.
   - **Tên mô hình (Model Name)**: Điền `Qwen2.5-VL-7B`.
   - **Độ ưu tiên (Priority)**: Đặt là `1` (ưu tiên cao nhất để tận dụng GPU miễn phí).
5. Nhấp nút **Lưu Khóa API**.
6. Hệ thống hiển thị thông báo thành công và khóa mới xuất hiện trong bảng **Cụm Khóa Kết Nối API (Key Tour)** ở trạng thái `ACTIVE`.

---

## 3. Hướng Dẫn Cách Dùng Trên Giao Diện Web Studio

Sau khi Admin đã nhập Endpoint Kaggle thành công, tất cả người dùng trong hệ thống có thể sử dụng sức mạnh của Kaggle GPU OCR như sau:

1. **Truy cập Trang Studio Chính (`/studio`)**:
   - Nhấp vào mục **Studio Bóc Tách** trên thanh điều hướng.
2. **Lựa chọn Mô hình AI (`#modelChoice`)**:
   - **Chế độ 1: Auto Hybrid Engine (Khuyến nghị)**: Hệ thống tự động phân loại. Trang văn bản số sẽ chạy Fast-Path (0.1s), trang ảnh scan sẽ tự động gửi sang Kaggle GPU OCR.
   - **Chế độ 2: Kaggle TPU/GPU (Qwen2.5-VL qua Cloudflare)**: Cưỡng bức gửi toàn bộ các trang tài liệu sang máy chủ Kaggle để bóc tách thị giác sâu.
3. **Tải tài liệu lên**:
   - Kéo thả tệp PDF (hợp đồng scan, hồ sơ thầu, bảng vẽ, bài báo khoa học) hoặc ảnh tài liệu vào khung thả tệp.
4. **Bắt đầu xử lý**:
   - Nhấn **Bắt đầu bóc tách & Dịch thuật**.
   - Máy chủ EC2 sẽ đọc cấu hình từ Key Tour, gửi payload ảnh qua Cloudflare Tunnel tới Kaggle GPU.
   - Mô hình `Qwen2.5-VL` bóc tách chính xác toàn bộ bảng biểu thành cú pháp `| Cột 1 | Cột 2 |`, bảo toàn tiêu đề phân cấp và thứ tự đọc.
5. **Xem và Xuất bản kết quả**:
   - Màn hình Split-view hiển thị tài liệu gốc bên trái và văn bản Markdown/bản dịch bên phải.
   - Người dùng có thể chỉnh sửa trực tiếp hoặc xuất bản ra tệp Microsoft Word (`.docx`), Markdown (`.md`) hoặc PDF.

---

## 4. Cơ Chế Tự Phục Hồi & Xử Lý Sự Cố (Troubleshooting & Failover)

1. **Hết phiên làm việc của Kaggle (Session Timeout)**:
   - Kaggle Notebook thông thường tự ngắt sau 9 - 12 giờ chạy liên tục hoặc sau 40 phút không có thao tác (Idle).
   - Khi đó, Cloudflare Tunnel sẽ bị đóng.
2. **Cơ chế Failover tự động**:
   - Trong mã nguồn `src/backend/parsers/ocr_dispatcher.py`, hệ thống đã được lập trình cơ chế bảo vệ kép: Nếu Kaggle Endpoint phản hồi quá 5 giây (Timeout) hoặc báo lỗi mất kết nối, hệ thống sẽ **tự động chuyển đổi dự phòng (Failover) sang Google Gemini Flash** để tài liệu của người dùng không bị gián đoạn.
3. **Cách khắc phục khi Kaggle dừng**:
   - Admin chỉ cần mở lại link notebook trên Kaggle, bấm **Run All**, lấy link Tunnel mới và cập nhật lại vào ô Giá trị của Key trong trang `/admin`.
