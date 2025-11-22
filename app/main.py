from fastapi import FastAPI
from loguru import logger

from app.core.config import get_settings
from app.api.routes import ask, health

def create_app():
    settings = get_settings()
    logger.info("Starting application: {}", settings.app_name)

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug
    )
    app.include_router(health.router)
    app.include_router(ask.router)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )