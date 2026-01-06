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
    def _bind_log(
        request: Request,
        *,
        request_id: str,
        status_code: int,
        duration_ms: float,
    ):
        return logger.bind(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            duration_ms=duration_ms,
            llm_calls=[c.model_dump() for c in request.state.llm_calls],
        )

    def _log_request(
        request: Request,
        *,
        request_id: str,
        status_code: int,
        start_time: float,
        exc: Optional[BaseException],
    ) -> None:
        duration_ms = (time() - start_time) * 1000
        log = _bind_log(
            request,
            request_id=request_id,
            status_code=status_code,
            duration_ms=duration_ms,
        )

        if exc is None:
            log.info("request_completed")
        else:
            log.error("request_failed")

    def _is_streaming(response) -> bool:
        return response is not None and isinstance(response, StreamingResponse)

    def _wrap_streaming_response(
        response: StreamingResponse,
        *,
        request: Request,
        request_id: str,
        start_time: float,
    ) -> None:
        original_iterator = response.body_iterator

        async def _stream_and_log():
            stream_exc: Optional[BaseException] = None
            try:
                async for chunk in original_iterator:
                    yield chunk
            except BaseException as exc:
                stream_exc = exc
                raise
            finally:
                _log_request(
                    request,
                    request_id=request_id,
                    status_code=getattr(response, "status_code", 500),
                    start_time=start_time,
                    exc=stream_exc,
                )

        response.body_iterator = _stream_and_log()

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        request_id: str = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id
        request.state.llm_calls = []

        start = time()
        response = None
        exc: Optional[BaseException] = None

        try:
            response = await call_next(request)
            if response is not None:
                response.headers["X-Request-Id"] = request_id

            if _is_streaming(response):
                _wrap_streaming_response(
                    response,
                    request=request,
                    request_id=request_id,
                    start_time=start,
                )

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

            if exc is None and _is_streaming(response):
                return

            if response is not None:
                response.headers["X-Request-Id"] = request_id

            _log_request(
                request,
                request_id=request_id,
                status_code=status_code,
                start_time=start,
                exc=exc,
            )
