"""
Kịch bản máy chủ phục vụ mô hình Vision OCR trên Kaggle GPU/TPU
Sử dụng FastAPI kết hợp Cloudflare Tunnel để xuất REST API công khai ra internet.
Chạy trực tiếp trong một cell của Kaggle Notebook.
"""

import os
import io
import base64
import subprocess
import threading
import time
from PIL import Image

# Cài đặt các thư viện cần thiết nếu chưa có trên Kaggle:
# !pip install -q fastapi uvicorn pycloudflared python-multipart transformers accelerate

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Kaggle Vision OCR Service")

class OCRRequest(BaseModel):
    image_base64: str
    prompt: str = "Trích xuất tài liệu này sang Markdown chuẩn giữ nguyên bảng biểu"

class OCRResponse(BaseModel):
    markdown: str
    inference_time_seconds: float

# Biến toàn cục lưu trữ mô hình
model = None
processor = None

def load_model():
    """Khởi tạo mô hình Qwen2.5-VL hoặc GOT-OCR trên GPU của Kaggle."""
    global model, processor
    try:
        import torch
        from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor

        model_id = "Qwen/Qwen2.5-VL-7B-Instruct"
        print(f"Đang tải mô hình {model_id} lên GPU...")
        
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto"
        )
        processor = AutoProcessor.from_pretrained(model_id)
        print("Tải mô hình thành công!")
    except Exception as e:
        print(f"Không thể tải mô hình với GPU ({e}). Khởi chạy ở chế độ Mock phục vụ kiểm thử kết nối.")

@app.on_event("startup")
def startup_event():
    load_model()

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

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
            inputs = processor(text=[text], images=[image], padding=True, return_tensors="pt")
            inputs = inputs.to("cuda")

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
        # Chế độ Mock phản hồi giả lập
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
    from pycloudflared import try_cloudflare
    
    print(f"Đang khởi tạo Cloudflare Tunnel trên cổng {port}...")
    tunnel = try_cloudflare(port=port)
    print("=" * 60)
    print(f"URL ENDPOINT CỦA BẠN: {tunnel.tunnel_url}/ocr")
    print("Hãy sao chép URL trên và dán vào cấu hình SSM Parameter Store của AWS!")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    run_tunnel_and_server()
