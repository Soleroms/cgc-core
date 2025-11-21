import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_level: str = 'INFO', log_file: str = 'logs/cgc_core.log'):
    """
    Configure production logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger()
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Clear existing handlers
    logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("=" * 70)
    logger.info("CGC CORE™ - Production Server")
    logger.info(f"Logging initialized: {log_file}")
    logger.info("=" * 70)

def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)