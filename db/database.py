from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from db.models import Base


def _get_engine():
    """Create SQLAlchemy engine based on BGV_DB env var (lazy)."""
    db_path = os.getenv("BGV_DB", "sqlite:///games.db")
    connect_args = {"check_same_thread": False} if db_path.startswith("sqlite") else {}
    return create_engine(db_path, connect_args=connect_args)


def init_db():
    engine = _get_engine()
    Base.metadata.create_all(bind=engine)


def get_session():
    engine = _get_engine()
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()
