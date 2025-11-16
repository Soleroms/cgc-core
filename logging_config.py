"""
Simple logging configuration
"""
import logging
import sys

def setup_logging():
    """Setup basic logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def get_logger(name):
    """Get logger instance"""
    return logging.getLogger(name)