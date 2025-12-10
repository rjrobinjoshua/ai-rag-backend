from fastapi import FastAPI
from loguru import logger

from app.api.routes import admin, ask, embed, health, rag_query, stream_chat
from app.core.config import get_settings
from app.core.logger import setup_logging
from app.core.middleware import setup_middleware

settings = get_settings()


def create_app():
    setup_logging()
    logger.info(
        "Starting application: {}",
        settings.app_name,
    )

    app = FastAPI(title=settings.app_name, debug=settings.debug)
    setup_middleware(app)

    app.include_router(health.router)
    app.include_router(ask.router)
    app.include_router(embed.router)
    app.include_router(stream_chat.router)
    app.include_router(rag_query.router)
    app.include_router(admin.router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
