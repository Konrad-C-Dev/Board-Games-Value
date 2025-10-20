from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from typing import List
import logging

from db import database
from db.models import Game
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scraper.aleplanszowki_scraper import AleplanszowkiScraper
from utils.robot_check import is_allowed
from scraper.persistence import upsert_game


class ScrapeRequest(BaseModel):
    url: HttpUrl


app = FastAPI(title="Board Games Value API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup():
    try:
        database.init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/games")
def list_games():
    session: Session = database.get_session()
    try:
        games = session.query(Game).order_by(Game.created_at.desc()).limit(100).all()
        result = [
            {
                "id": g.id,
                "name": g.name,
                "url": g.url,
                "price": g.price,
                "availability": g.availability,
                "image_url": g.image_url,
                "created_at": g.created_at.isoformat() if g.created_at else None,
            }
            for g in games
        ]
        return JSONResponse(result)
    finally:
        session.close()


@app.post("/api/scrape")
def scrape_url(req: ScrapeRequest):
    url = str(req.url)
    if not is_allowed(url, user_agent="DataScienceScraperBot/1.0 (+kontakt@example.com)"):
        raise HTTPException(status_code=403, detail="robots.txt disallows scraping this URL")

    scraper = AleplanszowkiScraper()
    html = scraper.fetch_html(url)
    parsed = scraper.parse_page(html)
    # ensure URL is present
    if not parsed.get("url"):
        parsed["url"] = url

    session = database.get_session()
    try:
        game = upsert_game(session, parsed)
        return {
            "id": game.id,
            "name": game.name,
            "url": game.url,
            "price": game.price,
            "availability": game.availability,
            "image_url": game.image_url,
            "created_at": game.created_at.isoformat() if game.created_at else None,
        }
    finally:
        session.close()

