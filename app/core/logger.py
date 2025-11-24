import sys

from loguru import logger


def setup_logging():
    logger.remove()  # Remove default handler

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<cyan>{level}</cyan> | "
        "<yellow>{message}</yellow>",
        level="INFO",
        enqueue=True,  # thread/process safe
    )

    logger.info("Logging initialized")
