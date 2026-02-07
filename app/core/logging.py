import logging
import sys
from app.core.config import settings

def setup_logging():
    logger = logging.getLogger("voice-service")
    logger.setLevel(settings.LOG_LEVEL)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger

logger = setup_logging()
