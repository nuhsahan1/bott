"""Shared logging configuration."""
import logging
import sys
from shared.config import settings


def get_logger(name: str) -> logging.Logger:
    """Get configured logger for service."""
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger
