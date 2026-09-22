import json
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import boto3
from botocore.exceptions import ClientError

from src.backend.config.settings import AppSettings, get_settings

logger = logging.getLogger(__name__)

class AWSStorageService:
    """Dich vu ket noi va thao tac voi ha tang AWS Cloud (S3, DynamoDB, Bedrock, SSM)."""

    def __init__(self, settings: Optional[AppSettings] = None):
        self.settings = settings or get_settings()
        self.region = self.settings.aws_region
        self.bucket_name = self.settings.s3_bucket
        self.table_name = self.settings.dynamodb_table

        try:
            self.s3_client = boto3.client("s3", region_name=self.region)
            self.dynamodb = boto3.resource("dynamodb", region_name=self.region)
            self.dynamodb_client = boto3.client("dynamodb", region_name=self.region)
            self.table = self.dynamodb.Table(self.table_name)
            self.bedrock_runtime = boto3.client("bedrock-runtime", region_name=self.region)
            self.is_connected = True
        except Exception as e:
            logger.warning(f"Khong the khoi tao Boto3 Client cho AWS: {e}")
            self.is_connected = False

    def upload_file(self, file_bytes: bytes, key: str, content_type: str = "application/octet-stream") -> Optional[str]:
        """Tai tep len Amazon S3 va tra ve duong dan S3 URI."""
        if not self.is_connected:
            logger.warning("AWS chua duoc ket noi, bo qua upload S3.")
            return None
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_bytes,
                ContentType=content_type
            )
            s3_uri = f"s3://{self.bucket_name}/{key}"
            logger.info(f"Da tai tep len S3 thanh cong: {s3_uri}")
            return s3_uri
        except ClientError as e:
            logger.error(f"Loi ClientError khi tai tep len S3: {e}")
            return None
        except Exception as e:
            logger.error(f"Loi khong xac dinh khi tai tep len S3: {e}")
            return None

    def download_file(self, key: str) -> Optional[bytes]:
        """Tai noi dung tep tu Amazon S3."""
        if not self.is_connected:
            return None
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response["Body"].read()
        except Exception as e:
            logger.error(f"Loi khi tai tep tu S3 ({key}): {e}")
            return None

    def record_job(
        self,
        job_id: str,
        filename: str,
        user_id: str = "anonymous",
        username: str = "anonymous",
        status: str = "COMPLETED",
        total_pages: int = 1,
        digital_pages: int = 0,
        scanned_pages: int = 0,
        processing_time_seconds: float = 0.0,
        s3_input_uri: str = "",
        s3_output_md_uri: str = "",
        s3_output_docx_uri: str = "",
        s3_output_pdf_uri: str = "",
        model_used: str = "Fast-Path",
        error_message: str = ""
    ) -> Optional[dict]:
        """Ghi nhan tien trinh xu ly tai lieu vao bang DynamoDB (Partition Key: job_id, Sort Key: created_at)."""
        if not self.is_connected:
            return None

        created_at = datetime.now(timezone.utc).isoformat()
        item = {
            "job_id": job_id,
            "created_at": created_at,
            "filename": filename,
            "user_id": user_id,
            "username": username,
            "status": status,
            "total_pages": int(total_pages),
            "digital_pages": int(digital_pages),
            "scanned_pages": int(scanned_pages),
            "processing_time_seconds": str(round(processing_time_seconds, 2)),
            "s3_input_uri": s3_input_uri,
            "s3_output_md_uri": s3_output_md_uri,
            "s3_output_docx_uri": s3_output_docx_uri,
            "s3_output_pdf_uri": s3_output_pdf_uri,
            "model_used": model_used
        }
        if error_message:
            item["error_message"] = error_message

        try:
            self.table.put_item(Item=item)
            logger.info(f"Da luu tien trinh vao DynamoDB thanh cong (job_id={job_id}, created_at={created_at})")
            return item
        except Exception as e:
            logger.error(f"Loi khi ghi ban ghi vao DynamoDB: {e}")
            return None

    def get_job(self, job_id: str) -> Optional[dict]:
        """Truy van thong tin mot tien trinh tu DynamoDB theo job_id."""
        if not self.is_connected:
            return None
        try:
            from boto3.dynamodb.conditions import Key
            response = self.table.query(
                KeyConditionExpression=Key("job_id").eq(job_id),
                ScanIndexForward=False,
                Limit=1
            )
            items = response.get("Items", [])
            return items[0] if items else None
        except Exception as e:
            logger.error(f"Loi khi truy van DynamoDB voi job_id {job_id}: {e}")
            return None

    def invoke_bedrock_converse(
        self,
        prompt: str,
        system_instruction: str = "Ban la chuyen gia dich thuat tai lieu ky thuat chat luong cao.",
        model_id: Optional[str] = None
    ) -> Optional[str]:
        """Goi mo hinh Amazon Bedrock qua Converse API (Amazon Nova hoac Anthropic Claude)."""
        if not self.is_connected:
            return None
        target_model = model_id or self.settings.aws_bedrock_model
        try:
            messages = [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]
            system_config = [{"text": system_instruction}] if system_instruction else []
            
            response = self.bedrock_runtime.converse(
                modelId=target_model,
                messages=messages,
                system=system_config,
                inferenceConfig={"temperature": 0.2, "maxTokens": 2048}
            )
            output_content = response["output"]["message"]["content"][0]["text"]
            return output_content
        except Exception as e:
            logger.error(f"Loi khi goi Bedrock converse ({target_model}): {e}")
            return None

    def check_aws_health(self) -> Dict[str, Any]:
        """Kiem tra toan dien ket noi va tinh trang cac tai nguyen AWS."""
        status = {
            "s3": {"status": "UNKNOWN", "bucket": self.bucket_name},
            "dynamodb": {"status": "UNKNOWN", "table": self.table_name},
            "ssm": {"status": "UNKNOWN", "parameter": self.settings.ssm_parameter_name}
        }
        if not self.is_connected:
            return {k: {"status": "DISCONNECTED"} for k in status}

        # Kiem tra S3
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            status["s3"]["status"] = "HEALTHY"
        except Exception as e:
            status["s3"]["status"] = "ERROR"
            status["s3"]["error"] = str(e)

        # Kiem tra DynamoDB
        try:
            desc = self.dynamodb_client.describe_table(TableName=self.table_name)
            status["dynamodb"]["status"] = desc["Table"]["TableStatus"]
        except Exception as e:
            status["dynamodb"]["status"] = "ERROR"
            status["dynamodb"]["error"] = str(e)

        # Kiem tra SSM Parameter
        try:
            ssm_client = boto3.client("ssm", region_name=self.region)
            res = ssm_client.get_parameter(Name=self.settings.ssm_parameter_name, WithDecryption=False)
            status["ssm"]["status"] = "EXISTS"
            status["ssm"]["version"] = res["Parameter"]["Version"]
        except Exception as e:
            status["ssm"]["status"] = "ERROR"
            status["ssm"]["error"] = str(e)

        return status
