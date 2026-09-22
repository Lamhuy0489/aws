import os
import sys
import time
import json
import re
import urllib.request
from kaggle.api.kaggle_api_extended import KaggleApi

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def main():
    kernel_slug = "lamhuy8904/qwen2-5-vl-ocr-server"
    log(f"Bắt đầu theo dõi máy chủ Kaggle: {kernel_slug}")
    
    api = KaggleApi()
    api.authenticate()
    
    url_found = None
    start_time = time.time()
    max_wait = 900  # 15 phút
    
    while time.time() - start_time < max_wait:
        # 1. Kiểm tra trạng thái kernel
        try:
            status_obj = api.kernels_status(kernel_slug)
            status = getattr(status_obj, "status", str(status_obj))
            log(f"Trạng thái máy ảo: {status}")
            
            if "error" in str(status).lower():
                log("CẢNH BÁO: Máy ảo báo trạng thái ERROR! Đang đọc log chi tiết...")
        except Exception as e:
            log(f"Lỗi khi kiểm tra status: {e}")

        # 2. Đọc logs
        try:
            raw_logs = api.kernels_logs(kernel_slug)
            if raw_logs:
                entries = json.loads(raw_logs)
                all_text = " ".join([e.get("data", "") for e in entries])
                
                # Tìm domain trycloudflare.com
                match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", all_text)
                if match:
                    url_found = match.group(0)
                    log("=" * 60)
                    log(f"ĐÃ TÌM THẤY ENDPOINT CLOUDFLARE: {url_found}")
                    log("=" * 60)
                    break
                else:
                    # In log gần nhất
                    recent = [e.get("data", "").strip() for e in entries[-5:] if e.get("data", "").strip()]
                    if recent:
                        log(f"Log gần nhất: {recent[-1][:120]}")
            else:
                log("Đang phân bổ GPU và tải trọng số vào container...")
        except Exception as e:
            log(f"Đang chờ dữ liệu log: {e}")

        time.sleep(15)

    if not url_found:
        log("Hết thời gian chờ mà chưa bắt được URL Cloudflare.")
        return False

    # 3. Kiểm tra kiểm thử kết nối /health
    endpoint_ocr = f"{url_found}/ocr"
    endpoint_health = f"{url_found}/health"
    log(f"Đang kiểm tra kết nối đến {endpoint_health}...")
    
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(endpoint_health, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = resp.read().decode("utf-8")
            log(f"Phản hồi từ server OCR: {data}")
    except Exception as e:
        log(f"Kiểm thử kết nối ban đầu: {e} (Có thể do server đang warmup)")

    # 4. Lưu cấu hình vào file .env để Web App tự động sử dụng
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    env_path = os.path.join(project_root, ".env")
    with open(env_path, "w") as f:
        f.write(f"KAGGLE_ENDPOINT={endpoint_ocr}\n")
        f.write("OCR_MODE=HYBRID_KAGGLE\n")
    log(f"Đã tự động cập nhật KAGGLE_ENDPOINT={endpoint_ocr} vào {env_path}")
    log("HỆ THỐNG ĐÃ KẾT NỐI VÀ SẴN SÀNG SỬ DỤNG!")
    return True

if __name__ == "__main__":
    main()
