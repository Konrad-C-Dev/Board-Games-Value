import schedule
import time
from typing import Callable
from utils.logging_config import get_logger

logger = get_logger(__name__)


def every_hours(hours: int, job: Callable):
    schedule.every(hours).hours.do(job)


def run_forever():
    logger.info("Starting scheduler loop")
    while True:
        schedule.run_pending()
        time.sleep(1)
