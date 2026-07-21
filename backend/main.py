import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.health import router as health_router
from backend.api.v1.detection import router as detection_router
from backend.api.v1.upload import router as upload_router
from backend.api.v1.video_job import router as video_job_router
from backend.core.config import settings
from backend.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager untuk startup dan shutdown aplikasi.
    """
    setup_logging()

    logger.info(
        "Mulai menjalankan %s pada mode [%s].",
        settings.APP_NAME,
        settings.APP_ENV,
    )

    yield

    logger.info("Mematikan server dan membersihkan resource...")


def create_app() -> FastAPI:
    """
    Application Factory Pattern.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description=(
            "Video-Based Object Tracking and "
            "Semantic Attribute Extraction System API"
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(
        health_router,
        prefix="/api/v1",
    )

    app.include_router(
        video_job_router,
        prefix="/api/v1",
    )

    app.include_router(
        detection_router,
        prefix="/api/v1",
    )

    app.include_router(
        upload_router,
        prefix="/api/v1",
    )

    @app.get("/", tags=["System"])
    async def root():
        return {
            "message": (
                f"Welcome to {settings.APP_NAME}. "
                "Kunjungi /docs untuk API Schema."
            )
        }

    return app


app = create_app()
