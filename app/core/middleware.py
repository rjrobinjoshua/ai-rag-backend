import uuid
from time import time
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import StreamingResponse


def setup_middleware(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        # -------------------------
        # Correlation + LLM state
        # -------------------------
        request_id: str = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id
        request.state.llm_calls = []  # Step 3 will populate this

        start = time()
        response = None
        exc: Optional[BaseException] = None
        defer_log = False

        try:
            response = await call_next(request)
            if response is not None:
                response.headers["X-Request-Id"] = request_id

            is_streaming = response is not None and (
                isinstance(response, StreamingResponse)
                or getattr(response, "body_iterator", None) is not None
            )

            if is_streaming:
                original_iterator = response.body_iterator
                defer_log = True

                async def _stream_and_log():
                    try:
                        async for chunk in original_iterator:
                            yield chunk
                    finally:
                        process_time_ms = (time() - start) * 1000
                        log = logger.bind(
                            request_id=request_id,
                            method=request.method,
                            path=request.url.path,
                            status_code=getattr(response, "status_code", 500),
                            duration_ms=process_time_ms,
                            llm_calls=[c.model_dump() for c in request.state.llm_calls],
                        )
                        log.info("request_completed")

                response.body_iterator = _stream_and_log()
            return response

        except StarletteHTTPException as http_exc:
            exc = http_exc
            raise

        except RequestValidationError as validation_exc:
            exc = validation_exc
            process_time = (time() - start) * 1000

            logger.bind(
                request_id=request_id,
                path=request.url.path,
                duration_ms=process_time,
                errors=validation_exc.errors(),
            ).warning("validation_error")

            return JSONResponse(
                status_code=422,
                content={
                    "detail": "Invalid request payload",
                    "errors": validation_exc.errors(),
                },
            )

        except Exception as e:
            exc = e
            process_time = (time() - start) * 1000

            logger.bind(
                request_id=request_id,
                path=request.url.path,
                duration_ms=process_time,
            ).exception("unhandled_exception")

            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )

        finally:
            status_code = getattr(response, "status_code", 500)

            if not (defer_log and exc is None):
                if response is not None:
                    response.headers["X-Request-Id"] = request_id

                process_time_ms = (time() - start) * 1000
                log = logger.bind(
                    request_id=request_id,
                    method=request.method,
                    path=request.url.path,
                    status_code=status_code,
                    duration_ms=process_time_ms,
                    llm_calls=[c.model_dump() for c in request.state.llm_calls],
                )

                if exc is None:
                    log.info("request_completed")
                else:
                    log.error("request_failed")
