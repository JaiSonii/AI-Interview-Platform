import logging
import sys
from loguru import logger
from app.config import settings

class InterceptHandler(logging.Handler):
    """
    Redirects standard logging messages to Loguru.
    This ensures libraries like Uvicorn, HTTPX, and Prisma use Loguru.
    """
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame is not None and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging():
    # 1. Remove default handlers to avoid duplicate logs
    logging.root.handlers = [InterceptHandler()]
    
    # 2. Intercept specific libraries
    # These libraries use standard logging; we redirect them to Loguru
    for name in ["uvicorn", "uvicorn.access", "httpx", "prisma"]:
        logging_logger = logging.getLogger(name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False

    # 3. Configure Loguru
    logger.remove() # Remove default handler
    
    # Sink 1: Console (Human Readable)
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # Sink 2: File (Rotated & Retained)
    # Rotates every 10 MB or every day at midnight, keeps logs for 10 days
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="10 days",
        level="DEBUG",
        compression="zip", # Save space
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

    logger.info("✅ Logging successfully configured")