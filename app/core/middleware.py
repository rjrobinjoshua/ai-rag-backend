from time import time
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger


def setup_middleware(app: FastAPI):
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time()
        try:
            response = await call_next(request)
        except StarletteHTTPException as http_exc:
            # Let FastAPI's normal HTTPException handling do its job
            process_time = (time() - start) * 1000
            logger.error(
                "HTTPException | path={} status={} duration_ms={:.2f}",
                request.url.path,
                http_exc.status_code,
                process_time,
            )
            raise http_exc
        except RequestValidationError as validation_exc:
            process_time = (time() - start) * 1000
            logger.error(
                "ValidationError | path={} errors={} duration_ms={:.2f}",
                request.url.path,
                validation_exc.errors(),
                process_time,
            )
            return JSONResponse(
                status_code=422,
                content={
                    "detail": "Invalid request payload",
                    "errors": validation_exc.errors(),
                },
            )
        except Exception as exc:
            # Catch any unhandled exception, log it once, return clean 500
            process_time = (time() - start) * 1000
            logger.exception(
                "UnhandledException | path={} duration_ms={:.2f}",
                request.url.path,
                process_time,
            )
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )

        # Normal case logging
        process_time = (time() - start) * 1000
        logger.info(
            "Request | path={} status={} duration_ms={:.2f}",
            request.url.path,
            response.status_code,
            process_time,
        )
        return response
