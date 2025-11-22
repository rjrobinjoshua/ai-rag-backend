from fastapi import FastAPI
from loguru import logger

from app.core.config import get_settings
from app.api.routes import ask, health
from app.core.middleware import setup_middleware

settings = get_settings()

def create_app():
    logger.info(
        "Starting application: {} in port {}",
        settings.app_name, 
        settings.port
    )

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug
    )
    setup_middleware(app)

    app.include_router(health.router)
    app.include_router(ask.router)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    )