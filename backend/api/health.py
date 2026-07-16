from fastapi import APIRouter
from backend.core.config import settings

# Menggunakan APIRouter agar routing termodularisasi dan terpisah dari main.py
router = APIRouter(tags=["System"])

@router.get("/health")
async def health_check():
    """
    Endpoint diagnostik untuk memverifikasi bahwa API berjalan
    dan layer konfigurasi berhasil dimuat dengan benar.
    """
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV
    }