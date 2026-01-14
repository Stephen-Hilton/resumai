import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging():
    """
    Set up logging to both console and dated log files with auto-flush.
    Creates logs in src/logs/ directory with format: YYYY-MM-DD_resumai.log
    
    Returns:
        logger: Logger instance for the calling module
    """
    root_logger = logging.getLogger()
    
    # Check if logging is already configured (look for our specific setup)
    if root_logger.handlers and hasattr(root_logger, '_resumai_configured'):
        return logging.getLogger(__name__)
    
    # Clear any existing handlers to start fresh
    root_logger.handlers.clear()
    
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Create dated log filename
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f'{today}_resumai.log'
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Configure root logger
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Set stdout to be unbuffered for immediate console output
    sys.stdout.reconfigure(line_buffering=True)
    
    # Mark that we've configured logging
    root_logger._resumai_configured = True
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("="*50)
    logger.info("ResumeAI Logging System Started")
    logger.info(f"Log file: {log_file}")
    logger.info("="*50)
    
    return logger


def force_flush_logs():
    """Force flush all logging handlers and stdout to ensure immediate output"""
    sys.stdout.flush()
    sys.stderr.flush()
    for handler in logging.getLogger().handlers:
        if hasattr(handler, 'flush'):
            handler.flush()


def get_logger(name):
    """
    Get a logger instance for the given module name.
    Ensures logging is set up first.
    
    Args:
        name: Usually __name__ from the calling module
        
    Returns:
        logger: Logger instance
    """
    setup_logging()
    return logging.getLogger(name)