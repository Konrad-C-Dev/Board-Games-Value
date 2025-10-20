from sqlalchemy.orm import Session
from db.models import Game, Category, PriceHistory
from datetime import datetime


def upsert_game(session: Session, data: dict) -> Game:
    """Insert or update a Game record and append a PriceHistory entry.

    data should contain: title, url, price, availability, image
    """
    url = data.get("url")
    if not url:
        raise ValueError("Missing url in data")

    game = session.query(Game).filter_by(url=url).one_or_none()
    if not game:
        game = Game(
            name=data.get("title") or "",
            url=url,
            price=data.get("price"),
            availability=data.get("availability"),
            image_url=data.get("image"),
        )
        session.add(game)
        session.flush()  # get id
    else:
        # update simple fields
        game.name = data.get("title") or game.name
        game.price = data.get("price")
        game.availability = data.get("availability")
        game.image_url = data.get("image")

    # append price history
    ph = PriceHistory(game_id=game.id, price=data.get("price"), recorded_at=datetime.utcnow())
    session.add(ph)
    session.commit()
    session.refresh(game)
    return game
