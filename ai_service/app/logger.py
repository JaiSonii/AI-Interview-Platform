from loguru import logger
import sys
import os

from .config import settings


def setup_logging():
    global logger
    ROOT_PATH = settings.LOG_ROOT_PATH
    if not ROOT_PATH:
        raise ValueError('ROOT PATH FOR LOGS NOT PROVIDED')
        
    os.makedirs(ROOT_PATH, exist_ok=True)

    # First remove the basic logger
    logger.remove()

    # Now add handler for info
    logger.add(
        sys.stdout,
        format="<green>{time}</green> <level>{level}</level> <cyan>{message}</cyan>",
        filter=lambda record: record["level"].name in ["INFO", "DEBUG", "TRACE"]
    )

    # wanring, error, critical -> stderr
    logger.add(
        sys.stderr,
        level='WARNING',
        format="<yellow>{time}</yellow> <level>{level}</level> <red>{message}</red>"
    )

    # File handler with rotation
    logger.add(
        os.path.join(ROOT_PATH, 'ai_service.log'),  
        rotation="10 MB",
        level='INFO',
        retention="10 days",
        compression='zip'
    )
