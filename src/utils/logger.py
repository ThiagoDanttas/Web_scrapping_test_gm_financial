from pathlib import Path
from loguru import logger


def setup_logging() -> None:
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    file_log = log_dir / "app_{time:YYYY-MM-DD_HH-mm-ss}.log"
    logger.add(str(file_log), rotation="10 MB", retention="10 days") 