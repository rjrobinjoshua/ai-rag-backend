import sys

from loguru import logger

from app.core.config import get_settings


def setup_logging() -> None:
    settings = get_settings()
    logger.remove()

    def _patch_record(record):
        record["extra"].setdefault("request_id", "-")
        record["extra"].setdefault("path", "-")
        record["extra"].setdefault("status_code", "-")
        record["extra"].setdefault("duration_ms", "-")
        record["extra"].setdefault("llm_calls", [])
        return record

    logger.configure(patcher=_patch_record)

    if settings.env == "local":
        # 1) Pretty console logs (human friendly)
        logger.add(
            sys.stdout,
            level=settings.log_level,
            enqueue=True,
            backtrace=False,
            diagnose=False,
            format=(
                "<green>{time:HH:mm:ss}</green> | "
                "<cyan>{level}</cyan> | "
                "{message} | "
                "rid={extra[request_id]} "
                "path={extra[path]} "
                "status={extra[status_code]} "
                "ms={extra[duration_ms]} "
                "llm={extra[llm_calls]}"
            ),
        )

        # 2) Full structured logs to file (machine friendly)
        logger.add(
            "logs/app.jsonl",
            level=settings.log_level,
            serialize=True,
            enqueue=True,
            backtrace=False,
            diagnose=False,
            rotation="10 MB",
            retention="7 days",
        )
    else:
        # Prod: JSON logs to stdout
        logger.add(
            sys.stdout,
            level=settings.log_level,
            serialize=True,
            enqueue=True,
            backtrace=False,
            diagnose=False,
        )

    logger.info("logging_initialized", env=settings.env, log_level=settings.log_level)
