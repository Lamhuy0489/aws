import pytest
from unittest.mock import MagicMock, patch
from src.backend.config.settings import AppSettings
from src.backend.cloud.aws_storage import AWSStorageService

def test_aws_storage_service_initialization():
    settings = AppSettings(
        aws_region="ap-southeast-1",
        s3_bucket="huylam-ocr-documents-ap-southeast-1",
        dynamodb_table="document_processing_jobs"
    )
    svc = AWSStorageService(settings=settings)
    assert svc.region == "ap-southeast-1"
    assert svc.bucket_name == "huylam-ocr-documents-ap-southeast-1"
    assert svc.table_name == "document_processing_jobs"

def test_record_job_mock():
    settings = AppSettings()
    svc = AWSStorageService(settings=settings)
    
    mock_table = MagicMock()
    svc.table = mock_table
    svc.is_connected = True

    result = svc.record_job(
        job_id="job-12345",
        filename="report.pdf",
        user_id="user-1",
        username="huylam",
        status="COMPLETED",
        total_pages=5,
        digital_pages=4,
        scanned_pages=1,
        processing_time_seconds=1.23,
        s3_input_uri="s3://huylam-ocr-documents-ap-southeast-1/uploads/job-12345/report.pdf",
        s3_output_md_uri="s3://huylam-ocr-documents-ap-southeast-1/outputs/job-12345/report.md",
        model_used="Fast-Path (Digital)"
    )

    assert result is not None
    assert result["job_id"] == "job-12345"
    assert "created_at" in result
    assert result["user_id"] == "user-1"
    assert result["total_pages"] == 5
    mock_table.put_item.assert_called_once()

def test_check_aws_health_mock():
    settings = AppSettings()
    svc = AWSStorageService(settings=settings)
    
    svc.s3_client = MagicMock()
    svc.dynamodb_client = MagicMock()
    svc.dynamodb_client.describe_table.return_value = {"Table": {"TableStatus": "ACTIVE"}}
    svc.is_connected = True

    with patch("boto3.client") as mock_boto:
        mock_ssm = MagicMock()
        mock_ssm.get_parameter.return_value = {"Parameter": {"Version": 1}}
        mock_boto.return_value = mock_ssm
        
        health = svc.check_aws_health()
        assert health["s3"]["status"] == "HEALTHY"
        assert health["dynamodb"]["status"] == "ACTIVE"
        assert health["ssm"]["status"] == "EXISTS"
