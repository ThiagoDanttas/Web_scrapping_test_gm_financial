from pathlib import Path
from loguru import logger
from datetime import date

def setup_logging() -> None:
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    today = date.today().strftime("%d-%m-%Y")
    file_log = log_dir / today / "app_{time:YYYY-MM-DD}.log"
    logger.add(str(file_log), rotation="50 MB", retention="10 days", mode='a') 