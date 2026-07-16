import logging

from fastapi import FastAPI

from backend.api.health import router as health_router
from backend.core.logging import setup_logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Video-Based Object Tracking API",
        description="Proof of Concept for Object Tracking and Semantic Attribute Extraction",
        version="0.1.0",
    )

    app.include_router(health_router, prefix="/api")

    logger.info("Application initialized successfully.")

    @app.get("/")
    async def root():
        return {
            "message": "Video-Based Object Tracking API is running."
        }

    return app


app = create_app()