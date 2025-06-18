# Builtin imports
import os
import sys

from datetime import datetime

# Third-party imports

# Local imports
from loguru import logger
from app.billy_web import BillyWeb

# ------------------------------- [LOGGER] -------------------------------
LEVEL = os.getenv("LOG_LEVEL")

logger.remove()  # Remove default logger configuration
# Add new logger configuration to write to a file
logger.add(
    f"logs/{LEVEL}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
    format="<yellow>[{time:YYYY-MM-DD HH:mm:ss:SSSS}]</yellow> [<level><b>{level}</b></level>] [<b>{file.path}:{line}</b>] [<b>{function}</b>] <level>{message}</level>",
    level=LEVEL,
)
# Add new logger configuration to print to console
logger.add(
    sys.stdout,
    format="<yellow>[{time:YYYY-MM-DD HH:mm:ss:SSSS}]</yellow> [<level><b>{level}</b></level>] [<b>{file.path}:{line}</b>] [<b>{function}</b>] <level>{message}</level>",
    level=LEVEL,
)


# ------------------------------- [APP] -------------------------------
billy_web = BillyWeb()
# ------------------------------- [RESPONSE ERROR] -------------------------------
