from fastapi import Request, HTTPException, status
from app.config import settings
import re

MAX_DEPTH = 20
MAX_KEYS = 5000

def validate_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key not in settings.ALLOWED_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

def mask_sensitive_data(payload: dict, fields_to_mask: list[str]) -> dict:
    masked = payload.copy()
    for field in fields_to_mask:
        if field in masked:
            masked[field] = "***MASKED***"
    return masked

def get_depth(obj, level=0):
    if isinstance(obj, dict):
        if not obj:
            return level
        return max(get_depth(v, level + 1) for v in obj.values())
    if isinstance(obj, list):
        if not obj:
            return level
        return max(get_depth(i, level + 1) for i in obj)
    return level


def count_keys(obj):
    if isinstance(obj, dict):
        return len(obj) + sum(count_keys(v) for v in obj.values())
    if isinstance(obj, list):
        return sum(count_keys(i) for i in obj)
    return 0


def contains_script_tags(obj):
    pattern = re.compile(r"<script.*?>", re.IGNORECASE)
    return pattern.search(str(obj)) is not None


def run_security_checks(payload: dict):
    if get_depth(payload) > MAX_DEPTH:
        return "Payload nesting too deep"

    if count_keys(payload) > MAX_KEYS:
        return "Payload too large"

    if contains_script_tags(payload):
        return "Script tag detected"

    return None