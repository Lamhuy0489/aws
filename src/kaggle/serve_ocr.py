"""
Kịch bản máy chủ phục vụ mô hình Vision OCR trên Kaggle GPU/TPU
Sử dụng FastAPI kết hợp Cloudflare Tunnel để xuất REST API công khai ra internet.
Chạy trực tiếp trong một cell của Kaggle Notebook hoặc chạy độc lập.
"""

import os
import io
import glob
import base64
import time
from PIL import Image
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from pycloudflared import try_cloudflare

app = FastAPI(title="Kaggle Qwen2.5-VL OCR Service")

class OCRRequest(BaseModel):
    image_base64: str
    prompt: str = (
        "Bạn là chuyên gia OCR tài liệu cao cấp. Hãy chuyển đổi hình ảnh tài liệu này "
        "thành định dạng Markdown chuẩn xác. Yêu cầu bắt buộc:\n"
        "1. Giữ nguyên 100% toàn bộ bảng biểu số liệu bằng định dạng Markdown Table (| Cột 1 | Cột 2 |).\n"
        "2. Giữ nguyên các cấp tiêu đề (#, ##, ###), danh sách liệt kê, và thứ tự đọc của văn bản nhiều cột.\n"
        "3. Bảo toàn chính xác toàn bộ chữ tiếng Việt có dấu và các ký tự đặc biệt.\n"
        "4. Tuyệt đối không thêm lời giải thích, lời chào hay bình luận; chỉ xuất duy nhất nội dung Markdown của tài liệu."
    )

class OCRResponse(BaseModel):
    markdown: str
    inference_time_seconds: float

# Biến toàn cục lưu trữ mô hình
model = None
processor = None

def load_model():
    """Khởi tạo mô hình Qwen2.5-VL trên GPU của Kaggle."""
    global model, processor
    try:
        from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor

        # Tự động tìm kiếm mô hình mount sẵn từ Kaggle Models / Datasets
        config_files = glob.glob("/kaggle/input/**/config.json", recursive=True)
        model_path = None
        for cfg in config_files:
            if any(k in cfg.lower() for k in ["qwen", "vl"]):
                model_path = os.path.dirname(cfg)
                break

        if not model_path:
            model_path = "Qwen/Qwen2.5-VL-7B-Instruct"
            print(f"Không tìm thấy trọng số trong /kaggle/input, tải từ Hugging Face: {model_path}")
        else:
            print(f"Phát hiện trọng số mô hình có sẵn tại: {model_path} (Tải 0s)")

        print(f"Đang tải mô hình {model_path} lên GPU...")
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        processor = AutoProcessor.from_pretrained(model_path)
        print("Tải mô hình thành công lên GPU!")
    except Exception as e:
        print(f"Không thể tải mô hình với GPU ({e}). Khởi chạy ở chế độ Mock phục vụ kiểm thử kết nối.")

@app.on_event("startup")
def startup_event():
    load_model()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "cuda_available": torch.cuda.is_available()
    }

@app.post("/ocr", response_model=OCRResponse)
def perform_ocr(req: OCRRequest):
    start_t = time.time()
    try:
        # Giải mã ảnh từ Base64
        image_data = base64.b64decode(req.image_base64)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Không thể giải mã hình ảnh: {str(e)}")

    if model is not None and processor is not None:
        try:
            from qwen_vl_utils import process_vision_info

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": req.prompt}
                    ]
                }
            ]
            text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            image_inputs, video_inputs = process_vision_info(messages)
            inputs = processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt"
            ).to("cuda")

            with torch.inference_mode():
                generated_ids = model.generate(**inputs, max_new_tokens=2048)
                generated_ids_trimmed = [
                    out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                ]
                output_text = processor.batch_decode(
                    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
                )[0]

            elapsed = round(time.time() - start_t, 2)
            return OCRResponse(markdown=output_text.strip(), inference_time_seconds=elapsed)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi suy luận: {str(e)}")
    else:
        # Chế độ Mock phản hồi giả lập nếu chưa có GPU
        elapsed = round(time.time() - start_t, 2)
        mock_md = (
            "## BẢNG KÊ CHI PHÍ DỊCH VỤ (MOCK OCR)\n\n"
            "| Hạng mục | Số lượng | Đơn giá | Thành tiền |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| Thuê Cloud Server EC2 | 2 | 500,000 | 1,000,000 |\n"
            "| Lưu trữ S3 Standard | 50 GB | 1,000 | 50,000 |\n\n"
            "**Tổng cộng thanh toán**: 1,050,000 VNĐ"
        )
        return OCRResponse(markdown=mock_md, inference_time_seconds=elapsed)

def run_tunnel_and_server(port: int = 8000):
    """Mở Cloudflare Tunnel và khởi chạy máy chủ FastAPI."""
    print(f"Đang khởi tạo Cloudflare Tunnel trên cổng {port}...")
    tunnel = try_cloudflare(port=port)
    tunnel_url = getattr(tunnel, "tunnel", str(tunnel))
    print("=" * 60)
    print(f"URL ENDPOINT CỦA BẠN: {tunnel_url}/ocr")
    print("Hãy sao chép URL trên và dán vào cấu hình SSM Parameter Store hoặc Cài Đặt!")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    run_tunnel_and_server()
