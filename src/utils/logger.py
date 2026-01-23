import logging
import sys
from pathlib import Path

# Create logger
logger = logging.getLogger("intelligent_data_viz")
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(Path(__file__).parent.parent.parent / "app.log")

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        logging.Logger instance
    """
    return logging.getLogger(f"intelligent_data_viz.{name}")