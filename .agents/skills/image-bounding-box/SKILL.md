---
name: image-bounding-box
description: >-
  Locate UI elements, text, and badges accurately in screenshots using Apple Vision OCR and Computer Vision, draw precise red bounding boxes with padding, verify results visually, and export optimized proof images for AWS labs and worklogs.
---

# Image Bounding Box & Proof Annotation Skill

Kỹ năng chuyên biệt phục vụ việc nhận diện vị trí các thành phần giao diện (UI elements), định danh tài khoản, thông số kỹ thuật và tạo khung viền đỏ (red bounding boxes) chuẩn xác từng pixel trên các ảnh chụp màn hình minh chứng thực hành AWS.

---

## 1. Nguyên Tắc Cốt Lõi: Không Đoán Tọa Độ (Zero Hardcoded Guesswork)

Lý do các ảnh minh chứng trước đây thường bị lệch khung (như khoanh nhầm vào thanh tìm kiếm thay vì tiêu đề email, hoặc lệch bảng cấu hình) là do **sử dụng tọa độ ước lượng hoặc tọa độ cố định từ màn hình khác**.

Trên macOS và trình duyệt web:
- Độ phân giải hiển thị có thể thay đổi (màn hình Retina 2x scale: 2880x1800 vs màn hình ngoài 1920x1080).
- Người dùng có thể cuộn trang (scroll), mở rộng Sidebar hoặc co giãn cửa sổ.
- Bố cục trang web có thể thay đổi vị trí các card và widget.

**Quy tắc bắt buộc**: Không bao giờ gán cứng tọa độ `(x1, y1, x2, y2)` một cách cảm tính. Phải luôn sử dụng công cụ OCR của kỹ năng này để trích xuất vị trí thực tế của các khối văn bản trên ảnh gốc trước khi tiến hành vẽ khung.

---

## 2. Các Công Cụ Đi Kèm Trong Kỹ Năng

Kỹ năng cung cấp sẵn hai công cụ mạnh mẽ trong thư mục `scripts/`:

1. **`scripts/ocr.swift`**:
   - Sử dụng Apple Vision Framework nguyên bản trên macOS (`VNRecognizeTextRequest`).
   - Tốc độ cực nhanh (<1 giây), độ chính xác tuyệt đối, không phụ thuộc vào thư viện ngoài như Tesseract.
   - Xuất dữ liệu JSON từng dòng chứa tọa độ pixel chuẩn: `{"text": "...", "x": float, "y": float, "w": float, "h": float}`.

2. **`scripts/annotate.py`**:
   - Tự động gọi `ocr.swift` để đọc toàn bộ văn bản trên màn hình.
   - Tự động nhận diện **AWS Account Badge** (`huylam`, `677994024390`, `Singapore`) ở góc trên bên phải màn hình thông qua cờ `--badge`.
   - Tìm kiếm vị trí các từ khóa chỉ định thông qua cờ `--find "tu_khoa_1" "tu_khoa_2"`.
   - Tự động thêm khoảng đệm lề (padding) đẹp mắt (`pad_x=16`, `pad_y=10`).
   - Hỗ trợ thêm các hộp tùy chỉnh `--custom-box X1 Y1 X2 Y2` khi cần bao quanh toàn bộ card hoặc bảng dựa trên tọa độ neo tìm được.

---

## 3. Quy Trình 5 Bước Chuẩn Mực Khi Xử Lý Minh Chứng

Mỗi khi thu thập và xử lý ảnh chụp màn hình từ `~/Desktop` cho bài thực hành, agent PHẢI tuân thủ đúng 5 bước sau:

### Bước 1: Sao lưu ảnh gốc vào thư mục `originals/`
Không bao giờ vẽ đè trực tiếp lên file ảnh gốc duy nhất. Luôn tạo bản sao nguyên bản:
```bash
cp ~/Desktop/"Screen Shot ... .png" workshop/static/images/weekX/originals/<ten-anh>.png
```

### Bước 2: Quét tọa độ phần tử qua OCR
Chạy kiểm tra nhanh để nắm bắt bố cục và tọa độ các phần tử trọng yếu:
```bash
python3 .agent/skills/image-bounding-box/scripts/annotate.py \
  --image workshop/static/images/weekX/originals/<ten-anh>.png \
  --ocr-only
```
Hoặc grep từ khóa cụ thể:
```bash
python3 .agent/skills/image-bounding-box/scripts/annotate.py \
  --image workshop/static/images/weekX/originals/<ten-anh>.png \
  --ocr-only | grep -i "tu_khoa"
```

### Bước 3: Tính toán và vẽ khung viền đỏ
Sử dụng `annotate.py` để tạo ảnh có viền đỏ:
- **Tiêu chuẩn màu viền đỏ**: `RGB(239, 68, 68)` (Đỏ Tailwind 500 nổi bật, tương phản cao trên cả nền sáng và tối).
- **Độ dày đường viền (Line Width)**: `6px`.
- **Ví dụ lệnh vẽ**:
```bash
python3 .agent/skills/image-bounding-box/scripts/annotate.py \
  --image workshop/static/images/weekX/originals/<ten-anh>.png \
  --badge \
  --find "huylam-ssm-instance" "Online" \
  --out workshop/static/images/weekX/<ten-anh>.png
```
Nếu đối tượng cần khoanh là một bảng hoặc card lớn chứa từ khóa, lấy tọa độ `y` của từ khóa làm mốc trên, sau đó mở rộng `x1=40`, `x2=2830` và `y2` tương ứng với phần đuôi của bảng bằng cờ `--custom-box`.

### Bước 4: Kiểm chứng trực quan bằng `view_file` (BẮT BUỘC)
Sau khi tạo file ảnh kết quả, **BẮT BUỘC** gọi công cụ `view_file` với đường dẫn tuyệt đối của file ảnh vừa tạo.
- Quan sát kỹ:
  - Khung viền có bao trọn vẹn văn bản hay bị đè vào chữ?
  - Khung có bị lệch lên thanh địa chỉ/thanh tìm kiếm hay không?
  - Huy hiệu tài khoản (`huylam` / `677994024390`) đã được khoanh chuẩn chưa?
- Nếu phát hiện khung bị lệch: sửa lại tọa độ trong script và vẽ lại ngay lập tức.

### Bước 5: Đồng bộ xuất bản sang cả hai thư mục
Sau khi xác thực ảnh đạt chuẩn 100%, sao chép sang thư mục tài liệu lưu trữ:
```bash
cp workshop/static/images/weekX/<ten-anh>.png raw/images/weekX/<ten-anh>.png
```

---

## 4. Tiêu Chuẩn Trình Bày & Không Dùng Emoji

- Nghiêm cấm sử dụng bất kỳ biểu tượng cảm xúc (emoji), icon hay ký tự trang trí Unicode nào trong tên file, mã nguồn, thông điệp in ra terminal, hay trong các chú thích ảnh markdown.
- Luôn sử dụng tiếng Việt có dấu đầy đủ, chuẩn mực kỹ thuật trong các tài liệu và giải thích.
