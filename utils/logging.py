import logging
import sys
from utils.config import Config

def setup_logger(name: str):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(Config.LOG_LEVEL)
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(Config.LOG_LEVEL)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add handler
        logger.addHandler(handler)
        
    return logger
