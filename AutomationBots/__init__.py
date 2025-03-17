"""
AutomationBots

A collection of automation bots for various tasks.
"""
import sys
from loguru import logger

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:MM-DD HH:mm}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True,
    filter=lambda record: record["level"].name == "INFO",
)
# level data do not exist, so we need to create a new level
logger.level("DATA", no=15, color="<blue>")

logger.add(
    sys.stdout,
    level="DATA",
    format="<blue>{time:MM-DD HH:mm}</blue> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
    filter=lambda record: record["level"].name == "DATA",
)



__version__ = "0.1.0"