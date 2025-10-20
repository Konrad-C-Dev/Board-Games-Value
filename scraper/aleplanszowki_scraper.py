from typing import Dict, Optional
from bs4 import BeautifulSoup
import re

from .base_scraper import BaseScraper
from .selectors import TITLE, PRICE, AVAILABILITY, IMAGE, OG_URL
from utils.logging_config import get_logger

logger = get_logger(__name__)


class AleplanszowkiScraper(BaseScraper):
    def parse_page(self, html: str) -> Dict:
        soup = BeautifulSoup(html, "lxml")

        def first_or_none(sel):
            el = soup.select_one(sel)
            return el.get_text(strip=True) if el else None

        def meta_content(sel):
            el = soup.select_one(sel)
            return el["content"] if el and el.has_attr("content") else None

        # Title: prefer structured selectors, then og:title, then <title>
        title = first_or_none(TITLE) or meta_content("meta[property='og:title']") or (soup.title.string.strip() if soup.title and soup.title.string else None)

        # Price: try several common meta tags and selectors, fallback to regex search
        price = (
            first_or_none(PRICE)
            or meta_content("meta[itemprop='price']")
            or meta_content("meta[property='product:price:amount']")
            or meta_content("meta[name='price']")
        )
        if not price:
            # regex: look for patterns like 123.45 or 123,45 with optional currency
            m = re.search(r"(\d+[\.,]\d{2})(?=\s*(PLN|zł|zloty|EUR|€|USD|\$)?)", html)
            if m:
                price = m.group(1)

        availability = first_or_none(AVAILABILITY) or meta_content("meta[itemprop='availability']")

        # Image: prefer itemprop image, then og:image
        image = None
        img_el = soup.select_one(IMAGE)
        if img_el and img_el.has_attr("src"):
            image = img_el["src"]
        if not image:
            image = meta_content("meta[property='og:image']")

        url = meta_content(OG_URL) or meta_content("meta[property='og:url']")

        data = {
            "title": title,
            "price": price,
            "availability": availability,
            "image": image,
            "url": url,
        }
        logger.debug("Parsed data: %s", data)
        return data
