import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.health import router as health_router

# Import layer yang sudah kita bangun sebelumnya
from backend.core.config import settings
from backend.core.logging import setup_logging

# Inisialisasi logger untuk file ini
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager untuk mengatur fase startup dan shutdown aplikasi.
    Menggantikan pola usang @app.on_event("startup").
    """
    # --- Fase Startup ---
    # Setup konfigurasi logging terpusat tepat sebelum server menerima request
    setup_logging()
    logger.info(f"Mulai menjalankan {settings.APP_NAME} pada mode [{settings.APP_ENV}].")
    
    # Aplikasi berjalan dan menerima request pada titik ini
    yield
    
    # --- Fase Shutdown ---
    # Kode di bawah yield akan dieksekusi saat server dimatikan (Ctrl+C)
    # Berguna untuk menutup koneksi database atau membersihkan antrean VLM nanti
    logger.info("Mematikan server dan membersihkan resource...")

def create_app() -> FastAPI:
    """
    Application Factory Pattern.
    Membungkus inisialisasi FastAPI ke dalam sebuah fungsi.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Video-Based Object Tracking and Semantic Attribute Extraction System API",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Registrasi modul router (Mounting API)
    app.include_router(health_router, prefix="/api/v1")

    # Base endpoint untuk identifikasi root
    @app.get("/", tags=["System"])
    async def root():
        return {
            "message": f"Welcome to {settings.APP_NAME}. Kunjungi /docs untuk API Schema."
        }

    return app

# Instansiasi singleton aplikasi yang akan dieksekusi oleh Uvicorn
app = create_app()