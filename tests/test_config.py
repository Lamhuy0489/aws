import os
import pytest
from src.backend.config.settings import AppSettings, get_settings

def test_app_settings_defaults():
    settings = AppSettings()
    assert settings.ocr_mode == "HYBRID_KAGGLE"
    assert settings.fast_path_enabled is True
    assert settings.scan_threshold_chars == 50
    assert settings.dynamodb_table == "document_processing_jobs"

def test_app_settings_env_override(monkeypatch):
    monkeypatch.setenv("OCR_MODE", "STANDALONE")
    monkeypatch.setenv("FAST_PATH_ENABLED", "false")
    monkeypatch.setenv("SCAN_THRESHOLD_CHARS", "100")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")
    
    settings = get_settings()
    assert settings.ocr_mode == "STANDALONE"
    assert settings.fast_path_enabled is False
    assert settings.scan_threshold_chars == 100
    assert settings.gemini_api_key == "test-key-123"
