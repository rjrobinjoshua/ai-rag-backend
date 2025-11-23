from fastapi import FastAPI
from loguru import logger

from app.core.config import get_settings
from app.api.routes import ask, embed, health
from app.core.logger import setup_logging
from app.core.middleware import setup_middleware

settings = get_settings()



def create_app():
    setup_logging()
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
    app.include_router(embed.router)
    
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