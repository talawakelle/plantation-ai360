from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter(tags=["system"])

@router.get("/health")
def health():
    s = get_settings()
    return {"status": "ok", "service": s.app_name, "version": s.app_version, "environment": s.environment}
