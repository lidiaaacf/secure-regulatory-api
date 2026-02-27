from fastapi import Request, HTTPException, status
from app.config import settings

def validate_api_key(request: Request):
    """
    Validate the API key from request headers using allowed keys from env.
    """
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key not in settings.ALLOWED_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

def mask_sensitive_data(payload: dict, fields_to_mask: list[str]) -> dict:
    """Return a copy of payload with sensitive fields masked."""
    masked = payload.copy()
    for field in fields_to_mask:
        if field in masked:
            masked[field] = "***MASKED***"
    return masked