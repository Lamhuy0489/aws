import json
import os
import logging
from typing import Optional, Literal
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class AppSettings(BaseModel):
    """Cấu hình toàn hệ thống cho Hybrid Document OCR Platform."""
    ocr_mode: Literal["HYBRID_KAGGLE", "STANDALONE", "LOCAL_MOCK", "AWS_NATIVE"] = Field(
        default="HYBRID_KAGGLE",
        description="Chế độ chạy: HYBRID_KAGGLE (Kaggle GPU/TPU), STANDALONE (Gemini API), LOCAL_MOCK (Kiểm thử cục bộ), hoặc AWS_NATIVE (Amazon Bedrock/Nova)"
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
        default="huylam-ocr-documents-ap-southeast-1",
        description="Tên bucket S3 lưu trữ tài liệu"
    )
    dynamodb_table: str = Field(
        default="document_processing_jobs",
        description="Tên bảng DynamoDB lưu trữ tiến trình"
    )
    aws_native_mode_enabled: bool = Field(
        default=False,
        description="Bật chế độ khép kín với mô hình AWS Native Foundation Models (Amazon Nova / Bedrock)"
    )
    aws_bedrock_model: str = Field(
        default="amazon.nova-micro-v1:0",
        description="Mã định danh mô hình Bedrock (Amazon Nova Micro hoặc Claude 3.5 Haiku)"
    )
    ssm_parameter_name: str = Field(
        default="/huylam-ocr/config",
        description="Đường dẫn tham số cấu hình trên AWS SSM Parameter Store"
    )
    timeout_seconds: int = Field(
        default=120,
        description="Thời gian chờ tối đa cho các cuộc gọi API ngoại vi"
    )
    cognito_region: str = Field(
        default="ap-southeast-1",
        description="Vùng AWS Cognito"
    )
    cognito_user_pool_id: Optional[str] = Field(
        default="ap-southeast-1_dNJkc4IWG",
        description="Cognito User Pool ID"
    )
    cognito_app_client_id: Optional[str] = Field(
        default="25tat78efli48ghdg3t6d9cul1",
        description="Cognito App Client ID"
    )
    cognito_app_client_secret: Optional[str] = Field(
        default="smd2157sug894ccm0aojnu98u4umh7ba28kitl1i67j98ra5tjb",
        description="Cognito App Client Secret"
    )
    cognito_domain: Optional[str] = Field(
        default="https://ap-southeast-1dnjkc4iwg.auth.ap-southeast-1.amazoncognito.com",
        description="Cognito Hosted UI Domain"
    )
    cognito_redirect_uri: str = Field(
        default="https://hpyewvtaya.execute-api.ap-southeast-1.amazonaws.com/api/auth/cognito/callback",
        description="Cognito OAuth Redirect Callback URI"
    )

def load_settings_from_ssm(parameter_name: Optional[str] = None, region: str = "ap-southeast-1") -> Optional[dict]:
    """Tải chuỗi cấu hình JSON từ AWS Systems Manager Parameter Store."""
    if parameter_name is None:
        parameter_name = os.getenv("SSM_PARAMETER_NAME", "/huylam-ocr/config")
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
        "AWS_NATIVE_MODE_ENABLED": "aws_native_mode_enabled",
        "AWS_BEDROCK_MODEL": "aws_bedrock_model",
        "SSM_PARAMETER_NAME": "ssm_parameter_name",
        "TIMEOUT_SECONDS": "timeout_seconds",
        "COGNITO_REGION": "cognito_region",
        "COGNITO_USER_POOL_ID": "cognito_user_pool_id",
        "COGNITO_APP_CLIENT_ID": "cognito_app_client_id",
        "COGNITO_APP_CLIENT_SECRET": "cognito_app_client_secret",
        "COGNITO_DOMAIN": "cognito_domain",
        "COGNITO_REDIRECT_URI": "cognito_redirect_uri"
    }
    
    for env_k, cfg_k in env_mappings.items():
        val = os.getenv(env_k)
        if val is not None:
            if cfg_k in ("fast_path_enabled", "aws_native_mode_enabled"):
                config_dict[cfg_k] = val.lower() in ("true", "1", "yes")
            elif cfg_k in ("scan_threshold_chars", "timeout_seconds"):
                config_dict[cfg_k] = int(val)
            else:
                config_dict[cfg_k] = val
                
    return AppSettings(**config_dict)
