import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from app.core.config import settings

def setup_logging():
    """Configure application logging"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create formatters and handlers
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename=log_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Set up specific loggers
    loggers = [
        "app",
        "uvicorn",
        "celery",
        "sqlalchemy.engine"
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(settings.LOG_LEVEL)
        logger.propagate = False
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

# Create a logger instance for the application
logger = logging.getLogger("app")