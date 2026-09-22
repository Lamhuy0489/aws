import json
import os
import logging
from typing import Optional, Literal
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class AppSettings(BaseModel):
    """Cấu hình toàn hệ thống cho Hybrid Document OCR Platform."""
    ocr_mode: Literal["HYBRID_KAGGLE", "STANDALONE", "LOCAL_MOCK"] = Field(
        default="HYBRID_KAGGLE",
        description="Chế độ chạy: HYBRID_KAGGLE (Kaggle GPU/TPU), STANDALONE (Gemini API), hoặc LOCAL_MOCK (Kiểm thử giao diện cục bộ)"
    )
    fast_path_enabled: bool = Field(
        default=True,
        description="Kích hoạt Tầng 1: Bóc tách trực tiếp luồng văn bản số của PDF"
    )
    scan_threshold_chars: int = Field(
        default=50,
        description="Ngưỡng ký tự tối thiểu: Nếu trang có ít hơn số ký tự này thì phân loại là trang scan"
    )
    kaggle_endpoint: Optional[str] = Field(
        default="",
        description="URL Cloudflare Tunnel hoặc ngrok trỏ đến máy chủ OCR trên Kaggle"
    )
    gemini_api_key: Optional[str] = Field(
        default="",
        description="Google Gemini API Key dùng cho chế độ dự phòng (Failover)"
    )
    gemini_model: str = Field(
        default="gemini-flash-lite-latest",
        description="Tên mô hình Gemini dùng để OCR ảnh"
    )
    aws_region: str = Field(
        default="ap-southeast-1",
        description="Vùng AWS mặc định"
    )
    s3_bucket: str = Field(
        default="hybrid-ocr-documents",
        description="Tên bucket S3 lưu trữ tài liệu"
    )
    dynamodb_table: str = Field(
        default="document_processing_jobs",
        description="Tên bảng DynamoDB lưu trữ tiến trình"
    )
    timeout_seconds: int = Field(
        default=120,
        description="Thời gian chờ tối đa cho các cuộc gọi API ngoại vi"
    )

def load_settings_from_ssm(parameter_name: str = "/hybrid_ocr/config", region: str = "ap-southeast-1") -> Optional[dict]:
    """Tải chuỗi cấu hình JSON từ AWS Systems Manager Parameter Store."""
    try:
        import boto3
        ssm = boto3.client("ssm", region_name=region)
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        raw_val = response["Parameter"]["Value"]
        return json.loads(raw_val)
    except Exception as e:
        logger.info(f"Không thể đọc cấu hình từ SSM Parameter Store ({str(e)}). Sử dụng biến môi trường.")
        return None

def get_settings() -> AppSettings:
    """Khởi tạo cấu hình hệ thống kết hợp giữa SSM Parameter Store và biến môi trường."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass
    region = os.getenv("AWS_REGION", "ap-southeast-1")
    ssm_config = load_settings_from_ssm(region=region)
    
    config_dict = {}
    if ssm_config:
        config_dict.update(ssm_config)
    
    # Biến môi trường có quyền ghi đè
    env_mappings = {
        "OCR_MODE": "ocr_mode",
        "FAST_PATH_ENABLED": "fast_path_enabled",
        "SCAN_THRESHOLD_CHARS": "scan_threshold_chars",
        "KAGGLE_ENDPOINT": "kaggle_endpoint",
        "GEMINI_API_KEY": "gemini_api_key",
        "GEMINI_MODEL": "gemini_model",
        "AWS_REGION": "aws_region",
        "S3_BUCKET": "s3_bucket",
        "DYNAMODB_TABLE": "dynamodb_table",
        "TIMEOUT_SECONDS": "timeout_seconds"
    }
    
    for env_k, cfg_k in env_mappings.items():
        val = os.getenv(env_k)
        if val is not None:
            if cfg_k == "fast_path_enabled":
                config_dict[cfg_k] = val.lower() in ("true", "1", "yes")
            elif cfg_k in ("scan_threshold_chars", "timeout_seconds"):
                config_dict[cfg_k] = int(val)
            else:
                config_dict[cfg_k] = val
                
    return AppSettings(**config_dict)
