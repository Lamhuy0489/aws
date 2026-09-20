import io
import pytest
from src.backend.parsers.fast_parser import FastNativeParser, ParsedPage

def test_convert_table_to_markdown():
    matrix = [
        ["Hạng mục", "Số lượng", "Đơn giá"],
        ["Máy chủ EC2", "2", "500,000"],
        ["Lưu trữ S3", "50 GB", "1,000"]
    ]
    md = FastNativeParser._convert_table_to_markdown(matrix)
    
    assert "| Hạng mục | Số lượng | Đơn giá |" in md
    assert "| --- | --- | --- |" in md
    assert "| Máy chủ EC2 | 2 | 500,000 |" in md
    assert "| Lưu trữ S3 | 50 GB | 1,000 |" in md

def test_convert_empty_table():
    assert FastNativeParser._convert_table_to_markdown([]) == ""
    assert FastNativeParser._convert_table_to_markdown([[]]) == ""

def test_fast_parser_scan_threshold():
    parser = FastNativeParser(scan_threshold_chars=50)
    assert parser.scan_threshold_chars == 50
