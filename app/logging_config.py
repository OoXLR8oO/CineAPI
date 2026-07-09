from logging import INFO, Formatter, getLogger
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

handler = RotatingFileHandler(
    LOG_DIR / "app.log",
    maxBytes=1_000_000,
    backupCount=5,
)

handler.setFormatter(Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))

root_logger = getLogger()
root_logger.setLevel(INFO)
root_logger.addHandler(handler)
