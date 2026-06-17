# utils/logger.py
# Lynkeus Initiative
# Centralized Framework Logging Utility

import os
import logging
def setup_logger():
    # Ensure the logs directory exists in the project root
    log_file = "lynkeus.log"
    
    # Create a system-wide logger instance
    logger = logging.getLogger("LynkeusLogger")
    
    # Prevent duplicate handlers if setup is called multiple times
    if not logger.handlers:
        logger.setLevel(logging.INFO)
    
        # Configure file logging with a clean timestamp layout
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
    
# Globally accessible instance for simple importing across modules
log = setup_logger()
