from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.config import get_settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


async def verify_key(key: str = Security(_api_key_header)) -> None:
    settings = get_settings()
    if not settings.api_secret_key:
        raise HTTPException(status_code=500, detail="API key not configured on server")
    if key != settings.api_secret_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
