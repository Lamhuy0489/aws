import json
import os
import uuid
import logging
import boto3
from typing import Dict, Any
from src.backend.config.settings import get_settings
from src.backend.parsers.hybrid_engine import HybridDocumentEngine
from src.backend.exporters.markdown_exporter import MarkdownExporter
from src.backend.exporters.docx_exporter import DocxExporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Điểm khởi chạy chính của AWS Lambda cho cả sự kiện S3 và API Gateway."""
    settings = get_settings()
    engine = HybridDocumentEngine(settings=settings)
    s3_client = boto3.client("s3", region_name=settings.aws_region)
    dynamodb = boto3.resource("dynamodb", region_name=settings.aws_region)

    # 1. Xử lý sự kiện tải tệp lên Amazon S3 (s3:ObjectCreated)
    if "Records" in event and event["Records"] and "s3" in event["Records"][0]:
        return handle_s3_event(event, settings, engine, s3_client, dynamodb)

    # 2. Xử lý yêu cầu HTTP qua API Gateway
    http_method = event.get("httpMethod", event.get("requestContext", {}).get("http", {}).get("method", ""))
    path = event.get("path", event.get("rawPath", ""))

    # Yêu cầu cấp S3 Presigned URL để upload tệp
    if "/presigned-url" in path:
        return handle_presigned_url_request(event, settings, s3_client)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps({
            "service": "Serverless Hybrid Document OCR & Parsing Platform",
            "mode": settings.ocr_mode,
            "fast_path_enabled": settings.fast_path_enabled,
            "status": "ready"
        })
    }

def handle_s3_event(event: dict, settings: Any, engine: HybridDocumentEngine, s3_client: Any, dynamodb: Any) -> dict:
    """Xử lý tệp được kích hoạt từ sự kiện S3 ObjectCreated."""
    record = event["Records"][0]["s3"]
    bucket_name = record["bucket"]["name"]
    object_key = record["object"]["key"]

    logger.info(f"Nhận sự kiện tệp mới tải lên: s3://{bucket_name}/{object_key}")
    filename = os.path.basename(object_key)
    doc_id = str(uuid.uuid4())[:8]

    try:
        # Tải tệp từ S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        file_bytes = response["Body"].read()

        # Thực thi bóc tách lai
        result = engine.process_document(file_bytes=file_bytes, filename=filename, document_id=doc_id)

        # Xuất file Markdown và tải lên S3 /outputs/
        md_content = MarkdownExporter.export_to_string(result)
        out_md_key = f"outputs/{doc_id}/{filename}.md"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=out_md_key,
            Body=md_content.encode("utf-8"),
            ContentType="text/markdown"
        )

        # Xuất file Word (.docx) và tải lên S3 /outputs/
        docx_bytes = DocxExporter.export_to_bytes(result)
        out_docx_key = f"outputs/{doc_id}/{filename}.docx"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=out_docx_key,
            Body=docx_bytes,
            ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        # Ghi nhận trạng thái vào DynamoDB
        try:
            table = dynamodb.Table(settings.dynamodb_table)
            table.put_item(Item={
                "document_id": doc_id,
                "filename": filename,
                "total_pages": result.total_pages,
                "digital_pages": result.digital_pages_count,
                "scanned_pages": result.scanned_pages_count,
                "processing_time_seconds": str(result.processing_time_seconds),
                "output_md_url": f"s3://{bucket_name}/{out_md_key}",
                "output_docx_url": f"s3://{bucket_name}/{out_docx_key}",
                "status": "COMPLETED"
            })
        except Exception as db_err:
            logger.warning(f"Không thể ghi dữ liệu vào DynamoDB: {db_err}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Xử lý tài liệu thành công",
                "document_id": doc_id,
                "markdown_key": out_md_key,
                "docx_key": out_docx_key
            })
        }
    except Exception as e:
        logger.error(f"Lỗi khi xử lý tệp từ S3: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def handle_presigned_url_request(event: dict, settings: Any, s3_client: Any) -> dict:
    """Tạo Presigned URL cho phép trình duyệt tải tệp thẳng lên S3 mà không nghẽn API Gateway."""
    query = event.get("queryStringParameters") or {}
    filename = query.get("filename", "document.pdf")
    upload_key = f"uploads/{uuid.uuid4().hex[:8]}/{filename}"

    presigned_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": settings.s3_bucket, "Key": upload_key},
        ExpiresIn=300
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps({
            "upload_url": presigned_url,
            "key": upload_key
        })
    }
