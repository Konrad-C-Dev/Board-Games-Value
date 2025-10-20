import time
import random
import logging
from typing import Dict

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from utils.logging_config import get_logger

logger = get_logger(__name__)


class BaseScraper:
    def __init__(self, user_agent: str = "DataScienceScraperBot/1.0 (+kontakt@example.com)"):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    @retry(retry=retry_if_exception_type(RequestException), stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def fetch_html(self, url: str) -> str:
        """Fetch HTML from a URL with basic retry/backoff and polite delay."""
        logger.info("Fetching %s", url)
        # polite random delay
        time.sleep(random.uniform(1, 2))
        resp = self.session.get(url, timeout=15)
        resp.raise_for_status()
        return resp.text

    def parse_page(self, html: str) -> Dict:
        """Subclasses should implement parsing logic and return dict."""
        raise NotImplementedError()

    def save_to_db(self, data: Dict):
        """Hook for saving parsed data. Subclasses can override or call DB helpers."""
        logger.info("save_to_db called with: %s", data)
