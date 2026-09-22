import json
import os
import uuid
import logging
import urllib.parse
from datetime import datetime, timezone
import boto3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb")
s3_client = boto3.client("s3")

DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "document_processing_jobs")

def lambda_handler(event, context):
    """
    Diem khoi chay xu ly su kien S3 Event Notification khi co tep moi trong uploads/.
    Tu dong ghi nhan tien trinh vao Amazon DynamoDB va ghi log CloudWatch.
    """
    logger.info("Nhan su kien moi tu Amazon S3 Event Notification: %s", json.dumps(event))

    records = event.get("Records", [])
    if not records:
        logger.warning("Khong tim thay Records trong event payload.")
        return {"statusCode": 400, "body": json.dumps({"error": "No records found"})}

    results = []
    table = dynamodb.Table(DYNAMODB_TABLE)

    for record in records:
        s3_data = record.get("s3", {})
        bucket_name = s3_data.get("bucket", {}).get("name", "")
        raw_key = s3_data.get("object", {}).get("key", "")
        object_key = urllib.parse.unquote_plus(raw_key)
        object_size = s3_data.get("object", {}).get("size", 0)

        logger.info("Phat hien tep moi: s3://%s/%s (Kich thuoc: %d bytes)", bucket_name, object_key, object_size)

        # Trích xuất filename va job_id
        parts = object_key.split("/")
        filename = parts[-1] if parts else "document.pdf"

        # Neu co dinh dang uploads/<doc_id>/<filename>, dung doc_id do; neu khong thi sinh moi
        if len(parts) >= 3 and parts[0] == "uploads":
            job_id = parts[1]
        else:
            job_id = f"auto-{uuid.uuid4().hex[:8]}"

        now_iso = datetime.now(timezone.utc).isoformat()
        item = {
            "job_id": job_id,
            "created_at": now_iso,
            "filename": filename,
            "user_id": "s3-event-auto",
            "username": "automated-pipeline",
            "status": "RECEIVED_VIA_S3_EVENT",
            "s3_input_uri": f"s3://{bucket_name}/{object_key}",
            "s3_output_md_uri": f"s3://{bucket_name}/outputs/{job_id}/{filename}.md",
            "model_used": "AWS S3 Event Trigger (Serverless)",
            "file_size_bytes": object_size,
            "processing_time_seconds": "0.05"
        }

        try:
            table.put_item(Item=item)
            logger.info("Da luu tien trinh vao DynamoDB thanh cong (job_id: %s)", job_id)
            results.append({"job_id": job_id, "status": "RECORDED", "key": object_key})
        except Exception as e:
            logger.error("Loi khi ghi vao DynamoDB: %s", str(e))
            results.append({"job_id": job_id, "status": "ERROR", "error": str(e)})

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "message": "Xu ly su kien S3 hoan tat",
            "processed_count": len(results),
            "results": results
        })
    }
