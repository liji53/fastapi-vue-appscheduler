import re

from .models import SeverityEnum


def parse_log_content(log_text):
    if "Traceback (most recent call last):" in log_text:
        return SeverityEnum.FATAL

    error_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \| ERROR'
    if re.search(error_pattern, log_text):
        return SeverityEnum.ERROR

    warning_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \| WARNING'
    if re.search(warning_pattern, log_text):
        return SeverityEnum.WARNING

    return SeverityEnum.OTHER


def parse(running_status: bool, log: str, execute_type: str) -> dict:
    """日志文件解析"""
    if not running_status:
        return {
            "status": False,
            "log_type": SeverityEnum.FATAL,
            "execute_type": execute_type,
            "content": log
        }
    severity = parse_log_content(log)
    return {
        "status": False if severity == SeverityEnum.FATAL else True,
        "log_type": severity,
        "execute_type": execute_type,
        "content": log
    }
