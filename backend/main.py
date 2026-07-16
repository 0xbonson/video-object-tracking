from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Video-Based Object Tracking API",
        description="Proof of Concept for Object Tracking and Semantic Attribute Extraction",
        version="0.1.0",
    )

    @app.get("/")
    async def root():
        return {
            "message": "Video-Based Object Tracking API is running."
        }

    return app


app = create_app()
